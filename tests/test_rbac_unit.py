from app.access.rbac import ROLE_RANK, require_capability, require_role
from app.models.orm import MemberRole
from fastapi import HTTPException
import pytest


def test_viewer_cannot_upload():
    with pytest.raises(HTTPException) as ei:
        require_role(MemberRole.viewer, "kb.upload")
    assert ei.value.status_code == 403


def test_contributor_can_upload():
    require_role(MemberRole.contributor, "kb.upload")


def test_api_key_retrieve_blocks_qa():
    with pytest.raises(HTTPException) as ei:
        require_capability(["retrieve"], "kb.chat")
    assert ei.value.status_code == 403


def test_api_key_qa_allows_chat():
    require_capability(["qa"], "kb.chat")


def test_role_rank_order():
    assert ROLE_RANK[MemberRole.viewer] < ROLE_RANK[MemberRole.owner]
