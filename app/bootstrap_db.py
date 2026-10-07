"""python -m app.bootstrap_db"""

from app.core.db import init_db
from app.core.logging import setup_logging


def main() -> None:
    setup_logging(True)
    init_db()
    print("Database initialized.")


if __name__ == "__main__":
    main()
