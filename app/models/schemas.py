from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from app.models.orm import MemberRole, ParseStatus


class HealthOut(BaseModel):
    ok: bool = True
    service: str


class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    username: str = Field(min_length=2, max_length=120)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MembershipOut(BaseModel):
    tenant_id: UUID
    tenant_name: str
    role: MemberRole
    status: str


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    memberships: list[MembershipOut] = []


class TenantCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)


class TenantOut(BaseModel):
    id: UUID
    name: str
    created_at: datetime


class InviteIn(BaseModel):
    email: EmailStr
    role: MemberRole = MemberRole.viewer


class MemberOut(BaseModel):
    user_id: UUID
    email: str
    username: str
    role: MemberRole
    status: str


class RolePatch(BaseModel):
    role: MemberRole


class KBCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str = ""


class KBOut(BaseModel):
    id: UUID
    tenant_id: UUID
    owner_user_id: UUID
    name: str
    description: str
    created_at: datetime


class DocumentOut(BaseModel):
    id: UUID
    kb_id: UUID
    tenant_id: UUID
    title: str
    parse_status: ParseStatus
    error_message: str | None = None
    created_at: datetime


class SearchIn(BaseModel):
    query: str
    kb_id: UUID
    top_k: int = 5


class CitationOut(BaseModel):
    chunk_id: UUID
    document_id: UUID
    title: str
    content: str
    score: float


class SearchOut(BaseModel):
    results: list[CitationOut]


class ChatIn(BaseModel):
    question: str
    kb_id: UUID
    top_k: int = 5


class ChatOut(BaseModel):
    answer: str
    citations: list[CitationOut]


class AgentChatIn(BaseModel):
    question: str
    kb_id: UUID
    max_steps: int = 5


class APIKeyCreate(BaseModel):
    name: str
    capabilities: list[str] = Field(default_factory=lambda: ["retrieve"])
    kb_allowlist: list[UUID] | None = None


class APIKeyOut(BaseModel):
    id: UUID
    name: str
    key_prefix: str
    capabilities: list[str]
    kb_allowlist: list[UUID] | None
    created_at: datetime
    raw_key: str | None = None


class AuditOut(BaseModel):
    id: UUID
    action: str
    resource_type: str
    resource_id: str | None
    created_at: datetime
