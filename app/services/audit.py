from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.orm import AuditLog


def write_audit(
    db: Session,
    *,
    action: str,
    resource_type: str,
    resource_id: str | None = None,
    tenant_id: UUID | None = None,
    actor_user_id: UUID | None = None,
    actor_api_key_id: UUID | None = None,
    meta: dict | None = None,
) -> AuditLog:
    row = AuditLog(
        tenant_id=tenant_id,
        actor_user_id=actor_user_id,
        actor_api_key_id=actor_api_key_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        meta=meta,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
