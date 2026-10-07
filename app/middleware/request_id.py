from __future__ import annotations

import logging
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:  # type: ignore[no-untyped-def]
        request_id = request.headers.get("X-Request-Id", uuid.uuid4().hex[:12])
        request.state.request_id = request_id
        # Attach to log records in this context via filter-less attribute on logger adapter
        old_factory = logging.getLogRecordFactory()

        def factory(*args, **kwargs):  # type: ignore[no-untyped-def]
            record = old_factory(*args, **kwargs)
            record.request_id = request_id
            return record

        logging.setLogRecordFactory(factory)
        try:
            response = await call_next(request)
        finally:
            logging.setLogRecordFactory(old_factory)
        response.headers["X-Request-Id"] = request_id
        return response
