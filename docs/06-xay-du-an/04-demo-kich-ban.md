# 04 — Kịch bản demo Phase 6 (Pháp chế / Luật Đất đai)

Sau khi backend MVP (Phase 1–5) chạy được, bước **dự án thật** là gắn một domain cụ thể: corpus, tenant mẫu, và kịch bản demo có thể lặp lại.

## Chuẩn bị

1. Postgres + Redis (nếu async ingest): `make up`
2. DB: `make db`
3. API: `make run` (cổng 8000)
4. Corpus lab: [`data/docs/`](../../data/docs/) — gồm tóm tắt Luật 2024 (thời hạn, chuyển mục đích), NĐ 88/102, FAQ + chính sách nội bộ

## Chạy một lệnh

```bash
make demo-phap-che
```

Script [`scripts/demo_phap_che.sh`](../../scripts/demo_phap_che.sh) thực hiện:

| Bước | Hành vi | Khớp tiêu chí MVP |
|------|---------|-------------------|
| 1 | Lead tạo tenant `Phòng Pháp chế` | Blueprint §3 |
| 2 | KB `Luật Đất đai + Policy` + upload 2 file `.md` | Ingest + citation |
| 3 | Search + chat câu hỏi điển hình | RAG |
| 4 | Mời Viewer — chat OK, upload 403 | RBAC |
| 5 | User tenant khác chat → 404 | Isolation |

## Tự demo tay (Swagger)

1. `POST /auth/register` → lấy JWT  
2. `POST /tenants` body `{"name":"Phòng Pháp chế"}` → lấy `tenant_id`  
3. Mọi request nghiệp vụ: header `X-Tenant-Id`  
4. `POST /kb` → upload từng file trong `data/docs/`  
5. `POST /chat` với câu hỏi ví dụ:
   - *"Thời hạn sử dụng đất nông nghiệp của cá nhân trực tiếp sản xuất là bao lâu?"*
   - *"Đất ở có phải thời hạn 50 năm không?"*
   - *"Nghị định nào quy định bồi thường, hỗ trợ, tái định cư khi thu hồi đất?"*
   - *"Hồ sơ chuyển mục đích nội bộ cần những giấy tờ gì?"*

## Mở rộng corpus (tài liệu thật)

1. Đặt file `.doc` / `.pdf` vào thư mục riêng (không commit nếu mật).  
2. Convert sang `.txt` hoặc `.md` (LibreOffice, pandoc).  
3. Upload qua `POST /kb/{id}/documents` hoặc chỉnh `scripts/ingest_sample.sh`:

```bash
bash scripts/ingest_sample.sh data/docs/tom-tat-quy-dinh-su-dung-dat-lab.md
```

4. Bật `USE_ASYNC_INGEST=true` + worker khi file lớn: `make worker`

## Checklist “xong Phase 6 lab”

- [x] Chạy demo / ingest corpus pass trên máy lab  
- [x] ≥ 2 câu hỏi domain có `citations[]` (đất ở / NĐ 88 / 50 năm)  
- [x] LLM thật (Mistral chat + embed) — không còn phụ thuộc `fake` chat  
- [ ] (Tuỳ chọn) Thêm 1 tenant thứ hai với KB khác để demo isolation rõ hơn  
- [ ] (Tuỳ chọn) So sánh Gemini  
- [x] M5.1 UI tối thiểu (`/ui`)  

## Demo UI (M5.1)

1. API chạy: `make run` (cổng 8000)  
2. Mở http://127.0.0.1:8000/ui  
3. Register → tạo/chọn tenant → tạo KB → upload 1 file trong `data/docs/`  
4. Chat câu domain → xem citation; hoặc Agent (SSE)  

Khi đổi `EMBEDDING_DIM`: `make db-reset` rồi ingest lại (mất data lab).

## Liên kết

- Blueprint: [01-blueprint.md](./01-blueprint.md)  
- Milestone M5 (UI, OIDC…): [02-milestone.md](./02-milestone.md)
