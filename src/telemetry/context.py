import contextvars
from dataclasses import asdict, dataclass
from typing import Dict, Optional


@dataclass
class RequestContext:
    user_id: str
    session_id: str
    conversation_id: Optional[str]
    request_id: str
    tenant_id: str
    experiment_id: str
    model_version: str


_request_context: contextvars.ContextVar[Optional[RequestContext]] = contextvars.ContextVar(
    "request_context", default=None
)


def set_request_context(context: RequestContext) -> None:
    _request_context.set(context)


def get_request_context() -> RequestContext:
    context = _request_context.get()
    if context is None:
        raise RuntimeError("Request context is not available")
    return context


def get_request_context_as_dict() -> Dict[str, Optional[str]]:
    return asdict(get_request_context())
