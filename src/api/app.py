from fastapi import FastAPI

from api.routers import health_and_root
from api.routers import chat

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

def create_app() -> FastAPI:
    app = FastAPI(title="My FastAPI Application", version="1.0.0")

    # Include your routers here
    app.include_router(health_and_root.router)
    app.include_router(chat.router)
    # app.include_router(my_router)

    return app