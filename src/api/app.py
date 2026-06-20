from fastapi import FastAPI

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter

from api.routers import health_and_root, chat
import logging
logging.basicConfig(level=logging.DEBUG)

#from opentelemetry.sdk.trace import set_tracer_provider
import os

os.environ["OTEL_LOG_LEVEL"] = "debug"

import os

ARIZE_SPACE_ID = os.environ["ARIZE_SPACE_ID"]
ARIZE_API_KEY = os.environ["ARIZE_API_KEY"]

# ✅ IMPORTANT: correct Arize + OpenInference resource attributes
resource = Resource.create({
    "service.name": "chat-service",
    "openinference.project.name": "my-chatbot",
})

provider = TracerProvider(resource=resource)

exporter = OTLPSpanExporter(
    endpoint="https://otlp.arize.com/v1/traces",
    headers={
        "arize-space-id": ARIZE_SPACE_ID,
        "arize-api-key": ARIZE_API_KEY,
    },
)

console_exporter = ConsoleSpanExporter()

provider.add_span_processor(SimpleSpanProcessor(exporter))
provider.add_span_processor(SimpleSpanProcessor(console_exporter))

trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title="My FastAPI Application", version="1.0.0")

    app.include_router(health_and_root.router)
    app.include_router(chat.router)

    return app