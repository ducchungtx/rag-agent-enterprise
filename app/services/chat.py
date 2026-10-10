from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.schemas import ChatOut
from app.services.llm import chat_completion
from app.services.retrieve import search_chunks

SYSTEM = (
    "Bạn là trợ lý Q&A doanh nghiệp pháp chế. "
    "CHỈ trả lời dựa trên ngữ cảnh được cung cấp. "
    "Không suy diễn ngoài nguồn. "
    "Nếu ngữ cảnh trống hoặc không liên quan câu hỏi, nói rõ không có thông tin phù hợp "
    "và không bịa điều luật."
)

REFUSAL_ANSWER = (
    "Không đủ nguồn phù hợp trong Knowledge Base đang chọn để trả lời câu hỏi này."
)
REFUSAL_SUGGESTION = (
    "Hãy đổi sang KB đúng miền (ví dụ Luật Đất đai khi hỏi về đất đai), "
    "hoặc upload tài liệu liên quan rồi hỏi lại."
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
        db,
        tenant_id=tenant_id,
        kb_id=kb_id,
        query=question,
        top_k=top_k,
        apply_relevance_gate=True,
    )
    if not citations:
        return ChatOut(
            answer=REFUSAL_ANSWER,
            citations=[],
            refused=True,
            refusal_reason=REFUSAL_ANSWER,
            suggested_message=REFUSAL_SUGGESTION,
        )
    contexts = [c.content for c in citations]
    answer = chat_completion(SYSTEM, question, contexts)
    return ChatOut(
        answer=answer,
        citations=citations,
        refused=False,
        refusal_reason=None,
        suggested_message=None,
    )
