from __future__ import annotations

import logging
from uuid import UUID

logger = logging.getLogger(__name__)


def process_document_job(document_id: str) -> str:
    from app.core.db import SessionLocal
    from app.services.ingest import process_document

    with SessionLocal() as db:
        doc = process_document(db, UUID(document_id))
        return doc.parse_status.value
