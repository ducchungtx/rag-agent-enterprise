# 01 — Blueprint sản phẩm

Đã điền cho domain học: **Pháp chế / Luật Đất đai** (corpus trong `data/docs`).

## 1. Bài toán

| Câu hỏi | Trả lời |
|---------|---------|
| Ai dùng? | Chuyên viên pháp chế, nhân viên liên quan đất đai nội bộ |
| Câu hỏi điển hình? | “Nghị định X quy định gì về …?”, “Thời hạn / điều kiện …?” |
| Tài liệu nguồn? | Nghị định / Thông tư (`.doc`) + chính sách nội bộ `.md` |
| Rủi ro nếu trả lời sai? | Cao — luôn kèm citation; không bịa khi thiếu nguồn |
| Cần audit không? | Có — upload, invite, API key, role change |

## 2. Phạm vi v1

- Multi-tenant workspace + RBAC 4 cấp  
- KB upload md/txt/pdf → chunk → embed → search/chat citation  
- Agent ReAct tối giản + SSE  
- API Key scoped (`retrieve`/`qa`/`ingest`/`admin`)  
- Async ingest (Redis RQ) khi `USE_ASYNC_INGEST=true`  

**Gạch (chưa làm):** Wiki, GraphRAG, sandbox/skills, IM, OIDC, UI đầy đủ.

## 3. Mô hình quyền

| Phòng ban | Tenant | Role mặc định | KB |
|-----------|--------|---------------|-----|
| Pháp chế | `Phòng Pháp chế` | Owner: lead; Viewer: nhân viên | Luật Đất đai + Policy |
| Team khác | Tenant riêng | Owner riêng | Không thấy KB Pháp chế |

## 4. Kiến trúc chọn

- Stack: **Python / FastAPI / SQLAlchemy / PostgreSQL+pgvector**  
- Model: fake (lab) hoặc OpenAI-compatible / Ollama  
- Ingest: sync mặc định; async qua Redis RQ (Phase 5)  
- UI: API-only + Swagger (MVP)

## 5. Map module → thư mục

```text
auth      → app/api/auth.py, app/services/auth.py
tenant    → app/api/tenants.py, app/services/tenant.py
kb        → app/api/kb.py, app/services/kb.py
ingest    → app/services/ingest.py, app/services/queue.py
retrieve  → app/services/retrieve.py
chat      → app/services/chat.py
agent     → app/services/agent.py, app/api/rag.py
apikey    → app/api/apikeys.py, app/services/apikey.py
audit     → app/services/audit.py
access    → app/access/rbac.py, app/api/deps.py
```

## 6. Phi chức năng

| Chỉ tiêu | Mục tiêu |
|----------|----------|
| Latency chat P95 | < 5s (fake/local); phụ thuộc LLM khi openai |
| Documents / tenant | Hàng trăm (MVP lab) |
| Concurrent users | Dev single-instance |
