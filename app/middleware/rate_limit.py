"""Simple in-memory rate limit (dev/MVP). Prefer Redis in production."""

from __future__ import annotations

import time
from collections import defaultdict, deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Limit bursts on auth + write endpoints per client IP."""

    def __init__(self, app, *, limit: int = 60, window: float = 60.0) -> None:
        super().__init__(app)
        self.limit = limit
        self.window = window
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next) -> Response:  # type: ignore[no-untyped-def]
        path = request.url.path
        if not (
            path.startswith("/auth/")
            or path.startswith("/kb/")
            or path.startswith("/api-keys")
        ):
            return await call_next(request)

        ip = request.client.host if request.client else "unknown"
        key = f"{ip}:{path.split('/')[1]}"
        now = time.monotonic()
        q = self._hits[key]
        while q and now - q[0] > self.window:
            q.popleft()
        if len(q) >= self.limit:
            return JSONResponse(
                {"detail": "Rate limit exceeded"},
                status_code=429,
                headers={"Retry-After": str(int(self.window))},
            )
        q.append(now)
        return await call_next(request)
