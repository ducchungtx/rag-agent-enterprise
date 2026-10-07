from __future__ import annotations

import logging
import shutil
from pathlib import Path
from uuid import UUID, uuid4

from pypdf import PdfReader
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.orm import Chunk, Document, ParseStatus
from app.services.audit import write_audit
from app.services.llm import embed_texts

logger = logging.getLogger(__name__)

CHUNK_SIZE = 800
CHUNK_OVERLAP = 120


def _read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        reader = PdfReader(str(path))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    raise ValueError(f"Unsupported file type: {suffix}")


def chunk_text(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + CHUNK_SIZE)
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        if end >= len(text):
            break
        start = max(0, end - CHUNK_OVERLAP)
    return chunks


def create_document_record(
    db: Session,
    *,
    tenant_id: UUID,
    kb_id: UUID,
    title: str,
    src_path: Path,
    user_id: UUID,
) -> Document:
    dest_dir = settings.ensure_data_dir() / str(tenant_id) / str(kb_id)
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{uuid4().hex}_{src_path.name}"
    shutil.copy2(src_path, dest)

    doc = Document(
        tenant_id=tenant_id,
        kb_id=kb_id,
        title=title,
        storage_path=str(dest),
        parse_status=ParseStatus.pending,
        created_by=user_id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    write_audit(
        db,
        action="document.upload",
        resource_type="document",
        resource_id=str(doc.id),
        tenant_id=tenant_id,
        actor_user_id=user_id,
        meta={"kb_id": str(kb_id), "title": title},
    )
    return doc


def process_document(db: Session, document_id: UUID) -> Document:
    doc = db.scalar(select(Document).where(Document.id == document_id))
    if not doc:
        raise ValueError("Document not found")
    doc.parse_status = ParseStatus.processing
    db.commit()
    try:
        text = _read_text(Path(doc.storage_path))
        pieces = chunk_text(text)
        if not pieces:
            raise ValueError("Empty document after parse")

        db.execute(delete(Chunk).where(Chunk.document_id == doc.id))
        embeddings = embed_texts(pieces)
        for i, (content, emb) in enumerate(zip(pieces, embeddings, strict=True)):
            db.add(
                Chunk(
                    tenant_id=doc.tenant_id,
                    document_id=doc.id,
                    kb_id=doc.kb_id,
                    position=i,
                    content=content,
                    embedding=emb,
                )
            )
        doc.parse_status = ParseStatus.completed
        doc.error_message = None
        db.commit()
        db.refresh(doc)
        logger.info("Ingested document %s with %s chunks", doc.id, len(pieces))
        return doc
    except Exception as exc:  # noqa: BLE001
        doc.parse_status = ParseStatus.failed
        doc.error_message = str(exc)
        db.commit()
        db.refresh(doc)
        logger.exception("Ingest failed for %s", document_id)
        return doc


def get_document(db: Session, tenant_id: UUID, document_id: UUID) -> Document | None:
    return db.scalar(
        select(Document).where(Document.id == document_id, Document.tenant_id == tenant_id)
    )
