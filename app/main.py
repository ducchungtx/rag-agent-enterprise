from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api import api_router
from app.core.config import settings
from app.core.db import init_db
from app.core.logging import setup_logging
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.request_id import RequestIdMiddleware
from app.models.schemas import HealthOut

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIST = ROOT / "frontend" / "dist"
WEB_DIR = ROOT / "web"


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
    origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins or ["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(RequestIdMiddleware)
    application.add_middleware(RateLimitMiddleware, limit=120, window=60.0)
    application.include_router(api_router)

    @application.get("/health", response_model=HealthOut, tags=["system"])
    def health() -> HealthOut:
        return HealthOut(ok=True, service=settings.app_name)

    @application.get("/ui", include_in_schema=False)
    def ui_root() -> RedirectResponse:
        return RedirectResponse(url="/ui/")

    # Prefer React build; fall back to lab web/ if dist missing.
    static_dir = FRONTEND_DIST if FRONTEND_DIST.is_dir() else WEB_DIR
    if static_dir.is_dir():
        application.mount(
            "/ui",
            StaticFiles(directory=str(static_dir), html=True),
            name="ui",
        )

    return application


app = create_app()
