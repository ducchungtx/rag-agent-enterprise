# 05 — Lab: Mini Agent

## Mục tiêu

`POST /agent/chat` với body `{ "kb_id", "question" }`:

- Model được schema 3 tools  
- Tự gọi `search_knowledge` ít nhất 1 lần trên câu hỏi cần tra cứu  
- Stream SSE (hoặc NDJSON) về client  
- Tool tôn trọng `tenant_id`

## Gợi ý triển khai

1. Dùng model hỗ trợ tool calling (OpenAI API / Qwen / GPT…). Ollama: chọn model có tools.  
2. Nếu local khó tool-calling: **fallback router** rule-based (“nếu hỏi về KB → luôn search rồi trả lời”) — vẫn học được vòng lặp, đổi LLM sau.  
3. Viết `ToolRegistry` interface sạch — dễ test fake tools.

## Kiểm thử

| Case | Kỳ vọng |
|------|---------|
| “Theo tài liệu, bảo hành bao lâu?” | Có `tool_call` search |
| KB trống | Agent nói không có nguồn |
| `document_id` tenant khác | Tool error forbidden, không leak nội dung |

## Definition of Done

- [ ] Ít nhất 2 tools chạy được  
- [ ] Log/event thấy vòng think–act  
- [ ] `max_steps` cắt được vòng lặp vô hạn  
- [ ] Cùng ACL với RAG search  

## Tham chiếu WeKnora

- `internal/agent/`  
- `internal/agent/tools/search_knowledge.go`  
- `cli/AGENTS.md` (NDJSON events)

## Sau lab

→ Phase 4 (trọng tâm): [`../04-phan-quyen/README.md`](../04-phan-quyen/README.md)
