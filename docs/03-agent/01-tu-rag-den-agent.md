# 01 — Từ RAG đến Agent

## Khác nhau cốt lõi

| | RAG Q&A | Agent |
|---|---------|-------|
| Lộ trình | Cố định: search → prompt → answer | Động: model chọn tool / dừng |
| Số bước | 1 lần retrieve | Nhiều vòng think–act–observe |
| Phù hợp | Câu hỏi tra cứu | Nhiệm vụ (“so sánh 2 tài liệu”, “tìm rồi tóm tắt”) |

WeKnora UI: **Quick Q&A** vs **Smart reasoning**.

## Khi nào dùng Agent trong sản phẩm doanh nghiệp

- Cần đọc nhiều document tuần tự  
- Cần tool ngoài KB (calendar, ticket) — Phase sau  
- Cần giải thích từng bước cho audit  

Khi câu hỏi đơn giản → để RAG thẳng (rẻ hơn, ổn định hơn).

## Thành phần runtime

```text
AgentRuntime
  ├── Planner / LLM (tool calling)
  ├── ToolRegistry
  ├── Memory (transcript vòng hiện tại)
  ├── PermissionChecker  ← quan trọng: tool cũng phải ACL
  └── EventEmitter (SSE)
```

## Ràng buộc doanh nghiệp

Agent **không** được bypass RBAC.  
`search_knowledge` chỉ search KB user được phép.  
Tool nguy hiểm (delete, gửi email) cần approval — WeKnora có human-in-the-loop cho MCP.

## Tiếp

→ [02 — Vòng ReAct](./02-react-loop.md)
