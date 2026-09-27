# 06 — Lab: RBAC

## Mục tiêu demo (bắt buộc)

Script hoặc test tự động:

1. Alice Owner tạo tenant + KB + upload  
2. Mời Bob **Viewer** — Bob chat OK, upload **403**  
3. Nâng Bob lên **Contributor** — upload OK  
4. Carol ở tenant khác — không đọc được KB Alice  
5. API Key `retrieve` only — search OK, ingest 403  

## Việc cần implement

- [ ] Middleware `RequireRole`  
- [ ] Invite + accept member  
- [ ] `PATCH /members/:userId` đổi role (Admin+)  
- [ ] Access helpers cho KB  
- [ ] API Key create/list/revoke + gate middleware  
- [ ] Ít nhất 5 test case isolation  
- [ ] Audit log cho upload / delete / invite  

## Structure gợi ý

```text
internal/middleware/auth.go
internal/middleware/rbac.go
internal/middleware/api_key.go
internal/access/kb.go
internal/service/member.go
internal/service/apikey.go
```

## Tham chiếu WeKnora (đọc sâu)

- `website-docs/03-features/01-tenant-auth.md` — toàn bộ khái niệm  
- `internal/application/access/`  
- `internal/middleware/api_key_gate.go`  
- `internal/handler/tenant_member.go`  

## Definition of Done

- [ ] Demo 5 bước trên chạy lại được  
- [ ] Không còn endpoint nghiệp vụ nào thiếu filter tenant  
- [ ] README demo ghi curl mẫu  

## Sau lab

→ Phase 5: [`../05-production/README.md`](../05-production/README.md)
