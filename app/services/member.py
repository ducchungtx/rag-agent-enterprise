from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.orm import MemberRole, MemberStatus, TenantMember, User
from app.services.audit import write_audit


def invite_member(
    db: Session,
    *,
    tenant_id: UUID,
    email: str,
    role: MemberRole,
    actor_user_id: UUID,
) -> TenantMember:
    if role == MemberRole.owner:
        raise ValueError("Cannot invite as owner; transfer ownership separately")
    user = db.scalar(select(User).where(User.email == email.lower()))
    if not user:
        raise ValueError("User must register before invite (MVP)")
    existing = db.scalar(
        select(TenantMember).where(
            TenantMember.tenant_id == tenant_id,
            TenantMember.user_id == user.id,
        )
    )
    if existing:
        existing.role = role
        existing.status = MemberStatus.active
        db.commit()
        db.refresh(existing)
        member = existing
    else:
        member = TenantMember(
            tenant_id=tenant_id,
            user_id=user.id,
            role=role,
            status=MemberStatus.active,
        )
        db.add(member)
        db.commit()
        db.refresh(member)
    write_audit(
        db,
        action="member.invite",
        resource_type="tenant_member",
        resource_id=str(member.id),
        tenant_id=tenant_id,
        actor_user_id=actor_user_id,
        meta={"invitee": str(user.id), "role": role.value},
    )
    return member


def list_members(db: Session, tenant_id: UUID) -> list[tuple[TenantMember, User]]:
    rows = db.execute(
        select(TenantMember, User)
        .join(User, User.id == TenantMember.user_id)
        .where(TenantMember.tenant_id == tenant_id)
    ).all()
    return [(m, u) for m, u in rows]


def update_role(
    db: Session,
    *,
    tenant_id: UUID,
    user_id: UUID,
    role: MemberRole,
    actor_user_id: UUID,
) -> TenantMember:
    member = db.scalar(
        select(TenantMember).where(
            TenantMember.tenant_id == tenant_id,
            TenantMember.user_id == user_id,
        )
    )
    if not member:
        raise ValueError("Member not found")
    if member.role == MemberRole.owner and role != MemberRole.owner:
        raise ValueError("Cannot demote the only owner via this endpoint")
    member.role = role
    db.commit()
    db.refresh(member)
    write_audit(
        db,
        action="member.role_change",
        resource_type="tenant_member",
        resource_id=str(member.id),
        tenant_id=tenant_id,
        actor_user_id=actor_user_id,
        meta={"new_role": role.value},
    )
    return member


def get_membership(db: Session, tenant_id: UUID, user_id: UUID) -> TenantMember | None:
    return db.scalar(
        select(TenantMember).where(
            TenantMember.tenant_id == tenant_id,
            TenantMember.user_id == user_id,
            TenantMember.status == MemberStatus.active,
        )
    )
