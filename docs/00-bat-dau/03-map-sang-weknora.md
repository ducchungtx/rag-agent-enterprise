# 03 — Map sang WeKnora

Tài liệu học **không** thay docs chính thức. Dùng bảng này như mục lục “soi code mẫu”.

Root WeKnora: `E:\Projects\learning\AI\WeKnora`

## Đọc theo phase

### Phase 1 — Nền tảng

| Chủ đề | File / thư mục WeKnora |
|--------|------------------------|
| Tổng quan kiến trúc | `website-docs/02-architecture/01-overview.md` |
| Backend layers | `website-docs/02-architecture/02-backend-design.md` |
| Entry server | `cmd/server/` |
| Router + middleware | `internal/router/`, `internal/middleware/` |
| DI container | `internal/container/container.go` |

### Phase 2 — RAG

| Chủ đề | File / thư mục WeKnora |
|--------|------------------------|
| Document pipeline | `website-docs/02-architecture/03-document-pipeline.md` |
| RAG pipeline | `website-docs/02-architecture/04-rag-pipeline.md` |
| Chat pipeline plugins | `internal/application/service/chat_pipeline/` |
| Retrieval | `internal/application/repository/retriever/` |
| Knowledge handler | `internal/handler/knowledge*.go` |

### Phase 3 — Agent

| Chủ đề | File / thư mục WeKnora |
|--------|------------------------|
| Agent engine | `internal/agent/` (think / act / observe) |
| Tools | `internal/agent/tools/` (đặc biệt `search_knowledge.go`) |
| Stream / SSE | `internal/stream/`, handler session |
| CLI agent contract | `cli/AGENTS.md` |

### Phase 4 — Phân quyền (trọng tâm)

| Chủ đề | File / thư mục WeKnora |
|--------|------------------------|
| Tenant & auth (docs) | `website-docs/03-features/01-tenant-auth.md` |
| Auth handler | `internal/handler/auth*.go` |
| Tenant members | `internal/handler/tenant_member.go` |
| Access rules | `internal/application/access/` |
| API Key gate | `internal/middleware/api_key_gate.go` |
| RBAC middleware | `internal/middleware/` (rbac / tenant match) |

### Phase 5 — Production

| Chủ đề | File / thư mục WeKnora |
|--------|------------------------|
| Async tasks | `website-docs/02-architecture/05-async-tasks.md` |
| Observability | docs feature observability + `internal/tracing/` |
| Compose deploy | `docker-compose.yml`, `.env.example` |
| Security notes | `SECURITY.md`, SSRF utils |

## Ba sơ đồ “nhớ thuộc”

### 1) Request path

```text
Client → Middleware (Auth, Tenant, RBAC)
       → Handler (DTO)
       → Service (business)
       → Repository / Agent / Queue
```

### 2) Identity model (rút gọn)

```text
User ──< TenantMember(role) >── Tenant (workspace)
                                    │
                    KnowledgeBase / Agent / Session / APIKey
```

### 3) Capability tách khỏi Role

| Chủ thể | Cách cấp quyền |
|---------|----------------|
| User (JWT) | Role trong tenant + ownership/share trên resource |
| Machine (API Key) | Capabilities (`retrieve`/`qa`/`ingest`/`admin`) + KB allow-list |

WeKnora **không** map API Key = role Owner. Học đúng điểm này ở Phase 4.

## Bài tập Phase 0 (15 phút)

1. Mở `website-docs/02-architecture/01-overview.md` — liệt kê 5 service core.  
2. Mở `website-docs/03-features/01-tenant-auth.md` — viết lại bằng tiếng Việt 4 role.  
3. Trả lời: *Tại sao Viewer không được upload?* (1–2 câu).

## Liên kết tiếp

→ Phase 1: [`../01-nen-tang/README.md`](../01-nen-tang/README.md)
