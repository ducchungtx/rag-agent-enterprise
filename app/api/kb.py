from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import AuthContext, assert_kb_allowlist, get_tenant_context, require_action
from app.core.db import get_db
from app.models.schemas import DocumentOut, KBCreate, KBOut
from app.services import ingest as ingest_service
from app.services import kb as kb_service
from app.services.queue import enqueue_ingest

router = APIRouter(tags=["knowledge"])


@router.post("/kb", response_model=KBOut)
def create_kb(
    payload: KBCreate,
    auth: Annotated[AuthContext, Depends(require_action("kb.create"))],
    db: Annotated[Session, Depends(get_db)],
) -> KBOut:
    assert auth.tenant_id
    from app.models.orm import User
    from sqlalchemy import select

    if auth.user:
        owner = auth.user
    elif auth.api_key:
        owner = db.scalar(select(User).where(User.id == auth.api_key.created_by))
        if not owner:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "API Key owner missing")
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")
    kb = kb_service.create_kb(
        db,
        tenant_id=auth.tenant_id,
        owner=owner,
        name=payload.name,
        description=payload.description,
    )
    return KBOut(
        id=kb.id,
        tenant_id=kb.tenant_id,
        owner_user_id=kb.owner_user_id,
        name=kb.name,
        description=kb.description,
        created_at=kb.created_at,
    )


@router.get("/kb", response_model=list[KBOut])
def list_kb(
    auth: Annotated[AuthContext, Depends(require_action("kb.read"))],
    db: Annotated[Session, Depends(get_db)],
) -> list[KBOut]:
    assert auth.tenant_id
    rows = kb_service.list_kbs(db, auth.tenant_id)
    return [
        KBOut(
            id=k.id,
            tenant_id=k.tenant_id,
            owner_user_id=k.owner_user_id,
            name=k.name,
            description=k.description,
            created_at=k.created_at,
        )
        for k in rows
    ]


@router.post("/kb/{kb_id}/documents", response_model=DocumentOut)
async def upload_document(
    kb_id: UUID,
    auth: Annotated[AuthContext, Depends(require_action("kb.upload"))],
    db: Annotated[Session, Depends(get_db)],
    file: UploadFile = File(...),
    title: str | None = Form(default=None),
) -> DocumentOut:
    assert auth.tenant_id
    assert_kb_allowlist(auth, kb_id)
    kb = kb_service.get_kb(db, auth.tenant_id, kb_id)
    if not kb:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "KB not found")

    suffix = Path(file.filename or "upload.txt").suffix or ".txt"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = Path(tmp.name)

    actor = auth.actor_user_id
    if actor is None and auth.api_key:
        actor = auth.api_key.created_by
    assert actor

    doc = ingest_service.create_document_record(
        db,
        tenant_id=auth.tenant_id,
        kb_id=kb_id,
        title=title or (file.filename or "untitled"),
        src_path=tmp_path,
        user_id=actor,
    )
    enqueue_ingest(doc.id)
    db.refresh(doc)
    return DocumentOut(
        id=doc.id,
        kb_id=doc.kb_id,
        tenant_id=doc.tenant_id,
        title=doc.title,
        parse_status=doc.parse_status,
        error_message=doc.error_message,
        created_at=doc.created_at,
    )


@router.get("/documents/{document_id}", response_model=DocumentOut)
def get_document(
    document_id: UUID,
    auth: Annotated[AuthContext, Depends(require_action("kb.read"))],
    db: Annotated[Session, Depends(get_db)],
) -> DocumentOut:
    assert auth.tenant_id
    doc = ingest_service.get_document(db, auth.tenant_id, document_id)
    if not doc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")
    return DocumentOut(
        id=doc.id,
        kb_id=doc.kb_id,
        tenant_id=doc.tenant_id,
        title=doc.title,
        parse_status=doc.parse_status,
        error_message=doc.error_message,
        created_at=doc.created_at,
    )
