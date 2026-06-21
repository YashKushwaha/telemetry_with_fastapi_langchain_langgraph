from fastapi import FastAPI
from api.routers import chat

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(title="My API", version="1.0.0")

    # Import and include the chat router
    
    app.include_router(chat.router)

    return app