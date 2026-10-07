from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import AuthContext, require_action
from app.core.db import get_db
from app.models.schemas import APIKeyCreate, APIKeyOut, AuditOut
from app.models.orm import AuditLog
from app.services import apikey as apikey_service
from sqlalchemy import select

router = APIRouter(tags=["apikeys"])


@router.post("/api-keys", response_model=APIKeyOut)
def create_key(
    payload: APIKeyCreate,
    auth: Annotated[AuthContext, Depends(require_action("apikey.manage"))],
    db: Annotated[Session, Depends(get_db)],
) -> APIKeyOut:
    assert auth.tenant_id and auth.user
    try:
        row, raw = apikey_service.create_api_key(
            db,
            tenant_id=auth.tenant_id,
            name=payload.name,
            capabilities=payload.capabilities,
            kb_allowlist=payload.kb_allowlist,
            actor_user_id=auth.user.id,
        )
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    return APIKeyOut(
        id=row.id,
        name=row.name,
        key_prefix=row.key_prefix,
        capabilities=list(row.capabilities or []),
        kb_allowlist=list(row.kb_allowlist) if row.kb_allowlist else None,
        created_at=row.created_at,
        raw_key=raw,
    )


@router.get("/api-keys", response_model=list[APIKeyOut])
def list_keys(
    auth: Annotated[AuthContext, Depends(require_action("apikey.manage"))],
    db: Annotated[Session, Depends(get_db)],
) -> list[APIKeyOut]:
    assert auth.tenant_id
    rows = apikey_service.list_api_keys(db, auth.tenant_id)
    return [
        APIKeyOut(
            id=r.id,
            name=r.name,
            key_prefix=r.key_prefix,
            capabilities=list(r.capabilities or []),
            kb_allowlist=list(r.kb_allowlist) if r.kb_allowlist else None,
            created_at=r.created_at,
        )
        for r in rows
    ]


@router.delete("/api-keys/{key_id}", response_model=APIKeyOut)
def revoke_key(
    key_id: UUID,
    auth: Annotated[AuthContext, Depends(require_action("apikey.manage"))],
    db: Annotated[Session, Depends(get_db)],
) -> APIKeyOut:
    assert auth.tenant_id and auth.user
    try:
        row = apikey_service.revoke_api_key(db, auth.tenant_id, key_id, auth.user.id)
    except ValueError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    return APIKeyOut(
        id=row.id,
        name=row.name,
        key_prefix=row.key_prefix,
        capabilities=list(row.capabilities or []),
        kb_allowlist=list(row.kb_allowlist) if row.kb_allowlist else None,
        created_at=row.created_at,
    )


@router.get("/audit", response_model=list[AuditOut])
def list_audit(
    auth: Annotated[AuthContext, Depends(require_action("apikey.manage"))],
    db: Annotated[Session, Depends(get_db)],
) -> list[AuditOut]:
    assert auth.tenant_id
    rows = db.scalars(
        select(AuditLog)
        .where(AuditLog.tenant_id == auth.tenant_id)
        .order_by(AuditLog.created_at.desc())
        .limit(50)
    ).all()
    return [
        AuditOut(
            id=r.id,
            action=r.action,
            resource_type=r.resource_type,
            resource_id=r.resource_id,
            created_at=r.created_at,
        )
        for r in rows
    ]
