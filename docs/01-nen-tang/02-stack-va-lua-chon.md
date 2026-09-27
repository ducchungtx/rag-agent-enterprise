# 02 — Stack và lựa chọn công nghệ

## Nguyên tắc

Chọn stack **một lần**, giữ hết lộ trình. Đừng đổi Go ↔ Python giữa chừng.

## Hai hướng đề xuất

### Hướng A — Gần WeKnora nhất (khuyến nghị nếu muốn đọc code gốc dễ)

| Thành phần | Chọn |
|------------|------|
| Language | Go 1.22+ |
| HTTP | Gin |
| ORM | GORM |
| DI | dig hoặc wire tay `main` |
| DB | PostgreSQL 16+ với extension `vector` |
| Auth | golang-jwt |
| Queue (sau) | Asynq |

### Hướng B — Nhanh prototype

| Thành phần | Chọn |
|------------|------|
| Language | Python 3.11+ |
| HTTP | FastAPI |
| ORM | SQLAlchemy 2 / SQLModel |
| DB | PostgreSQL + pgvector |
| Auth | python-jose / Authlib |
| Queue (sau) | Redis + RQ hoặc Celery |

Cả hai hướng đều đạt cùng kiến trúc logic. Tài liệu lab mô tả **hành vi**, không khóa syntax.

## Những gì WeKnora có mà bạn chưa cần

| WeKnora | MVP của bạn |
|---------|-------------|
| ParadeDB (BM25 sẵn) | Postgres + `tsvector` hoặc chỉ vector trước |
| 8 loại vector store | Chỉ pgvector |
| docreader gRPC | Parse in-process (unstructured / pdfplumber) |
| 27 model vendors | 1 OpenAI-compatible endpoint + Ollama |
| Vue frontend đầy đủ | curl / httpie / Swagger UI |

## Cấu trúc repo code đề xuất (tạo ở lab)

```text
rag-agent-enterprise/
├── docs/                 # bạn đang đọc
├── README.md
└── app/                  # hoặc backend/
    ├── cmd/server/
    ├── internal/
    │   ├── handler/
    │   ├── service/
    │   ├── repository/
    │   ├── middleware/
    │   ├── access/
    │   └── types/
    ├── migrations/
    ├── configs/
    └── docker-compose.yml   # chỉ postgres (+ redis sau)
```

## Environment tối thiểu

```bash
DATABASE_URL=postgres://...
JWT_SECRET=dev-only-change-me
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
EMBEDDING_MODEL=nomic-embed-text
CHAT_MODEL=qwen2.5:7b
```

## Tiếp

→ [03 — Mô hình dữ liệu](./03-mo-hinh-du-lieu.md)
