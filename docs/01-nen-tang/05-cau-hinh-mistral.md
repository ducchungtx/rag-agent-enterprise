# Cấu hình Mistral AI (chat / embed)

Repo này **giữ pipeline RAG riêng** (ingest → pgvector → citation). Mistral chỉ thay lớp **LLM** (và tuỳ chọn embedding).

RAG hosted Library ([docs](https://docs.mistral.ai/getting-started/quickstarts/developer/rag-document-search)) là đường khác — không bắt buộc cho MVP trong repo này.

Catalog chung: [docs.mistral.ai/models](https://docs.mistral.ai/models).  
**Bảng dưới = model có trên account lab hiện tại** (quota TPM / RPS).

## Model có thể dùng (account của bạn)

### Chat / LLM (cho `/chat`, agent)

| API id | Vai trò | TPM | RPS | Gợi ý lab |
|--------|---------|-----|-----|-----------|
| `mistral-medium-latest` | Mid LLM | 20k | **1.0** | Q&A chất lượng — dễ **429** nếu spam |
| `mistral-small-2603` | Small LLM | 20k | 1.0 | Rẻ hơn Medium, đủ FAQ |
| `ministral-8b-2512` | Small LLM | 625k | **3.13** | **Khuyến nghị lab** khi Medium bị rate limit |
| `ministral-14b-2512` | Small LLM | 937.5k | 0.5 | Chất lượng hơn 8B, RPS thấp |
| `ministral-3b-2512` | Lightweight | 1.3M | **12.5** | Ping API / test latency |
| `mistral-large-2512` | Frontier | 250k | 1.0 | Câu khó, nhiều ngữ cảnh |
| `mistral-large-4` | Frontier | 20k | 0.83 | Mạnh nhất — dùng sparingly |
| `zai-glm-5-3` | General LLM | 20k | 1.0 | Thử so sánh chất lượng |
| `glm-5-2` | LLM | — | 1.0 | Thử nghiệm |
| `labs-leanstral-1-5-1` | Experimental | 5M | 0.63 | Không cần cho RAG pháp chế |

Không dùng cho chat RAG: `codestral-2508` (code), `mistral-moderation-2603`, các `voxtral-*` (audio/TTS/STT).

### Embedding

| API id | TPM | RPS | Dim | Ghi chú |
|--------|-----|-----|-----|---------|
| `mistral-embed-2312` | 20M | 1.0 | **1024** | **Khuyến nghị** khi bật embed Mistral |
| `codestral-embed` | 50k | 1.0 | (code) | Không phù hợp corpus luật |

Cách A (lab nhanh): giữ `EMBEDDING_PROVIDER=fake` — không đụng dim DB.  
Cách B: `EMBEDDING_MODEL=mistral-embed-2312` + `EMBEDDING_DIM=1024` + `make db` + re-ingest.

## Nhiều provider (Mistral + Gemini)

Giữ **cả hai key** trong `.env`. Base URL tự chọn theo `CHAT_PROVIDER` (không cần sửa `LLM_BASE_URL`).

```bash
MISTRAL_API_KEY=...
GEMINI_API_KEY=...

# Đang dùng Mistral:
CHAT_PROVIDER=mistral
CHAT_MODEL=mistral-medium-latest

# Đổi sang Gemini (restart API) — catalog: https://ai.google.dev/gemini-api/docs/models
# CHAT_PROVIDER=gemini
# CHAT_MODEL=gemini-3.8-flash
```

Gemini OpenAI-compatible: [ai.google.dev/gemini-api/docs/openai](https://ai.google.dev/gemini-api/docs/openai).

### Gemini — model phù hợp RAG chat (text)

Nguồn: [Gemini API Models](https://ai.google.dev/gemini-api/docs/models) (cập nhật ~2026-10).

| API id (`CHAT_MODEL`) | Vai trò | Gợi ý lab |
|------------------------|---------|-----------|
| `gemini-3.8-flash` | Flash mới nhất (stable) | **Khuyến nghị** — agent / Q&A doanh nghiệp |
| `gemini-3.7-flash` / `gemini-3.6-flash` | Flash thế hệ trước | Fallback nếu 3.8 chưa mở trên key |
| `gemini-3.5-flash` | Flash legacy | Throughput thường |
| `gemini-3.5-flash-lite` / `gemini-3.1-flash-lite` | Rẻ / nhanh | Smoke nhiều câu |
| `gemini-3.1-pro-preview` | Pro (preview) | Câu khó, reasoning |
| `gemini-2.5-flash` / `gemini-2.5-pro` | Family 2.5 | Chỉ nếu account đã từng dùng 2.5 (Google hạn chế user mới → nên dùng 3.x) |
| `gemini-flash-latest` | Alias “latest” | Tiện, nhưng model phía sau có thể đổi |

**Không dùng** cho `/chat` RAG text: Live / TTS / Transcribe (`gemini-*-live*`, `*-tts`), image (Nano Banana), video (Veo / Omni), music (Lyria), Deep Research agent.

### Gemini — embedding (sau này)

| API id | Ghi chú |
|--------|---------|
| `gemini-embedding-001` | Text embed cho RAG |
| `gemini-embedding-2-preview` | Multimodal embed (preview) |

Khi bật: `EMBEDDING_PROVIDER=gemini` + kiểm tra dim vector thực tế rồi set `EMBEDDING_DIM` + `make db` + re-ingest.

## Cách A — Chat Mistral (khuyến nghị bắt đầu)

```bash
CHAT_PROVIDER=mistral
EMBEDDING_PROVIDER=fake
EMBEDDING_DIM=384
MISTRAL_API_KEY=sk-...
CHAT_MODEL=mistral-medium-latest
# hoặc: ministral-8b-2512 | mistral-small-2603 | mistral-large-2512
```

Restart API (`make run`). Không cần re-ingest.

## Cách B — Embed `mistral-embed-2312`

```bash
EMBEDDING_PROVIDER=mistral
EMBEDDING_DIM=1024
EMBEDDING_MODEL=mistral-embed-2312
CHAT_PROVIDER=mistral
LLM_BASE_URL=https://api.mistral.ai/v1
MISTRAL_API_KEY=sk-...
CHAT_MODEL=mistral-medium-latest
```

```bash
make db
make demo-phap-che   # hoặc upload lại corpus
```

## Kiểm tra nhanh

```bash
curl -s http://127.0.0.1:8000/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  -H 'Content-Type: application/json' \
  -d '{"kb_id":"...","question":"Đất ở có thời hạn 50 năm không?"}'
```

## Endpoint khu vực

| Base | Ghi chú |
|------|---------|
| `https://api.mistral.ai/v1` | Global (mặc định) |
| `https://api.eu.mistral.ai/v1` | EU |
| `https://api.us.mistral.ai/v1` | US |
