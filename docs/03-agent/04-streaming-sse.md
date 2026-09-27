# 04 — Streaming SSE

## Vì sao SSE?

Agent chạy lâu — UX cần token / tool event realtime. WeKnora dùng SSE + StreamManager (memory/Redis) để resume.

## Event tối thiểu

```text
event: meta
data: {"session_id":"...","message_id":"..."}

event: thinking
data: {"content":"..."}

event: tool_call
data: {"name":"search_knowledge","input":{...}}

event: tool_result
data: {"name":"search_knowledge","ok":true,"preview":"..."}

event: answer
data: {"content":"token hoặc đoạn"}

event: done
data: {"ok":true}
```

Hoặc NDJSON một dòng/JSON như CLI WeKnora (`type` field).

## Endpoint

`POST /sessions/:id/agent-chat`  
Headers: `Accept: text/event-stream`  
Response: flush từng event; disable proxy buffer nếu có nginx.

## Resume (học ý, code sau)

WeKnora `session resume` replay từ đầu — client phải **dedupe**. MVP có thể bỏ resume.

## Tiếp

→ [05 — Lab Mini Agent](./05-lab-mini-agent.md)
