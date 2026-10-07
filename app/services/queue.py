"""Async ingest via Redis RQ (Phase 5). Falls back to sync when disabled."""

from __future__ import annotations

import logging
from uuid import UUID

from app.core.config import settings

logger = logging.getLogger(__name__)


def enqueue_ingest(document_id: UUID) -> str:
    """Return job id or 'sync'."""
    if not settings.use_async_ingest:
        from app.core.db import SessionLocal
        from app.services.ingest import process_document

        with SessionLocal() as db:
            process_document(db, document_id)
        return "sync"

    from redis import Redis
    from rq import Queue

    from app.workers.jobs import process_document_job

    redis = Redis.from_url(settings.redis_url)
    q = Queue("ingest", connection=redis)
    job = q.enqueue(process_document_job, str(document_id))
    logger.info("Enqueued ingest job %s for document %s", job.id, document_id)
    return job.id
