# UI — Stitch exports + design system

Design system: [`DESIGN.md`](./DESIGN.md) (Jurisprudence Precision).  
Product brief: [`../docs/06-xay-du-an/06-ui-brief-ai.md`](../docs/06-xay-du-an/06-ui-brief-ai.md).  
KB enterprise gap: [`../docs/06-xay-du-an/05-kb-vuot-demo.md`](../docs/06-xay-du-an/05-kb-vuot-demo.md).

**App React đang chạy:** [`../frontend/`](../frontend/) — `npm run dev` hoặc build mount `/ui`.  
Lab cũ: `web/` (fallback nếu chưa có `frontend/dist`).

## Bản đồ màn hình (reference Stitch)

| # | Thư mục | Màn brief | Nội dung chính | FE status |
|---|---------|-----------|----------------|-----------|
| 01 | [`screens/01-auth/`](./screens/01-auth/) | A Auth | Brand rae hero, login | ✅ `AuthPage` |
| 02 | [`screens/02-chat-success/`](./screens/02-chat-success/) | E Chat | Scope bar + citations | ✅ `ChatPage` |
| 03 | [`screens/03-chat-refusal/`](./screens/03-chat-refusal/) | E Refusal | Lệch miền → từ chối | ✅ + M6.0 API |
| 04 | [`screens/04-kb-list/`](./screens/04-kb-list/) | D KB list | Domain / mô tả | ✅ list + create |
| 05 | [`screens/05-kb-detail/`](./screens/05-kb-detail/) | D2 Detail | Upload corpus | ✅ upload trên Knowledge |
| 06 | [`screens/06-members/`](./screens/06-members/) | F Members | RBAC | ✅ list |
| 07 | [`screens/07-api-keys/`](./screens/07-api-keys/) | F API Keys | Allowlist | ✅ list |

Mỗi folder: `screen.png` · `code.html` · `DESIGN.md`. Zip gốc: `stitch_*.zip`.

## M6.0

- Backend: `RETRIEVAL_MIN_SCORE` (mặc định `0.22`) → `ChatOut.refused` + agent `done.refused`
- FE: `ScopeBar` + `RefusalBanner`
