# 03 — Tools và MCP

## Bộ tool MVP (bám WeKnora v0.8)

| Tool | Input | Việc |
|------|-------|------|
| `search_knowledge` | `query`, `kb_ids[]?`, `top_k?` | Hybrid search có ACL |
| `read_document` | `document_id` | Đọc full text / đoạn |
| `list_documents` | `kb_id` | Liệt kê tài liệu trong KB |

WeKnora gộp retrieval tools thành bộ này — đừng invent 10 tool trùng chức năng.

## Contract tool

Mỗi tool:

1. `Name`, `Description`, JSON Schema parameters  
2. `Execute(ctx, args) (any, error)`  
3. Bên trong **luôn** đọc `tenant_id` / role từ context  

## MCP — học khái niệm, implement sau

| Hướng | Ý nghĩa |
|-------|---------|
| App là MCP **client** | Agent gọi tool từ server ngoài (GitHub, DB…) |
| App là MCP **server** | Cursor/Claude gọi vào KB của bạn |

WeKnora: built-in MCP server per-workspace + CLI `weknora mcp serve` (read-only curated).  
MVP Phase 3: **chưa** cần MCP — chỉ in-process tools. Ghi chú vào backlog Phase 6.

## Approval (ý tưởng)

Với tool `destructiveHint=true` → emit event `approval_required`, đợi user.  
CLI WeKnora exit 10 tương tự tinh thần “không auto-yes”.

## Tiếp

→ [04 — Streaming SSE](./04-streaming-sse.md)
