from __future__ import annotations

import hashlib
import secrets
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.access.rbac import VALID_CAPABILITIES
from app.models.orm import APIKey
from app.services.audit import write_audit


def _hash_key(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()


def create_api_key(
    db: Session,
    *,
    tenant_id: UUID,
    name: str,
    capabilities: list[str],
    kb_allowlist: list[UUID] | None,
    actor_user_id: UUID,
) -> tuple[APIKey, str]:
    caps = [c for c in capabilities if c in VALID_CAPABILITIES]
    if not caps:
        raise ValueError("At least one valid capability required")
    raw = f"rae_{secrets.token_urlsafe(32)}"
    row = APIKey(
        tenant_id=tenant_id,
        name=name,
        key_prefix=raw[:12],
        key_hash=_hash_key(raw),
        capabilities=caps,
        kb_allowlist=kb_allowlist,
        created_by=actor_user_id,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    write_audit(
        db,
        action="apikey.create",
        resource_type="api_key",
        resource_id=str(row.id),
        tenant_id=tenant_id,
        actor_user_id=actor_user_id,
        meta={"capabilities": caps},
    )
    return row, raw


def list_api_keys(db: Session, tenant_id: UUID) -> list[APIKey]:
    return list(
        db.scalars(
            select(APIKey).where(APIKey.tenant_id == tenant_id, APIKey.revoked_at.is_(None))
        ).all()
    )


def revoke_api_key(db: Session, tenant_id: UUID, key_id: UUID, actor_user_id: UUID) -> APIKey:
    row = db.scalar(
        select(APIKey).where(APIKey.id == key_id, APIKey.tenant_id == tenant_id)
    )
    if not row:
        raise ValueError("API key not found")
    row.revoked_at = datetime.now(UTC)
    db.commit()
    db.refresh(row)
    write_audit(
        db,
        action="apikey.revoke",
        resource_type="api_key",
        resource_id=str(row.id),
        tenant_id=tenant_id,
        actor_user_id=actor_user_id,
    )
    return row


def resolve_api_key(db: Session, raw_key: str) -> APIKey | None:
    if not raw_key:
        return None
    hashed = _hash_key(raw_key)
    return db.scalar(
        select(APIKey).where(APIKey.key_hash == hashed, APIKey.revoked_at.is_(None))
    )
