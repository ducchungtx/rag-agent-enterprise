from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.access.rbac import require_capability, require_role
from app.core.db import get_db
from app.core.security import safe_decode_token
from app.models.orm import APIKey, MemberRole, TenantMember, User
from app.services.apikey import resolve_api_key
from app.services.member import get_membership

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass
class AuthContext:
    user: User | None
    api_key: APIKey | None
    tenant_id: UUID | None
    role: MemberRole | None

    @property
    def actor_user_id(self) -> UUID | None:
        return self.user.id if self.user else None

    @property
    def actor_api_key_id(self) -> UUID | None:
        return self.api_key.id if self.api_key else None


def get_current_user_optional(
    db: Annotated[Session, Depends(get_db)],
    creds: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    x_api_key: Annotated[str | None, Header(alias="X-API-Key")] = None,
) -> AuthContext:
    if x_api_key:
        key = resolve_api_key(db, x_api_key)
        if not key:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid API Key")
        return AuthContext(user=None, api_key=key, tenant_id=key.tenant_id, role=None)

    if not creds:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing credentials")
    payload = safe_decode_token(creds.credentials)
    if not payload or "sub" not in payload:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    user = db.scalar(select(User).where(User.id == UUID(payload["sub"])))
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")
    return AuthContext(user=user, api_key=None, tenant_id=None, role=None)


def get_tenant_context(
    auth: Annotated[AuthContext, Depends(get_current_user_optional)],
    db: Annotated[Session, Depends(get_db)],
    x_tenant_id: Annotated[str | None, Header(alias="X-Tenant-Id")] = None,
) -> AuthContext:
    if auth.api_key:
        return auth
    if not x_tenant_id:
        # default to first membership
        if not auth.user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")
        memberships = list(
            db.scalars(
                select(TenantMember).where(TenantMember.user_id == auth.user.id)
            ).all()
        )
        if not memberships:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "No tenant membership")
        m = memberships[0]
        auth.tenant_id = m.tenant_id
        auth.role = m.role
        return auth

    tenant_id = UUID(x_tenant_id)
    if not auth.user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")
    m = get_membership(db, tenant_id, auth.user.id)
    if not m:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not a member of this tenant")
    auth.tenant_id = tenant_id
    auth.role = m.role
    return auth


def require_action(action: str):
    def _dep(ctx: Annotated[AuthContext, Depends(get_tenant_context)]) -> AuthContext:
        if ctx.api_key:
            require_capability(list(ctx.api_key.capabilities or []), action)
            return ctx
        if ctx.role is None:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Missing role")
        require_role(ctx.role, action)
        return ctx

    return _dep


def assert_kb_allowlist(ctx: AuthContext, kb_id: UUID) -> None:
    if not ctx.api_key:
        return
    allow = ctx.api_key.kb_allowlist
    if allow and kb_id not in allow:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "KB not in API Key allow-list")
