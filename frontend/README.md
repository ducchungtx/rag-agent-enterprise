# rae frontend

React + Vite + TypeScript + Tailwind v4 — SPA doanh nghiệp gắn API FastAPI.

## Dev

```bash
# terminal 1 — API
cd .. && uv run uvicorn app.main:app --reload --port 8000

# terminal 2 — FE (proxy API → :8000)
npm install
npm run dev
```

Mở http://127.0.0.1:5173/ui/ (base path `/ui/`).

## Production build

```bash
npm run build   # → dist/
```

FastAPI mount `frontend/dist` tại `/ui` nếu có; không thì fallback `web/` lab.

## Cấu trúc

```text
src/
  api/         client + types
  auth/        AuthContext (JWT, tenant, KB)
  layout/      AppShell
  pages/       Auth, Chat, Knowledge, Members, ApiKeys
  components/  ScopeBar, CitationPanel, RefusalBanner
```

Design reference: [`../ui/`](../ui/).
