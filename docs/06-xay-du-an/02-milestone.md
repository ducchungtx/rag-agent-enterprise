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

## Phase 6 lab — Domain Pháp chế ✅ (một phần)

Corpus Luật Đất đai + demo RBAC/isolation; LLM Mistral (chat + embed 1024).  
**Demo:** `make demo-phap-che`; chat citation 3 câu domain.  
**Cấu hình:** [`../01-nen-tang/05-cau-hinh-mistral.md`](../01-nen-tang/05-cau-hinh-mistral.md)

## M5 — Productize (tuỳ chọn — làm tuần tự)

| Bước | Hạng mục | Trạng thái |
|------|----------|------------|
| M5.1 | UI tối thiểu | ✅ `web/` · http://127.0.0.1:8000/ui |
| M5.2 | MCP server read-only | ✅ (xem checklist) |
| M5.3 | Ragas / recall@k | Chưa |
| M5.4 | OIDC | Chưa |
| M5.5 | Đồng bộ Drive/Notion | Chưa |

**Demo M5.1:** mở `/ui` → register → tenant → KB + upload → Chat / Agent SSE.

## M5.6 — UI Stitch → React ✅

App: [`../../frontend/`](../../frontend/). Reference: [`../../ui/`](../../ui/). Lab cũ: `web/` (fallback).

| Bước | Hạng mục | Trạng thái |
|------|----------|------------|
| M5.6a | Shell + Auth | ✅ |
| M5.6b | Chat + Refusal UI | ✅ |
| M5.6c | KB list + upload | ✅ |
| M5.6d | Members + API Keys (list) | ✅ |

**Dev:** `cd frontend && npm run dev` → http://127.0.0.1:5173/ui/  
**Prod:** `npm run build` → FastAPI mount `frontend/dist` tại `/ui`.

## M6 — KB enterprise (vượt demo)

Thiết kế: [05-kb-vuot-demo.md](./05-kb-vuot-demo.md).

| Bước | Hạng mục | Trạng thái |
|------|----------|------------|
| M6.0 | Relevance gate + refusal + ScopeBar | ✅ `RETRIEVAL_MIN_SCORE` |
| M6.1 | Metadata domain / policy KB + document hiệu lực | ⬜ |
| M6.2 | Multi-KB (`kb_ids[]`) + citation có `kb_id` | ⬜ |
| M6.3 | Router domain + eval lệch miền | ⬜ |

**DoD M6.0:** hỏi đất đai trên KB lệch miền / score thấp → `refused=true` + RefusalBanner.

Tag gợi ý: `m0`…`m4`, `m5.1`, `m5.6`, `m6.0` khi bạn muốn đánh dấu git.
