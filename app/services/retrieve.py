from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.orm import Chunk, Document, ParseStatus
from app.models.schemas import CitationOut
from app.services.llm import embed_query


def search_chunks(
    db: Session,
    *,
    tenant_id: UUID,
    kb_id: UUID,
    query: str,
    top_k: int = 5,
) -> list[CitationOut]:
    q_emb = embed_query(query)
    # Vector distance (cosine via <=> with normalized vectors ≈ L2 for unit vectors)
    distance = Chunk.embedding.cosine_distance(q_emb).label("distance")

    stmt: Select = (
        select(Chunk, Document.title, distance)
        .join(Document, Document.id == Chunk.document_id)
        .where(
            Chunk.tenant_id == tenant_id,
            Chunk.kb_id == kb_id,
            Document.parse_status == ParseStatus.completed,
            Document.tenant_id == tenant_id,
        )
        .order_by(distance)
        .limit(top_k * 3)
    )
    rows = db.execute(stmt).all()

    # Light keyword boost (hybrid-lite)
    tokens = [t for t in query.lower().split() if len(t) > 2]
    scored: list[tuple[float, CitationOut]] = []
    for chunk, title, dist in rows:
        score = 1.0 / (1.0 + float(dist or 0.0))
        content_l = chunk.content.lower()
        boost = sum(1 for t in tokens if t in content_l) * 0.05
        score += boost
        scored.append(
            (
                score,
                CitationOut(
                    chunk_id=chunk.id,
                    document_id=chunk.document_id,
                    title=title,
                    content=chunk.content,
                    score=score,
                ),
            )
        )
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:top_k]]


def read_document_text(
    db: Session,
    *,
    tenant_id: UUID,
    document_id: UUID,
    max_chars: int = 4000,
) -> str | None:
    doc = db.scalar(
        select(Document).where(
            Document.id == document_id,
            Document.tenant_id == tenant_id,
            Document.parse_status == ParseStatus.completed,
        )
    )
    if not doc:
        return None
    chunks = list(
        db.scalars(
            select(Chunk)
            .where(Chunk.document_id == document_id, Chunk.tenant_id == tenant_id)
            .order_by(Chunk.position)
        ).all()
    )
    text_body = "\n\n".join(c.content for c in chunks)
    return text_body[:max_chars]
