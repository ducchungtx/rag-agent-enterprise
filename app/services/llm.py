"""Embedding + chat providers. fake = offline deterministic for labs.

OpenAI-compatible backends (Ollama, Mistral, …) share the same HTTP paths:
  POST {base}/chat/completions
  POST {base}/embeddings

Mistral: see docs/01-nen-tang/05-cau-hinh-mistral.md
"""

from __future__ import annotations

import hashlib
import logging
import math
import re
import time
from typing import Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)

# Mistral embed account often has RPS≈1 — keep batches small + pause between calls.
_EMBED_BATCH_SIZE = 32
_EMBED_MIN_INTERVAL_S = 1.05
_EMBED_MAX_RETRIES = 5


class LLMError(RuntimeError):
    """Raised when the upstream chat/embed API fails."""

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


def _tokenize(text: str) -> list[str]:
    return [t for t in re.split(r"\W+", text.lower()) if t]


def fake_embed(text: str, dim: int | None = None) -> list[float]:
    """Deterministic bag-of-hash embedding for local labs without Ollama."""
    dim = dim or settings.embedding_dim
    vec = [0.0] * dim
    for token in _tokenize(text):
        digest = hashlib.sha256(token.encode()).digest()
        for i in range(0, min(len(digest), dim)):
            vec[i % dim] += (digest[i] - 128) / 128.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def embed_texts(texts: list[str]) -> list[list[float]]:
    if settings.uses_openai_compatible_embed():
        return _openai_embed(texts)
    return [fake_embed(t) for t in texts]


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]


def _openai_embed(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    provider = settings.embedding_provider
    url = f"{settings.resolved_llm_base_url(provider).rstrip('/')}/embeddings"
    headers = {"Authorization": f"Bearer {settings.resolved_llm_api_key(provider)}"}
    out: list[list[float]] = []
    last_call = 0.0
    with httpx.Client(timeout=120.0) as client:
        for i in range(0, len(texts), _EMBED_BATCH_SIZE):
            batch = texts[i : i + _EMBED_BATCH_SIZE]
            # Respect RPS≈1 for mistral-embed
            elapsed = time.monotonic() - last_call
            if last_call and elapsed < _EMBED_MIN_INTERVAL_S:
                time.sleep(_EMBED_MIN_INTERVAL_S - elapsed)
            vectors = _embed_batch_with_retry(client, url, headers, batch, provider)
            last_call = time.monotonic()
            out.extend(vectors)
            logger.info(
                "Embedded batch %s-%s / %s (provider=%s model=%s)",
                i + 1,
                i + len(batch),
                len(texts),
                provider,
                settings.embedding_model,
            )
    return out


def _embed_batch_with_retry(
    client: httpx.Client,
    url: str,
    headers: dict[str, str],
    batch: list[str],
    provider: str,
) -> list[list[float]]:
    payload = {"model": settings.embedding_model, "input": batch}
    delay = _EMBED_MIN_INTERVAL_S
    for attempt in range(1, _EMBED_MAX_RETRIES + 1):
        resp = client.post(url, json=payload, headers=headers)
        if resp.status_code == 429:
            logger.warning("Embed 429 attempt %s/%s — sleep %.1fs", attempt, _EMBED_MAX_RETRIES, delay)
            time.sleep(delay)
            delay = min(delay * 2, 16.0)
            continue
        if resp.status_code >= 400:
            raise LLMError(
                f"Embed error {resp.status_code} provider={provider} "
                f"model={settings.embedding_model}: {resp.text[:300]}",
                status_code=resp.status_code,
            )
        data = resp.json()["data"]
        data = sorted(data, key=lambda x: x["index"])
        vectors = [row["embedding"] for row in data]
        if vectors and len(vectors[0]) != settings.embedding_dim:
            raise LLMError(
                f"Embedding dim mismatch: got {len(vectors[0])} expected {settings.embedding_dim}. "
                "Set EMBEDDING_DIM cho khớp model rồi make db --reset.",
                status_code=None,
            )
        return vectors
    raise LLMError(
        f"Embed rate limit (429) sau {_EMBED_MAX_RETRIES} lần — provider={provider} "
        f"model={settings.embedding_model}",
        status_code=429,
    )


def chat_completion(system: str, user: str, context_blocks: list[str] | None = None) -> str:
    if settings.uses_openai_compatible_chat():
        return _openai_chat(system, user, context_blocks or [])
    return _fake_chat(user, context_blocks or [])


def _fake_chat(question: str, contexts: list[str]) -> str:
    if not contexts:
        return "Không có dữ liệu phù hợp trong knowledge base để trả lời câu hỏi này."
    q_tokens = set(_tokenize(question))
    scored: list[tuple[int, str]] = []
    for ctx in contexts:
        overlap = len(q_tokens & set(_tokenize(ctx)))
        scored.append((overlap, ctx))
    scored.sort(key=lambda x: x[0], reverse=True)
    best = scored[0][1]
    sentences = re.split(r"(?<=[.!?。])\s+|\n+", best)
    pick = sentences[0] if sentences else best
    for s in sentences:
        if len(set(_tokenize(s)) & q_tokens) >= max(1, len(q_tokens) // 3):
            pick = s
            break
    return f"Theo tài liệu: {pick.strip()}"


def _openai_chat(system: str, user: str, contexts: list[str]) -> str:
    ctx = "\n\n".join(f"[{i+1}] {c}" for i, c in enumerate(contexts))
    messages = [
        {"role": "system", "content": system},
        {
            "role": "user",
            "content": f"Ngữ cảnh:\n{ctx}\n\nCâu hỏi: {user}\nTrả lời ngắn gọn, chỉ dựa trên ngữ cảnh.",
        },
    ]
    provider = settings.chat_provider
    url = f"{settings.resolved_llm_base_url(provider).rstrip('/')}/chat/completions"
    headers = {"Authorization": f"Bearer {settings.resolved_llm_api_key(provider)}"}
    payload: dict[str, Any] = {
        "model": settings.chat_model,
        "messages": messages,
        "temperature": 0.2,
    }
    with httpx.Client(timeout=120.0) as client:
        resp = client.post(url, json=payload, headers=headers)
        if resp.status_code >= 400:
            detail = resp.text[:300]
            if resp.status_code == 429:
                raise LLMError(
                    f"LLM rate limit (429) provider={provider} model={settings.chat_model}. "
                    f"Đợi vài giây hoặc đổi CHAT_MODEL (vd. ministral-8b-2512 / gemini-3.8-flash). "
                    f"Body: {detail}",
                    status_code=429,
                )
            raise LLMError(
                f"LLM error {resp.status_code} provider={provider} model={settings.chat_model}: {detail}",
                status_code=resp.status_code,
            )
        return resp.json()["choices"][0]["message"]["content"]
