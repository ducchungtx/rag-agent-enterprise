# 05 — Lab: Mini RAG

## Mục tiêu

End-to-end trên **một** tenant (RBAC tinh chỉnh để Phase 4):

1. Tạo KB  
2. Upload `sample.md`  
3. `POST /search` ra chunk đúng  
4. `POST /chat` trả lời có citation  

## Dữ liệu mẫu

Tạo `testdata/sample-policy.md` (~30–50 dòng) với vài sự thật rõ ràng (số ngày nghỉ, hạn bảo hành…).

## Việc cần code

| Module | Chức năng |
|--------|-----------|
| `service/kb.go` | CRUD KB theo tenant |
| `service/ingest.go` | Save file → chunk → embed |
| `service/retrieve.go` | Vector search |
| `service/chat.go` | Prompt + LLM + citations |
| Handlers tương ứng | Wire routes |

Tạm thời: mọi member trong tenant đều CRUD (sẽ siết role ở Phase 4).

## Kiểm thử

```bash
# tạo KB, upload, search, chat — lưu script scripts/smoke_rag.sh
```

Kịch bản fail bắt buộc:

- Chat KB trống → trả “không có dữ liệu” (không ảo giác)  
- Document `failed` không vào search  

## Definition of Done

- [ ] Ít nhất 1 document `completed` với N chunks > 0  
- [ ] Search trả về đoạn chứa đúng keyword bạn cài trong sample  
- [ ] Chat mention được sự thật trong sample + citation  
- [ ] Mọi query có filter `tenant_id`

## Tham chiếu WeKnora

- `website-docs/02-architecture/03-document-pipeline.md`  
- `website-docs/02-architecture/04-rag-pipeline.md`  
- `internal/agent/tools/search_knowledge.go` (shape tool — đọc ý)

## Sau lab

→ Phase 3: [`../03-agent/README.md`](../03-agent/README.md)
