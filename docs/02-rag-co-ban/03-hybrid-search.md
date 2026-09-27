# 03 — Hybrid search

## Mục tiêu

Cho query → top-K chunk **trong đúng KB + đúng tenant**.

## Vector search (bắt buộc)

```text
embed(query) → cosine similarity trên chunks
WHERE tenant_id = ? AND kb_id = ? 
ORDER BY embedding <=> $1 LIMIT K
```

## Keyword search (nên có sớm)

Postgres `tsvector` / `ILIKE` trên `content`. Hợp từ khóa mã số, tên riêng — chỗ vector hay trượt.

## Fusion đơn giản

1. Lấy top `K` vector + top `K` keyword  
2. RRF (Reciprocal Rank Fusion) hoặc điểm chuẩn hóa alpha  
3. Trả top `N` (thường 5–10) trước khi đưa vào LLM  

WeKnora có rerank model — bạn thêm sau khi baseline ổn.

## API

`POST /knowledge-bases/:id/search`

```json
{
  "query": "thời hạn bảo hành",
  "top_k": 8
}
```

Response:

```json
{
  "ok": true,
  "data": [
    {
      "chunk_id": "...",
      "document_id": "...",
      "content": "...",
      "score": 0.82,
      "document_title": "HD-BH.md"
    }
  ]
}
```

## Isolation test (bắt buộc)

Tạo 2 tenant, 2 KB nội dung khác nhau — user A search **không** ra chunk của B kể cả đoán được UUID.

## Tiếp

→ [04 — QA có citation](./04-qa-citation.md)
