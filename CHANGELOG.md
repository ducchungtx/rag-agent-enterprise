# Changelog

## Unreleased

- Docs: `docs/06-xay-du-an/05-kb-vuot-demo.md` — KB vượt demo (sơ đồ lỗ hổng, cấu trúc KB DN, roadmap P0–P3 / M6); liên kết blueprint, milestone, checklist, schema.

## 0.1.0 — MVP learning implementation

- Phase 0: architecture notes + WeKnora path (macOS)
- Phase 1: FastAPI auth, personal tenant, JWT
- Phase 2: KB ingest (md/txt/pdf), pgvector search, chat citations
- Phase 3: Agent tools + SSE (`/agent/chat`)
- Phase 4: RBAC 4 roles, invite/role patch, API Key capabilities, audit
- Phase 5: Redis RQ async ingest, request_id, rate limit, docker-compose
- Phase 6: Blueprint Pháp chế / Luật Đất đai + milestones checklist
- Phase 6 lab: corpus `data/docs/` + `converted/`, `make demo-phap-che`
- LLM: Mistral/Gemini providers; chat `ministral-8b-2512`; embed `mistral-embed-2312` (dim 1024, batch+retry); `make db-reset`
- M5.1: minimal UI (`web/`) served at `/ui` — login, tenant, KB upload, chat + agent SSE
