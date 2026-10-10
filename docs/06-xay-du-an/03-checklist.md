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

## Phase 6 — Domain Pháp chế

- [x] Corpus `data/docs/` (tóm tắt `.md` + `converted/*.txt` từ `.doc`)
- [x] `make demo-phap-che` / ingest lab pass
- [x] Chat domain có citation (Đ.171 đất ở, NĐ 88, thời hạn 50 năm)
- [x] LLM thật: Mistral chat (`ministral-8b-2512`) + embed (`mistral-embed-2312`, dim 1024)
- [ ] (Tuỳ chọn) So sánh Gemini `gemini-3.8-flash`
- [x] M5.1 UI tối thiểu — `web/` (lab) / React `frontend/` tại `/ui`
- [x] M5.2 MCP server read-only — `POST /mcp` (JSON-RPC: `initialize`, `tools/list`, `tools/call` với `list_knowledge_bases` / `search_knowledge` / `answer_question`; phân quyền qua JWT + `X-Tenant-Id` hoặc API Key capability `kb.search` + kb_allowlist)
- [x] M5.6 React SPA — `frontend/` (Vite+TS+Tailwind); Auth/Chat/KB/Members/API Keys; CORS + proxy
- [ ] M5.3 Ragas / recall@k
- [ ] M5.4 OIDC
- [ ] M5.5 Đồng bộ Drive/Notion

## M6 — KB vượt demo (enterprise)

Thiết kế + sơ đồ: [05-kb-vuot-demo.md](./05-kb-vuot-demo.md)

- [x] M6.0 Relevance gate + refusal khi score thấp (`RETRIEVAL_MIN_SCORE`, `ChatOut.refused`)
- [x] M6.0 UI ScopeBar + RefusalBanner (`frontend/`)
- [ ] M6.1 Metadata `domain` / policy KB + document `effective_*`
- [ ] M6.2 Search/chat `kb_ids[]` (multi-KB trong tenant + ACL)
- [ ] M6.3 Bộ câu vàng tự động: đất đai trên KB HN-GĐ → từ chối đúng

Chi tiết chạy: [04-demo-kich-ban.md](./04-demo-kich-ban.md) · LLM: [05-cau-hinh-mistral.md](../01-nen-tang/05-cau-hinh-mistral.md)

## Tự kiểm nhanh

1. Viewer upload → 403?  
2. Tenant khác chat KB → 404?  
3. API Key `retrieve` gọi `/chat` → 403?  
