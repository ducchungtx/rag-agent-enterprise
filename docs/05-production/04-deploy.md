# 04 — Deploy

## Compose mục tiêu

```text
services: api, worker, postgres, redis, (ollama optional)
```

Healthcheck: `/health` + migrate on start (hoặc job migrate riêng).

## Môi trường

| Env | Khác biệt |
|-----|-----------|
| `dev` | Hot reload, verbose log |
| `staging` | Giống prod, model rẻ |
| `prod` | Private network, backup DB, không expose Postgres |

## WeKnora tham chiếu

- `docker-compose.yml` + profiles  
- `docs/LITE.md` — biến thể single binary khi học xong  

## Definition of Done Phase 5

- [ ] `docker compose up` chạy api+worker+db  
- [ ] Upload lớn không block HTTP  
- [ ] Có tài liệu `DEPLOY.md` 1 trang  

## Sau phase

→ Phase 6: [`../06-xay-du-an/README.md`](../06-xay-du-an/README.md)
