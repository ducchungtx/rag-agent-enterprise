# 03 — Checklist MVP

- [x] Register tạo personal tenant (Owner)
- [x] JWT + `X-Tenant-Id`
- [x] KB CRUD theo tenant
- [x] Upload md/txt/pdf → chunks + embedding
- [x] Search filter `tenant_id` + `kb_id`
- [x] Chat có `citations[]`
- [x] Agent tools `search_knowledge` + `read_document` + SSE
- [x] RBAC 4 cấp (Viewer không upload)
- [x] Invite + đổi role
- [x] API Key capabilities tách khỏi role
- [x] Audit log
- [x] Request ID middleware
- [x] Redis RQ ingest (bật `USE_ASYNC_INGEST`)
- [x] docker-compose (postgres, redis, api, worker)
- [x] Blueprint domain Pháp chế / Luật Đất đai

## Phase 6 — Domain Pháp chế (bước tiếp theo)

- [ ] Corpus trong `data/docs/` (lab `.md`; `.doc` convert trước khi upload)
- [ ] `make demo-phap-che` pass — xem [04-demo-kich-ban.md](./04-demo-kich-ban.md)
- [ ] Demo tay 2 câu hỏi Luật Đất đai có citation trên Swagger

## Tự kiểm nhanh

1. Viewer upload → 403?  
2. Tenant khác chat KB → 404?  
3. API Key `retrieve` gọi `/chat` → 403?  
