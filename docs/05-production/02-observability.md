# 02 — Observability

## Ba trụ

| Trụ | MVP |
|-----|-----|
| Logs | JSON log + `request_id` + `tenant_id` + `user_id` |
| Metrics | Đếm request, latency, job fail (Prometheus optional) |
| Traces | Trace 1 chat/agent call (OpenTelemetry hoặc Langfuse) |

WeKnora tích hợp Langfuse cho bước agent / token.

## Event nên đo

- `ingest.duration_ms`, `embed.tokens`  
- `retrieve.hit_count`  
- `agent.steps`, `agent.tool_errors`  
- `authz.denied`  

## Không log

Password, API key plaintext, toàn bộ document content trên môi trường shared (PII).

## Tiếp

→ [03 — Bảo mật](./03-bao-mat.md)
