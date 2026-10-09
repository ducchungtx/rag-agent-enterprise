# App — rag-agent-enterprise

FastAPI MVP: Auth → Tenant/RBAC → KB ingest → hybrid search → chat citation → Agent SSE → API Key.

## Chạy local

```bash
# từ root repo
cp .env.example .env
docker compose up -d postgres redis
uv sync --all-extras
uv run python -m app.bootstrap_db   # hoặc: make db-reset khi đổi EMBEDDING_DIM
uv run uvicorn app.main:app --reload --port 8000
```

Swagger: http://127.0.0.1:8000/docs · UI tối thiểu: http://127.0.0.1:8000/ui

## Headers quan trọng

| Header | Khi nào |
|--------|---------|
| `Authorization: Bearer <jwt>` | User đăng nhập |
| `X-Tenant-Id: <uuid>` | Chọn workspace (JWT) |
| `X-API-Key: rae_...` | Máy gọi API (không cần JWT) |

## Smoke / demo

```bash
make smoke-rag
make smoke-rbac
make demo-phap-che
```

Lab offline: `EMBEDDING_PROVIDER=fake` + `CHAT_PROVIDER=fake`.

### Mistral / Gemini (lab hiện tại)

Chi tiết model + quota: [`docs/01-nen-tang/05-cau-hinh-mistral.md`](../docs/01-nen-tang/05-cau-hinh-mistral.md).

```bash
# .env — cấu hình đã chạy ổn trên máy lab
CHAT_PROVIDER=mistral
CHAT_MODEL=ministral-8b-2512
EMBEDDING_PROVIDER=mistral
EMBEDDING_DIM=1024
EMBEDDING_MODEL=mistral-embed-2312
MISTRAL_API_KEY=...
# GEMINI_API_KEY=...   # tuỳ chọn; đổi CHAT_PROVIDER=gemini + CHAT_MODEL=gemini-3.8-flash
```

Đổi dim embed → `make db-reset` + restart API + ingest lại.
