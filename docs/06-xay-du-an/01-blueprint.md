# 01 — Blueprint sản phẩm

Điền trước khi code thêm feature “cho vui”.

## 1. Bài toán

| Câu hỏi | Trả lời của bạn |
|---------|-----------------|
| Ai dùng? | (vd. HR BP, nhân viên) |
| Câu hỏi điển hình? | |
| Tài liệu nguồn? | (Confluence / PDF / Drive) |
| Rủi ro nếu trả lời sai? | |
| Cần audit không? | |

## 2. Phạm vi v1

Sao chép từ Phase 0 MVP rồi **gạch** thứ không cần (Agent? API Key? Chỉ RAG?).

## 3. Mô hình quyền

Vẽ bảng: phòng ban → tenant nào → role mặc định → KB nào.

## 4. Kiến trúc chọn

- Stack (Go/Python)  
- Model chat + embed  
- Sync hay async ingest  
- Có UI hay API-only  

## 5. Map module → thư mục

```text
auth | tenant | kb | ingest | retrieve | chat | agent | apikey | audit
```

## 6. Phi chức năng

| Chỉ tiêu | Mục tiêu |
|----------|----------|
| Latency chat P95 | (vd. < 5s với RAG) |
| Documents / tenant | |
| Concurrent users | |

## Tham chiếu tinh thần WeKnora

Đừng cố bằng feature Wiki/Sandbox ngay. WeKnora mất nhiều version mới đủ — bạn ship xương sống trước.
