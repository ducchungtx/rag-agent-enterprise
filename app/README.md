# App — rag-agent-enterprise

FastAPI MVP: Auth → Tenant/RBAC → KB ingest → hybrid search → chat citation → Agent SSE → API Key.

## Chạy local

```bash
# từ root repo
cp .env.example .env
docker compose up -d postgres redis
uv sync --all-extras
uv run python -m app.bootstrap_db
uv run uvicorn app.main:app --reload --port 8000
```

Swagger: http://127.0.0.1:8000/docs

## Headers quan trọng

| Header | Khi nào |
|--------|---------|
| `Authorization: Bearer <jwt>` | User đăng nhập |
| `X-Tenant-Id: <uuid>` | Chọn workspace (JWT) |
| `X-API-Key: rae_...` | Máy gọi API (không cần JWT) |

## Smoke

```bash
make smoke-rag
make smoke-rbac
```

`EMBEDDING_PROVIDER=fake` và `CHAT_PROVIDER=fake` mặc định — không cần Ollama để lab.

### Mistral AI (chat)

Giữ RAG/pgvector trong repo; chỉ đổi LLM sang Mistral (OpenAI-compatible). Chi tiết: [`docs/01-nen-tang/05-cau-hinh-mistral.md`](../docs/01-nen-tang/05-cau-hinh-mistral.md).

```bash
# trong .env — xem quota account trong docs/01-nen-tang/05-cau-hinh-mistral.md
CHAT_PROVIDER=mistral
EMBEDDING_PROVIDER=fake
LLM_BASE_URL=https://api.mistral.ai/v1
MISTRAL_API_KEY=sk-...
CHAT_MODEL=mistral-medium-latest   # hoặc ministral-8b-2512 / mistral-large-2512
# Gemini: CHAT_PROVIDER=gemini  CHAT_MODEL=gemini-3.8-flash
# embed sau: EMBEDDING_MODEL=mistral-embed-2312 + EMBEDDING_DIM=1024
```
