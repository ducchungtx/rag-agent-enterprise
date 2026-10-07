from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.orm import MemberRole, MemberStatus, Tenant, TenantMember, User
from app.services.audit import write_audit


def create_tenant(db: Session, *, name: str, owner: User) -> Tenant:
    tenant = Tenant(name=name)
    db.add(tenant)
    db.flush()
    db.add(
        TenantMember(
            tenant_id=tenant.id,
            user_id=owner.id,
            role=MemberRole.owner,
            status=MemberStatus.active,
        )
    )
    db.commit()
    db.refresh(tenant)
    write_audit(
        db,
        action="tenant.create",
        resource_type="tenant",
        resource_id=str(tenant.id),
        tenant_id=tenant.id,
        actor_user_id=owner.id,
    )
    return tenant


def list_tenants_for_user(db: Session, user_id: UUID) -> list[Tenant]:
    q = (
        select(Tenant)
        .join(TenantMember, TenantMember.tenant_id == Tenant.id)
        .where(
            TenantMember.user_id == user_id,
            TenantMember.status == MemberStatus.active,
            Tenant.deleted_at.is_(None),
        )
    )
    return list(db.scalars(q).all())


def get_tenant(db: Session, tenant_id: UUID) -> Tenant | None:
    return db.scalar(
        select(Tenant).where(Tenant.id == tenant_id, Tenant.deleted_at.is_(None))
    )
