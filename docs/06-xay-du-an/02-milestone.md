# 02 — Milestone giao hàng

## M0 — Skeleton (Phase 1) ✅

Auth + tenant + health.  
**Demo:** `POST /auth/register|login`, `GET /auth/me`, `GET /health`.

## M1 — RAG (Phase 2) ✅

Ingest + search + chat citation.  
**Demo:** `scripts/smoke_rag.sh` với `testdata/sample-policy.md`.

## M2 — Agent (Phase 3) ✅

Tools + SSE.  
**Demo:** `POST /agent/chat` (SSE events: think/tool_start/tool_result/token/done).

## M3 — Enterprise authz (Phase 4) ✅

RBAC + API Key + isolation.  
**Demo:** `scripts/smoke_rbac.sh` (Viewer 403 upload, Carol 404, key retrieve≠qa).

## M4 — Harden (Phase 5) ✅

Worker queue + compose + audit + request_id.  
**Demo:** `docker compose up` (api + worker + postgres + redis); `GET /audit`.

## M5 — Productize (tuỳ chọn — chưa làm)

- UI tối thiểu  
- OIDC  
- Đồng bộ Drive/Notion  
- MCP server read-only  
- Ragas / recall@k  

Tag gợi ý: `m0`…`m4` khi bạn muốn đánh dấu git.
