# 02 — Chunking & Embedding

## Chunking đơn giản (đủ cho MVP)

| Tham số | Gợi ý ban đầu |
|---------|----------------|
| `chunk_size` | 500–800 tokens (hoặc ~1200–2000 ký tự) |
| `overlap` | 10–15% |
| Strategy | Cắt theo đoạn văn (`\n\n`) rồi gộp đến gần `chunk_size` |

Chưa cần parent-child như WeKnora. Khi citation kém, hãy quay lại tinh chỉnh.

## Schema chunk

```text
chunks (
  id, document_id, kb_id, tenant_id,  -- tenant_id denormalize để filter nhanh
  position, content,
  embedding vector(dim),
  token_count, created_at
)
```

Index:

```sql
CREATE INDEX ON chunks USING ivfflat (embedding vector_cosine_ops); -- hoặc hnsw
CREATE INDEX ON chunks (kb_id);
CREATE INDEX ON chunks (tenant_id, kb_id);
```

`dim` phụ thuộc model (ví dụ 768 / 1024 / 1536). **Cố định** từ đầu trong config.

## Embedding

- Gọi API OpenAI-compatible: `POST /v1/embeddings`
- Batch 16–64 chunk/lần
- Lưu nguyên vector; không quantize ở MVP

## Metadata nên giữ

| Field | Lý do |
|-------|-------|
| `document_id` | Citation + ACL theo document |
| `kb_id` | Search scope |
| `position` | Sắp xếp / context window |
| `source_title` | Hiển thị UI |

## Sai lầm thường gặp

- Chunk quá lớn → retrieval nhiễu, tốn context  
- Chunk quá nhỏ → mất ngữ cảnh câu trả lời  
- Không lưu `tenant_id` trên chunk → query chậm hoặc dễ sót filter  

## Tiếp

→ [03 — Hybrid search](./03-hybrid-search.md)
