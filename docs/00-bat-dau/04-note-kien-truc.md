# Phase 0 — Note kiến trúc (bài tập)

## 1) Request path

```text
Client
  → Middleware (RequestID → Auth JWT|APIKey → Tenant context → RBAC)
  → Handler (DTO validation, không chứa business)
  → Service (nghiệp vụ: ingest, retrieve, agent…)
  → Repository / Vector / Queue / LLM
```

Mọi endpoint nghiệp vụ đi qua cùng chuỗi. Thiếu filter tenant ở bất kỳ tầng nào = rủi ro IDOR.

## 2) Identity model

```text
User ──< TenantMember(role) >── Tenant (workspace)
                                    │
                 KnowledgeBase / Session / APIKey / Document
```

- Một User có thể thuộc nhiều Tenant, mỗi nơi một `role`.
- Tài nguyên nghiệp vụ luôn gắn `tenant_id` — đây là biên giới cách ly dữ liệu.
- Role quyết định *loại hành động*; ownership/share quyết định *tài nguyên cụ thể*.

## 3) Capability ≠ Role (API Key không = Owner)

| Chủ thể | Cơ chế |
|---------|--------|
| User (JWT) | Role trong tenant: Owner / Admin / Contributor / Viewer |
| Machine (API Key) | Capabilities: `retrieve` / `qa` / `ingest` / `admin` + KB allow-list |

API Key **không** map sang bậc Owner. Key chỉ `retrieve` được search, **không** được chat QA hay upload — dù Owner của workspace đã tạo key đó.

## 4) Vì sao Viewer không upload?

Viewer chỉ được đọc KB và chat. Upload/sửa KB thuộc Contributor trở lên (kèm ownership). Giữ Viewer hẹp để team có thể mời người hỏi đáp mà không mở quyền ghi tài liệu.

## 5) Năm service core WeKnora

| Service | Vai trò |
|---------|---------|
| `app` | Go API + RAG + Agent + worker |
| `frontend` | Vue3 UI + NGINX reverse proxy |
| `docreader` | Python gRPC parse tài liệu |
| `postgres` | Business + BM25 + pgvector |
| `redis` | Asynq queue + SSE + rate limit |

MVP của repo này gộp parse in-process, bỏ frontend/docreader riêng ở giai đoạn đầu.
