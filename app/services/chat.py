from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.schemas import ChatOut, CitationOut
from app.services.llm import chat_completion
from app.services.retrieve import search_chunks

SYSTEM = (
    "Bạn là trợ lý Q&A doanh nghiệp. Chỉ trả lời dựa trên ngữ cảnh được cung cấp. "
    "Nếu thiếu dữ liệu, nói rõ không có thông tin."
)


def answer_question(
    db: Session,
    *,
    tenant_id: UUID,
    kb_id: UUID,
    question: str,
    top_k: int = 5,
) -> ChatOut:
    citations = search_chunks(
        db, tenant_id=tenant_id, kb_id=kb_id, query=question, top_k=top_k
    )
    contexts = [c.content for c in citations]
    answer = chat_completion(SYSTEM, question, contexts)
    return ChatOut(answer=answer, citations=citations)
