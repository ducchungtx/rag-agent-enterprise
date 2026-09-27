# 02 — RBAC 4 cấp

## Ma trận MVP (bám WeKnora)

| Hành động | Viewer | Contributor | Admin | Owner |
|-----------|:------:|:-----------:|:-----:|:-----:|
| Xem KB / search / chat / agent | ✓ | ✓ | ✓ | ✓ |
| Tạo KB / upload document | | ✓ | ✓ | ✓ |
| Sửa/xóa KB của người khác* | | | ✓ | ✓ |
| Mời member / đổi role | | | ✓ | ✓ |
| Xóa / chuyển Owner tenant | | | | ✓ |
| Quản lý API Key tenant | | | ✓ | ✓ |

\*Contributor thường chỉ sửa resource **mình tạo** (ownership) — xem bài 04.

## Cài đặt trong code

```text
type Role string
const (
  RoleViewer Role = "viewer"
  RoleContributor Role = "contributor"
  RoleAdmin Role = "admin"
  RoleOwner Role = "owner"
)

func (r Role) AtLeast(min Role) bool { /* bậc thang */ }
```

Middleware:

```text
RequireRole(RoleContributor)  // upload routes
RequireRole(RoleAdmin)        // members routes
RequireRole(RoleOwner)        // delete tenant
```

## Hai lớp quyền (nhắc lại)

```text
Role          → được phép làm HÀNH ĐỘNG loại này không?
Ownership     → được đụng ĐÚNG resource này không?
```

Ví dụ: Contributor được upload, nhưng không xóa KB của Admin khác trừ khi là owner của KB đó hoặc có share.

## Invite

Flow tối thiểu:

1. Owner/Admin `POST /tenants/:id/invitations { email, role }`  
2. User đăng nhập `POST /invitations/:token/accept`  
3. Tạo `tenant_members` status `active`

WeKnora có invite-only registration — hữu ích khi deploy nội bộ.

## Tiếp

→ [03 — Auth JWT & API Key](./03-auth-jwt-api-key.md)
