from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api_router
from app.core.config import settings
from app.core.db import init_db
from app.core.logging import setup_logging
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.request_id import RequestIdMiddleware
from app.models.schemas import HealthOut


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_logging(settings.debug)
    settings.ensure_data_dir()
    try:
        init_db()
    except Exception:  # noqa: BLE001
        # Allow app import without DB (tests/docs); runtime endpoints need DB.
        if not settings.debug:
            raise
    yield


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        description=(
            "Enterprise RAG/Agent MVP inspired by WeKnora: "
            "multi-tenant, RBAC, hybrid search, ReAct tools, SSE."
        ),
        version="0.1.0",
        lifespan=lifespan,
    )
    application.add_middleware(RequestIdMiddleware)
    application.add_middleware(RateLimitMiddleware, limit=120, window=60.0)
    application.include_router(api_router)

    @application.get("/health", response_model=HealthOut, tags=["system"])
    def health() -> HealthOut:
        return HealthOut(ok=True, service=settings.app_name)

    return application


app = create_app()
