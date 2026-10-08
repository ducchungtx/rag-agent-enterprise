"""python -m app.bootstrap_db [--reset]

--reset: DROP all tables rồi tạo lại (cần khi đổi EMBEDDING_DIM, vd. 384 → 1024).
"""

from __future__ import annotations

import sys

from app.core.db import Base, engine, init_db
from app.core.logging import setup_logging


def main() -> None:
    setup_logging(True)
    reset = "--reset" in sys.argv
    if reset:
        from app.models import orm as _orm  # noqa: F401

        Base.metadata.drop_all(bind=engine)
        print("Dropped all tables (--reset).")
    init_db()
    from app.core.config import settings

    print(f"Database initialized. EMBEDDING_DIM={settings.embedding_dim}")


if __name__ == "__main__":
    main()
