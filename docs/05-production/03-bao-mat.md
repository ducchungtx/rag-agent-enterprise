# 03 — Bảo mật

## Checklist tối thiểu doanh nghiệp

| Hạng mục | Việc |
|----------|------|
| Secrets | Env / secret manager; không commit `.env` |
| Password | Hash mạnh; policy độ dài |
| SSRF | URL fetch / tool web: whitelist DNS (WeKnora có mode whitelist-only) |
| Upload | Giới hạn MIME, size; không thực thi file |
| SQL | ORM/parameterized; không string-concat |
| CORS | Allowlist origin |
| Rate limit | Login + API Key |
| Encryption | TLS terminate; credential AES như WeKnora (sau) |
| Dependency | `govulncheck` / `pip-audit` |

## Destructive confirms

Xóa tenant / xóa toàn bộ docs: yêu cầu `confirm=true` hoặc header riêng — tinh thần exit-10 WeKnora CLI.

## Threat model ngắn

| Threat | Mitigation |
|--------|------------|
| IDOR UUID | Filter tenant + tests |
| Key leak | Hash, rotate, scope hẹp |
| Prompt injection qua document | Tool ACL; không để agent gọi admin tool |
| Tenant escape qua agent | Mọi tool nhận server-side context |

## Tiếp

→ [04 — Deploy](./04-deploy.md)
