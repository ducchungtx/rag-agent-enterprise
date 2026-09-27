# 05 — Audit và cô lập dữ liệu

## Audit log tối thiểu

Bảng `audit_logs`:

| Cột | Ví dụ |
|-----|-------|
| `tenant_id` | |
| `actor_user_id` / `actor_api_key_id` | |
| `action` | `kb.delete`, `member.invite`, `document.upload` |
| `resource_type` / `resource_id` | |
| `ip`, `request_id`, `created_at` | |
| `meta` JSON | diff nhẹ, không lưu secret |

Ghi log với hành động **destructive** và **authz deny** (để bắt brute IDOR).

## Test isolation (viết automated)

| Test | Kỳ vọng |
|------|---------|
| User B đoán UUID KB của A | 404 hoặc 403, body không có name/content |
| API Key tenant A + header tenant B | Reject |
| Viewer upload | 403 `auth.forbidden` |
| Search không truyền filter tenant | Fail closed trong repository |

## Error codes gợi ý

| Code | Khi nào |
|------|---------|
| `auth.unauthenticated` | Thiếu/sai token |
| `auth.forbidden` | Có identity nhưng thiếu quyền |
| `resource.not_found` | Không thấy **trong phạm vi được phép** (không tiết lộ tồn tại cross-tenant) |
| `input.confirmation_required` | Xóa workspace / xóa hàng loạt |

WeKnora: tách `not_found` vs `forbidden` cẩn thận để không leak.

## Fail closed

Mọi đường search/chat/agent **mặc định deny** nếu thiếu tenant context.  
Không có nhánh “dev bypass” trên nhánh main.

## Tiếp

→ [06 — Lab RBAC](./06-lab-rbac.md)
