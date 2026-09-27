# 04 — Ownership và chia sẻ

## Ownership

`knowledge_bases.owner_user_id` = người tạo.

| Actor | Xóa KB |
|-------|--------|
| Owner của KB | ✓ |
| Admin/Owner tenant | ✓ |
| Contributor khác | ✗ |
| Viewer | ✗ |

Tách “role workspace” khỏi “chủ resource” tránh mọi Contributor xóa lung tung.

## Access helper (học từ `internal/application/access`)

```text
CanViewKB(ctx, kb) bool
CanEditKB(ctx, kb) bool
CanDeleteKB(ctx, kb) bool
```

Bên trong:

1. Cùng `tenant_id`?  
2. Role bậc thang?  
3. Owner hoặc shared?  

Handler **không** tự if-else rải rác — gọi access package để một nơi sửa policy.

## Share (phiên bản rút gọn)

MVP nội bộ tenant: chưa share.  

Phase sau (như WeKnora):

- Share KB cho member cụ thể với permission `view|edit`  
- Hoặc Organization share cross-tenant  

Khi share: bảng `kb_shares(kb_id, grantee_user_id, permission)`.

## Agent & ownership

Custom Agent cũng có owner + có thể giới hạn KB scope.  
Agent chạy dưới quyền **caller**, không escalate lên Owner.

## Tiếp

→ [05 — Audit & isolation](./05-audit-isolation.md)
