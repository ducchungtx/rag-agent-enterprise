from __future__ import annotations

from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import AuthContext, assert_kb_allowlist, require_action
from app.core.db import get_db
from app.services import chat as chat_service
from app.services import kb as kb_service
from app.services import retrieve as retrieve_service
from app.services.llm import LLMError

router = APIRouter(tags=["mcp"])

MCP_PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "rag-agent-enterprise-mcp"
SERVER_VERSION = "0.1.0"

TOOLS = [
    {
        "name": "list_knowledge_bases",
        "description": "List knowledge bases in current tenant (read-only).",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "search_knowledge",
        "description": "Hybrid search chunks in a KB. Requires kb_id and query.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "kb_id": {"type": "string", "description": "KB UUID"},
                "query": {"type": "string"},
                "top_k": {"type": "integer", "default": 5, "minimum": 1, "maximum": 20},
            },
            "required": ["kb_id", "query"],
        },
    },
    {
        "name": "answer_question",
        "description": "Answer a question with citations from a KB.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "kb_id": {"type": "string", "description": "KB UUID"},
                "question": {"type": "string"},
                "top_k": {"type": "integer", "default": 5, "minimum": 1, "maximum": 20},
            },
            "required": ["kb_id", "question"],
        },
    },
]


class MCPRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: Any = None
    method: str
    params: dict[str, Any] = {}


def _ok(req_id: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def _err(req_id: Any, code: int, message: str, data: Any = None) -> dict[str, Any]:
    err: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    return {"jsonrpc": "2.0", "id": req_id, "error": err}


@router.post("/mcp")
def mcp_endpoint(
    payload: MCPRequest,
    auth: Annotated[AuthContext, Depends(require_action("kb.search"))],
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, Any]:
    assert auth.tenant_id
    method = payload.method

    if method == "initialize":
        return _ok(
            payload.id,
            {
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                "capabilities": {"tools": {"listChanged": False}},
            },
        )
    if method in ("notifications/initialized", "notifications/cancelled"):
        return _ok(payload.id, {})
    if method == "tools/list":
        return _ok(payload.id, {"tools": TOOLS})

    if method == "tools/call":
        name = payload.params.get("name")
        args: dict[str, Any] = payload.params.get("arguments") or {}
        try:
            if name == "list_knowledge_bases":
                rows = kb_service.list_kbs(db, auth.tenant_id)
                items = [
                    {"id": str(k.id), "name": k.name, "description": k.description}
                    for k in rows
                ]
                return _ok(
                    payload.id,
                    {"content": [{"type": "text", "text": str(items)}], "structuredContent": {"kbs": items}},
                )
            if name in ("search_knowledge", "answer_question"):
                try:
                    kb_id = UUID(str(args.get("kb_id")))
                except (ValueError, AttributeError, TypeError):
                    return _err(payload.id, -32602, "Invalid kb_id")
                assert_kb_allowlist(auth, kb_id)
                if not kb_service.get_kb(db, auth.tenant_id, kb_id):
                    raise HTTPException(status.HTTP_404_NOT_FOUND, "KB not found")
                top_k = int(args.get("top_k", 5))
                top_k = max(1, min(20, top_k))
                if name == "search_knowledge":
                    results = retrieve_service.search_chunks(
                        db, tenant_id=auth.tenant_id, kb_id=kb_id,
                        query=str(args.get("query", "")), top_k=top_k,
                    )
                    items = [r.model_dump(mode="json") for r in results]
                    return _ok(
                        payload.id,
                        {"content": [{"type": "text", "text": str(items)}], "structuredContent": {"results": items}},
                    )
                out = chat_service.answer_question(
                    db, tenant_id=auth.tenant_id, kb_id=kb_id,
                    question=str(args.get("question", "")), top_k=top_k,
                )
                data = out.model_dump(mode="json")
                return _ok(
                    payload.id,
                    {"content": [{"type": "text", "text": out.answer}], "structuredContent": data},
                )
            return _err(payload.id, -32601, f"Unknown tool: {name}")
        except HTTPException as exc:
            return _err(payload.id, -32000, f"HTTP {exc.status_code}: {exc.detail}")
        except LLMError as exc:
            return _err(payload.id, -32000, str(exc))
        except Exception as exc:  # noqa: BLE001
            return _err(payload.id, -32603, f"Internal error: {exc}")

    return _err(payload.id, -32601, f"Method not found: {method}")
