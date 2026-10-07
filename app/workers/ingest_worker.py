"""RQ worker entry: python -m app.workers.ingest_worker"""

from __future__ import annotations

from redis import Redis
from rq import Worker

from app.core.config import settings
from app.core.logging import setup_logging


def main() -> None:
    setup_logging(settings.debug)
    redis = Redis.from_url(settings.redis_url)
    worker = Worker(["ingest"], connection=redis)
    worker.work(with_scheduler=False)


if __name__ == "__main__":
    main()
