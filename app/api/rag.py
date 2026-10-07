from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import AuthContext, assert_kb_allowlist, require_action
from app.core.db import get_db
from app.models.schemas import AgentChatIn, ChatIn, ChatOut, SearchIn, SearchOut
from app.services import agent as agent_service
from app.services import chat as chat_service
from app.services import kb as kb_service
from app.services import retrieve as retrieve_service
from app.services.llm import LLMError

router = APIRouter(tags=["rag"])


@router.post("/search", response_model=SearchOut)
def search(
    payload: SearchIn,
    auth: Annotated[AuthContext, Depends(require_action("kb.search"))],
    db: Annotated[Session, Depends(get_db)],
) -> SearchOut:
    assert auth.tenant_id
    assert_kb_allowlist(auth, payload.kb_id)
    if not kb_service.get_kb(db, auth.tenant_id, payload.kb_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "KB not found")
    results = retrieve_service.search_chunks(
        db,
        tenant_id=auth.tenant_id,
        kb_id=payload.kb_id,
        query=payload.query,
        top_k=payload.top_k,
    )
    return SearchOut(results=results)


@router.post("/chat", response_model=ChatOut)
def chat(
    payload: ChatIn,
    auth: Annotated[AuthContext, Depends(require_action("kb.chat"))],
    db: Annotated[Session, Depends(get_db)],
) -> ChatOut:
    assert auth.tenant_id
    assert_kb_allowlist(auth, payload.kb_id)
    if not kb_service.get_kb(db, auth.tenant_id, payload.kb_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "KB not found")
    try:
        return chat_service.answer_question(
            db,
            tenant_id=auth.tenant_id,
            kb_id=payload.kb_id,
            question=payload.question,
            top_k=payload.top_k,
        )
    except LLMError as exc:
        code = status.HTTP_429_TOO_MANY_REQUESTS if exc.status_code == 429 else status.HTTP_502_BAD_GATEWAY
        raise HTTPException(code, str(exc)) from exc


@router.post("/agent/chat")
def agent_chat(
    payload: AgentChatIn,
    auth: Annotated[AuthContext, Depends(require_action("kb.chat"))],
    db: Annotated[Session, Depends(get_db)],
) -> StreamingResponse:
    assert auth.tenant_id
    assert_kb_allowlist(auth, payload.kb_id)
    if not kb_service.get_kb(db, auth.tenant_id, payload.kb_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "KB not found")

    def event_stream():
        for ev in agent_service.run_agent_events(
            db,
            tenant_id=auth.tenant_id,  # type: ignore[arg-type]
            kb_id=payload.kb_id,
            question=payload.question,
            max_steps=payload.max_steps,
        ):
            yield ev.sse()

    return StreamingResponse(event_stream(), media_type="text/event-stream")
