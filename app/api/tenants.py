from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import AuthContext, get_current_user_optional, get_tenant_context, require_action
from app.core.db import get_db
from app.models.schemas import (
    InviteIn,
    MemberOut,
    RolePatch,
    TenantCreate,
    TenantOut,
)
from app.services import member as member_service
from app.services import tenant as tenant_service

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.post("", response_model=TenantOut)
def create_tenant(
    payload: TenantCreate,
    auth: Annotated[AuthContext, Depends(get_current_user_optional)],
    db: Annotated[Session, Depends(get_db)],
) -> TenantOut:
    if not auth.user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "JWT required")
    t = tenant_service.create_tenant(db, name=payload.name, owner=auth.user)
    return TenantOut(id=t.id, name=t.name, created_at=t.created_at)


@router.get("", response_model=list[TenantOut])
def list_tenants(
    auth: Annotated[AuthContext, Depends(get_current_user_optional)],
    db: Annotated[Session, Depends(get_db)],
) -> list[TenantOut]:
    if not auth.user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "JWT required")
    rows = tenant_service.list_tenants_for_user(db, auth.user.id)
    return [TenantOut(id=t.id, name=t.name, created_at=t.created_at) for t in rows]


@router.get("/{tenant_id}/members", response_model=list[MemberOut])
def list_members(
    tenant_id: UUID,
    auth: Annotated[AuthContext, Depends(get_tenant_context)],
    db: Annotated[Session, Depends(get_db)],
) -> list[MemberOut]:
    if auth.tenant_id != tenant_id and not auth.api_key:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Tenant mismatch")
    rows = member_service.list_members(db, tenant_id)
    return [
        MemberOut(
            user_id=u.id,
            email=u.email,
            username=u.username,
            role=m.role,
            status=m.status.value,
        )
        for m, u in rows
    ]


@router.post("/{tenant_id}/members/invite", response_model=MemberOut)
def invite(
    tenant_id: UUID,
    payload: InviteIn,
    auth: Annotated[AuthContext, Depends(require_action("member.invite"))],
    db: Annotated[Session, Depends(get_db)],
) -> MemberOut:
    if auth.tenant_id != tenant_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Tenant mismatch")
    actor = auth.actor_user_id or (auth.api_key.created_by if auth.api_key else None)
    if actor is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "No actor")
    try:
        m = member_service.invite_member(
            db,
            tenant_id=tenant_id,
            email=payload.email,
            role=payload.role,
            actor_user_id=actor,
        )
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    user = next(u for mm, u in member_service.list_members(db, tenant_id) if mm.id == m.id)
    return MemberOut(
        user_id=user.id,
        email=user.email,
        username=user.username,
        role=m.role,
        status=m.status.value,
    )


@router.patch("/{tenant_id}/members/{user_id}", response_model=MemberOut)
def patch_role(
    tenant_id: UUID,
    user_id: UUID,
    payload: RolePatch,
    auth: Annotated[AuthContext, Depends(require_action("member.role"))],
    db: Annotated[Session, Depends(get_db)],
) -> MemberOut:
    if auth.tenant_id != tenant_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Tenant mismatch")
    try:
        m = member_service.update_role(
            db,
            tenant_id=tenant_id,
            user_id=user_id,
            role=payload.role,
            actor_user_id=auth.actor_user_id,  # type: ignore[arg-type]
        )
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc
    user = next(u for mm, u in member_service.list_members(db, tenant_id) if u.id == user_id)
    return MemberOut(
        user_id=user.id,
        email=user.email,
        username=user.username,
        role=m.role,
        status=m.status.value,
    )
