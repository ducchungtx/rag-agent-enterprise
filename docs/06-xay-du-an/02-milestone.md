# 02 — Milestone giao hàng

## M0 — Skeleton (Phase 1)

Auth + tenant + health.  
**Demo:** register/login/me.

## M1 — RAG (Phase 2)

Ingest + search + chat citation.  
**Demo:** 1 KB chính sách nội bộ.

## M2 — Agent (Phase 3)

Tools + SSE.  
**Demo:** câu hỏi cần 2 bước search→read.

## M3 — Enterprise authz (Phase 4)

RBAC + API Key + isolation tests.  
**Demo:** Viewer/Contributor + key scoped.

## M4 — Harden (Phase 5)

Worker queue + compose + audit.  
**Demo:** upload PDF lớn, theo dõi status.

## M5 — Productize (tuỳ chọn)

- UI tối thiểu  
- OIDC  
- Nguồn đồng bộ (Drive/Notion)  
- MCP server read-only cho Cursor  
- Đánh giá retrieval (recall@k)  

Mỗi milestone: tag git `m0`…`m4` + ghi chú trong `CHANGELOG.md`.
