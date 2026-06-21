from fastapi import FastAPI

from api.routers import analytics, chat, feedback, search, summarize
from middleware.request_context import RequestContextMiddleware


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="AI Knowledge Assistant Platform", version="0.1.0")
    app.add_middleware(RequestContextMiddleware)

    app.include_router(chat)
    app.include_router(search)
    app.include_router(summarize)
    app.include_router(analytics)
    app.include_router(feedback)

    return app


app = create_app()
