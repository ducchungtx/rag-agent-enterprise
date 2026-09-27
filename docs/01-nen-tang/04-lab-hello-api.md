# 04 — Lab: Hello API

## Mục tiêu lab

Trong `app/` (hoặc `backend/`), dựng skeleton chạy được:

- `GET /health` → `{ "ok": true }`
- `POST /auth/register` + `POST /auth/login` → JWT
- `GET /auth/me` (có Bearer) → user + danh sách memberships
- Tự tạo **personal tenant** khi register (giống WeKnora `create_personal`)

## Bước làm

### 1. Khởi tạo project + Docker Postgres

```bash
# trong rag-agent-enterprise/
mkdir -p app
cd app
# Go: go mod init github.com/you/rag-agent-enterprise
# hoặc Python: uv init / poetry init
```

`docker-compose.yml` tối giản:

```yaml
services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: rag_enterprise
    ports: ["5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]
volumes:
  pgdata:
```

### 2. Migration 3 bảng

`users`, `tenants`, `tenant_members` với PK UUID, unique email, unique `(tenant_id, user_id)`.

### 3. Layers

```text
handler/auth.go        → service/auth.go → repository/user.go
middleware/auth.go     → parse JWT, set context
```

### 4. Register flow (logic)

```text
validate email/password
→ hash password (bcrypt/argon2)
→ create user
→ create tenant name="{username}'s workspace"
→ create member role=owner
→ issue access + refresh token
```

### 5. Kiểm thử bằng tay

```bash
curl -s localhost:8080/health
curl -s -X POST localhost:8080/auth/register -H 'Content-Type: application/json' \
  -d '{"email":"a@example.com","password":"Secret123","username":"alice"}'
curl -s -X POST localhost:8080/auth/login -H 'Content-Type: application/json' \
  -d '{"email":"a@example.com","password":"Secret123"}'
curl -s localhost:8080/auth/me -H "Authorization: Bearer $TOKEN"
```

## Definition of Done

- [ ] Postgres lên bằng compose
- [ ] Register tạo user + tenant + membership owner
- [ ] Login trả JWT
- [ ] `/auth/me` 401 khi thiếu token
- [ ] README ngắn trong `app/` ghi cách chạy

## Tham chiếu WeKnora (đọc nhẹ)

- `internal/handler/auth.go` — shape request/response  
- `website-docs/03-features/01-tenant-auth.md` — mục đăng ký / login  

**Không** copy cả file — chỉ học flow.

## Sau lab

Commit: `feat: auth skeleton with personal tenant`

→ Phase 2: [`../02-rag-co-ban/README.md`](../02-rag-co-ban/README.md)
