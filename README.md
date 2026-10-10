# rag-agent-enterprise

Học kiến trúc và xây **Agent AI doanh nghiệp có phân quyền**, lấy [WeKnora](../WeKnora) làm mẫu tham chiếu thực tế.

> Repo gồm **lộ trình học (`docs/`)** + **MVP code (`app/`)** — Python/FastAPI, PostgreSQL+pgvector, Redis RQ.

## Chạy nhanh MVP

```bash
cp .env.example .env
docker compose up -d postgres redis
uv sync --all-extras
uv run python -m app.bootstrap_db   # đổi EMBEDDING_DIM → make db-reset
uv run uvicorn app.main:app --reload --port 8000
# smoke: make smoke-rag && make smoke-rbac
# Phase 6: make demo-phap-che

# Frontend React (dev)
cd frontend && npm install && npm run dev   # http://127.0.0.1:5173/ui/
# Prod UI: cd frontend && npm run build → FastAPI serve dist tại /ui
```

Chi tiết API: [`app/README.md`](./app/README.md) · FE: [`frontend/README.md`](./frontend/README.md) · LLM: [`docs/01-nen-tang/05-cau-hinh-mistral.md`](./docs/01-nen-tang/05-cau-hinh-mistral.md) · Swagger: http://127.0.0.1:8000/docs · UI: http://127.0.0.1:8000/ui

## Mục tiêu

Sau khi đi hết lộ trình, bạn có thể tự thiết kế và implement một hệ thống gồm:

1. **RAG** — ingest tài liệu → chunk → embed → hybrid search → trả lời có citation  
2. **Agent** — vòng ReAct, tools, streaming SSE  
3. **Phân quyền doanh nghiệp** — multi-tenant (workspace), RBAC 4 cấp, JWT + API Key, ownership, audit  
4. **Production basics** — hàng đợi bất đồng bộ, tracing, deploy

## Lộ trình (dễ → khó)

| Phase | Thư mục | Độ khó | Thời lượng gợi ý | Kết quả |
|-------|---------|--------|------------------|---------|
| 0 | [`docs/00-bat-dau/`](./docs/00-bat-dau/) | ★☆☆☆☆ | 0.5 ngày | Hiểu mục tiêu, map sang WeKnora |
| 1 | [`docs/01-nen-tang/`](./docs/01-nen-tang/) | ★★☆☆☆ | 2–3 ngày | API skeleton + mô hình dữ liệu |
| 2 | [`docs/02-rag-co-ban/`](./docs/02-rag-co-ban/) | ★★★☆☆ | 1 tuần | Mini RAG chạy được |
| 3 | [`docs/03-agent/`](./docs/03-agent/) | ★★★☆☆ | 1 tuần | Mini Agent + tools + SSE |
| 4 | [`docs/04-phan-quyen/`](./docs/04-phan-quyen/) | ★★★★☆ | 1–1.5 tuần | RBAC + tenant isolation |
| 5 | [`docs/05-production/`](./docs/05-production/) | ★★★★☆ | 3–5 ngày | Queue, observability, security |
| 6 | [`docs/06-xay-du-an/`](./docs/06-xay-du-an/) | ★★★★★ | liên tục | Blueprint & milestone dự án thật |

**Bắt đầu tại:** [`docs/00-bat-dau/01-muc-tieu-va-pham-vi.md`](./docs/00-bat-dau/01-muc-tieu-va-pham-vi.md)

## Nguyên tắc học (rút từ WeKnora)

1. **SDK / schema trước, convention sau** — thiết kế API từ model dữ liệu, không đoán flag.  
2. **Handler → Service → Repository** — Handler không chứa business logic.  
3. **Tenant là biên giới tài nguyên** — mọi KB, Agent, Session thuộc một workspace.  
4. **Role + ownership** — role cho phép *loại hành động*; ownership/share quyết định *tài nguyên nào*.  
5. **KB ≠ túi file** — miền, quyền, relevance gate, lifecycle; xem [`docs/06-xay-du-an/05-kb-vuot-demo.md`](./docs/06-xay-du-an/05-kb-vuot-demo.md).  
6. **Agent-friendly errors** — lỗi có mã typed, hint hành động tiếp theo.  
7. **Đừng auto-approve destructive** — thao tác xóa cần xác nhận tường minh.

## Map nhanh sang WeKnora

| Khái niệm doanh nghiệp | Trong WeKnora | Package tham chiếu |
|------------------------|---------------|-------------------|
| Workspace / Tenant | `Tenant` | `internal/application/service` tenant* |
| Thành viên + vai trò | `TenantMember` (Owner/Admin/Contributor/Viewer) | docs `01-tenant-auth` |
| Kho kiến thức | `KnowledgeBase` | handler + service knowledge* |
| Pipeline hỏi đáp | `chat_pipeline` (plugin events) | `internal/application/service/chat_pipeline` |
| Agent loop | think → act → observe | `internal/agent` |
| Auth | JWT / OIDC / API Key | `internal/middleware`, `internal/handler/auth*` |
| Hàng đợi | Asynq + Redis | document process workers |
| CLI / MCP | `cli/`, MCP built-in | `cli/AGENTS.md` |

Đường dẫn WeKnora trên máy bạn: `/Users/mac/Desktop/Projects/Learn/AI/WeKnora`.

## Cấu trúc thư mục tài liệu

```text
docs/
├── 00-bat-dau/          # Định hướng
├── 01-nen-tang/         # Kiến trúc & skeleton
├── 02-rag-co-ban/       # Ingest + retrieval + QA
├── 03-agent/            # ReAct, tools, SSE
├── 04-phan-quyen/       # Multi-tenant + RBAC (trọng tâm)
├── 05-production/       # Queue, obs, security, deploy
└── 06-xay-du-an/        # Blueprint dự án thật
```

Mỗi phase có bài lý thuyết + **lab** (bài tập thực hành). Làm lab trước khi sang phase sau.

## Stack đề xuất cho dự án học (tối giản so với WeKnora)

| Lớp | Gợi ý | Ghi chú |
|-----|-------|---------|
| Backend | **Python (FastAPI)** (đã chọn) | Học ý tưởng từ WeKnora Go; lab code trong `app/` |
| Frontend | Vue 3 hoặc Next.js (tùy bạn) | Phase 1–4 có thể chỉ API + curl |
| DB | PostgreSQL + pgvector | Đủ cho BM25/fulltext + vector |
| Queue | Redis + Asynq (Go) / RQ/Celery (Py) | Phase 5 mới bắt buộc |
| LLM | OpenAI-compatible hoặc Ollama | Dùng local trước cho rẻ |

Chi tiết lựa chọn: [`docs/01-nen-tang/02-stack-va-lua-chon.md`](./docs/01-nen-tang/02-stack-va-lua-chon.md).

## License học tập

Tài liệu trong repo này phục vụ học tập cá nhân. WeKnora gốc là MIT — khi tham chiếu code, giữ attribution phù hợp.
