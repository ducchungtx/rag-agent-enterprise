# 01 — Hàng đợi bất đồng bộ

## Vì sao cần

Embed 100 trang PDF trong HTTP request → timeout, UX tệ. WeKnora: Asynq + nhiều worker pool.

## Mô hình

```text
Handler: tạo Document(pending) → Enqueue("document:process", {doc_id})
Worker:  parse → chunk → embed → completed | failed
API:     GET document → client poll status (hoặc websocket sau)
```

## MVP queue

| Stack | Gợi ý |
|-------|--------|
| Go | Redis + Asynq |
| Python | Redis + RQ / ARQ / Celery |

Retry: exponential backoff, DLQ hoặc `failed` + nút reparse.

## Tách queue (học từ WeKnora)

- `default` — parse + index  
- `enrichment` — summary (sau)  
Đừng để job nặng chặn job nhẹ nếu scale.

## Tiếp

→ [02 — Observability](./02-observability.md)
