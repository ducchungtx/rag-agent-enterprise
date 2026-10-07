from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.orm import MemberRole, MemberStatus, Tenant, TenantMember, User
from app.models.schemas import LoginIn, RegisterIn, TokenOut
from app.services.audit import write_audit


def register_user(db: Session, payload: RegisterIn) -> tuple[User, Tenant, TokenOut]:
    existing = db.scalar(select(User).where(User.email == payload.email.lower()))
    if existing:
        raise ValueError("Email already registered")

    user = User(
        email=payload.email.lower(),
        username=payload.username,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.flush()

    tenant = Tenant(name=f"{payload.username}'s workspace")
    db.add(tenant)
    db.flush()

    member = TenantMember(
        tenant_id=tenant.id,
        user_id=user.id,
        role=MemberRole.owner,
        status=MemberStatus.active,
    )
    db.add(member)
    db.commit()
    db.refresh(user)
    db.refresh(tenant)

    write_audit(
        db,
        action="auth.register",
        resource_type="user",
        resource_id=str(user.id),
        tenant_id=tenant.id,
        actor_user_id=user.id,
    )
    token = TokenOut(access_token=create_access_token(user.id))
    return user, tenant, token


def login_user(db: Session, payload: LoginIn) -> TokenOut:
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise ValueError("Invalid email or password")
    return TokenOut(access_token=create_access_token(user.id))


def get_user_memberships(db: Session, user: User) -> list[TenantMember]:
    return list(
        db.scalars(
            select(TenantMember).where(
                TenantMember.user_id == user.id,
                TenantMember.status == MemberStatus.active,
            )
        ).all()
    )
