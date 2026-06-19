from fastapi import FastAPI

from api.routers import health_and_root
from api.routers import chat

def create_app() -> FastAPI:
    app = FastAPI(title="My FastAPI Application", version="1.0.0")

    # Include your routers here
    app.include_router(health_and_root.router)
    app.include_router(chat.router)
    # app.include_router(my_router)

    return app