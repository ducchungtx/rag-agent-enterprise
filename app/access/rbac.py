"""RBAC helpers — role for humans, capabilities for API keys (WeKnora spirit)."""

from __future__ import annotations

from fastapi import HTTPException, status

from app.models.orm import MemberRole

ROLE_RANK = {
    MemberRole.viewer: 1,
    MemberRole.contributor: 2,
    MemberRole.admin: 3,
    MemberRole.owner: 4,
}

# action → minimum role
ACTION_MIN_ROLE: dict[str, MemberRole] = {
    "kb.read": MemberRole.viewer,
    "kb.chat": MemberRole.viewer,
    "kb.search": MemberRole.viewer,
    "kb.create": MemberRole.contributor,
    "kb.upload": MemberRole.contributor,
    "kb.delete": MemberRole.admin,
    "member.invite": MemberRole.admin,
    "member.role": MemberRole.admin,
    "tenant.delete": MemberRole.owner,
    "apikey.manage": MemberRole.admin,
}

VALID_CAPABILITIES = {"retrieve", "qa", "ingest", "admin"}

CAPABILITY_FOR_ACTION = {
    "kb.search": "retrieve",
    "kb.read": "retrieve",
    "kb.chat": "qa",
    "kb.upload": "ingest",
    "kb.create": "ingest",
    "apikey.manage": "admin",
    "member.invite": "admin",
}


def require_role(role: MemberRole, action: str) -> None:
    min_role = ACTION_MIN_ROLE.get(action)
    if min_role is None:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Unknown action: {action}")
    if ROLE_RANK[role] < ROLE_RANK[min_role]:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=f"Role '{role.value}' cannot perform '{action}' (need >= {min_role.value})",
        )


def require_capability(capabilities: list[str], action: str) -> None:
    needed = CAPABILITY_FOR_ACTION.get(action)
    if needed is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"API Key cannot perform '{action}'")
    caps = set(capabilities or [])
    if "admin" in caps:
        return
    if needed not in caps:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            detail=f"API Key missing capability '{needed}' for action '{action}'",
        )
