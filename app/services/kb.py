from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.orm import KnowledgeBase, User
from app.services.audit import write_audit


def create_kb(
    db: Session,
    *,
    tenant_id: UUID,
    owner: User,
    name: str,
    description: str = "",
) -> KnowledgeBase:
    kb = KnowledgeBase(
        tenant_id=tenant_id,
        owner_user_id=owner.id,
        name=name,
        description=description,
    )
    db.add(kb)
    db.commit()
    db.refresh(kb)
    write_audit(
        db,
        action="kb.create",
        resource_type="knowledge_base",
        resource_id=str(kb.id),
        tenant_id=tenant_id,
        actor_user_id=owner.id,
    )
    return kb


def list_kbs(db: Session, tenant_id: UUID) -> list[KnowledgeBase]:
    return list(
        db.scalars(select(KnowledgeBase).where(KnowledgeBase.tenant_id == tenant_id)).all()
    )


def get_kb(db: Session, tenant_id: UUID, kb_id: UUID) -> KnowledgeBase | None:
    return db.scalar(
        select(KnowledgeBase).where(
            KnowledgeBase.id == kb_id,
            KnowledgeBase.tenant_id == tenant_id,
        )
    )
