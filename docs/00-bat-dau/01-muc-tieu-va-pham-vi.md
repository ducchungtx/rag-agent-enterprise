# 01 — Mục tiêu và phạm vi

## Bạn đang xây gì?

Một **Agent AI nội bộ doanh nghiệp** với các đặc tính tối thiểu:

| # | Năng lực | Mô tả ngắn |
|---|----------|------------|
| 1 | Đa không gian (multi-tenant) | Mỗi team có workspace riêng; dữ liệu không lẫn nhau |
| 2 | Phân quyền RBAC | 4 vai trò: Owner / Admin / Contributor / Viewer |
| 3 | Kho kiến thức | Upload tài liệu → parse → chunk → embed → tìm kiếm |
| 4 | Hỏi đáp RAG | Trả lời kèm citation từ KB được phép xem |
| 5 | Agent có tools | Ít nhất: `search_knowledge`, `read_document` |
| 6 | API Key máy | Chương trình gọi API với scope (retrieve / qa / ingest) |

Đây chính là “xương sống” WeKnora rút gọn — **không** cần Wiki, IM, sandbox, BrowserSkill ở MVP.

## Phạm vi MVP (làm)

- Auth: đăng ký / đăng nhập JWT + refresh (OIDC để sau)
- Workspace + invite thành viên + đổi role
- CRUD Knowledge Base trong phạm vi workspace
- Upload file `.md` / `.txt` / `.pdf` (PDF có thể phase sau)
- Pipeline: lưu file → chunk → embed → lưu vector
- Chat: RAG sync trước, SSE sau
- Agent mode đơn giản (ReAct 1–N bước)
- Middleware: Auth → Tenant context → RBAC
- Audit log cơ bản (ai làm gì trên resource nào)

## Ngoài phạm vi MVP (chưa làm)

- Wiki tự sinh, Knowledge Graph / Neo4j
- Sandbox / Skills / MCP đầy đủ
- IM (Slack, Feishu…), Embed widget
- Multi-vector-backend (chỉ pgvector)
- Desktop / Lite binary
- GraphRAG, parent-child chunking nâng cao

## Tiêu chí “xong MVP”

Bạn demo được kịch bản sau:

1. User A tạo workspace `Phòng Pháp chế`, mời User B với role **Viewer**.
2. A upload hợp đồng mẫu vào KB; B hỏi được nội dung, **không** upload được (403).
3. A tạo API Key chỉ `retrieve` — key đó chat QA bị từ chối.
4. User C ở workspace khác **không** thấy KB của A.

## Cách học hiệu quả

1. Đọc lý thuyết trong phase → đọc file WeKnora được chỉ định (chỉ những file đó).  
2. Làm lab bằng tay (code trong repo này, không fork nguyên WeKnora).  
3. Mỗi lab kết thúc bằng checklist + 3 câu tự kiểm.  
4. Không nhảy cóc Phase 4 (RBAC) trước khi RAG chạy — dễ rối isolation.

## Liên kết tiếp

→ [02 — Bản đồ học tập](./02-ban-do-hoc-tap.md)
