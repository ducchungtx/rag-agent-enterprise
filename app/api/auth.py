from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import AuthContext, get_current_user_optional
from app.core.db import get_db
from app.models.schemas import LoginIn, MembershipOut, RegisterIn, TokenOut, UserOut
from app.services import auth as auth_service
from app.services.tenant import get_tenant

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenOut)
def register(payload: RegisterIn, db: Annotated[Session, Depends(get_db)]) -> TokenOut:
    try:
        _, _, token = auth_service.register_user(db, payload)
        return token
    except ValueError as exc:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(exc)) from exc


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Annotated[Session, Depends(get_db)]) -> TokenOut:
    try:
        return auth_service.login_user(db, payload)
    except ValueError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(exc)) from exc


@router.get("/me", response_model=UserOut)
def me(
    auth: Annotated[AuthContext, Depends(get_current_user_optional)],
    db: Annotated[Session, Depends(get_db)],
) -> UserOut:
    if not auth.user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "JWT required")
    memberships = auth_service.get_user_memberships(db, auth.user)
    out = []
    for m in memberships:
        t = get_tenant(db, m.tenant_id)
        if t:
            out.append(
                MembershipOut(
                    tenant_id=m.tenant_id,
                    tenant_name=t.name,
                    role=m.role,
                    status=m.status.value,
                )
            )
    return UserOut(
        id=auth.user.id,
        email=auth.user.email,
        username=auth.user.username,
        memberships=out,
    )
