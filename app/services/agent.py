"""Minimal ReAct-style agent with tool registry + optional rule-based fallback."""

from __future__ import annotations

import json
import logging
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.llm import chat_completion
from app.services.retrieve import read_document_text, search_chunks

logger = logging.getLogger(__name__)


@dataclass
class AgentEvent:
    type: str
    data: dict[str, Any]

    def sse(self) -> str:
        return f"event: {self.type}\ndata: {json.dumps(self.data, ensure_ascii=False)}\n\n"


ToolFn = Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolFn] = {}

    def register(self, name: str, fn: ToolFn) -> None:
        self._tools[name] = fn

    def names(self) -> list[str]:
        return list(self._tools)

    def call(self, name: str, **kwargs: Any) -> Any:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name](**kwargs)


def build_tools(db: Session, tenant_id: UUID, kb_id: UUID) -> ToolRegistry:
    reg = ToolRegistry()

    def search_knowledge(query: str, top_k: int = 5) -> list[dict]:
        hits = search_chunks(
            db,
            tenant_id=tenant_id,
            kb_id=kb_id,
            query=query,
            top_k=top_k,
            apply_relevance_gate=True,
        )
        return [h.model_dump(mode="json") for h in hits]

    def read_document(document_id: str) -> dict:
        text = read_document_text(db, tenant_id=tenant_id, document_id=UUID(document_id))
        if text is None:
            return {"error": "forbidden_or_missing", "document_id": document_id}
        return {"document_id": document_id, "content": text}

    reg.register("search_knowledge", search_knowledge)
    reg.register("read_document", read_document)
    return reg


def run_agent_events(
    db: Session,
    *,
    tenant_id: UUID,
    kb_id: UUID,
    question: str,
    max_steps: int = 5,
) -> Iterator[AgentEvent]:
    tools = build_tools(db, tenant_id, kb_id)
    yield AgentEvent("think", {"step": 1, "message": "Planning tool use"})

    # Always search first (rule-based router — works with fake chat / no tool-calling LLM)
    yield AgentEvent("tool_start", {"tool": "search_knowledge", "args": {"query": question}})
    hits = tools.call("search_knowledge", query=question, top_k=5)
    yield AgentEvent("tool_result", {"tool": "search_knowledge", "result": hits})

    if not hits:
        reason = (
            "Không đủ nguồn phù hợp trong Knowledge Base đang chọn để trả lời câu hỏi này."
        )
        suggest = (
            "Hãy đổi sang KB đúng miền hoặc upload tài liệu liên quan rồi hỏi lại."
        )
        yield AgentEvent(
            "done",
            {
                "answer": reason,
                "citations": [],
                "refused": True,
                "refusal_reason": reason,
                "suggested_message": suggest,
                "provider": settings.chat_provider,
            },
        )
        return

    doc_id = hits[0]["document_id"] if hits else None
    if doc_id and max_steps >= 2:
        yield AgentEvent("tool_start", {"tool": "read_document", "args": {"document_id": doc_id}})
        body = tools.call("read_document", document_id=doc_id)
        yield AgentEvent("tool_result", {"tool": "read_document", "result": body})

    contexts = [h["content"] for h in hits]
    answer = chat_completion(
        "Bạn là agent doanh nghiệp pháp chế. CHỈ dựa trên kết quả tool. "
        "Không bịa khi thiếu nguồn.",
        question,
        contexts,
    )
    # Stream tokens (fake chunking)
    for i in range(0, len(answer), 24):
        yield AgentEvent("token", {"text": answer[i : i + 24]})
    yield AgentEvent(
        "done",
        {
            "answer": answer,
            "citations": hits,
            "refused": False,
            "provider": settings.chat_provider,
        },
    )

