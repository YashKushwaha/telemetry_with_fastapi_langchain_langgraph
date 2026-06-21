import time
import uuid
from typing import Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from telemetry.context import RequestContext, set_request_context
from telemetry.metrics import record_request


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        user_id = request.headers.get("x-user-id", "anonymous")
        session_id = request.headers.get("x-session-id", f"session-{uuid.uuid4().hex[:8]}")
        conversation_id = request.headers.get("x-conversation-id")
        tenant_id = request.headers.get("x-tenant-id", "default")
        experiment_id = request.headers.get("x-experiment-id", "default")
        model_version = request.headers.get("x-model-version", "mock-v1")

        set_request_context(
            RequestContext(
                user_id=user_id,
                session_id=session_id,
                conversation_id=conversation_id,
                request_id=request_id,
                tenant_id=tenant_id,
                experiment_id=experiment_id,
                model_version=model_version,
            )
        )

        start_time = time.perf_counter()
        failed = False
        try:
            response = await call_next(request)
            failed = response.status_code >= 400
            return response
        finally:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            record_request(request.url.path, round(latency_ms, 1), failed=failed)
