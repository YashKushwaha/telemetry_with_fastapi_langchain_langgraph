from opentelemetry import trace
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

def build_resource(config: dict) -> Resource:

    return Resource.create({
        config
    })

def build_provider(resource):
    return TracerProvider(resource=resource)

#### Exporters
def build_console():

    return ConsoleSpanExporter()


def build_otlp():
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    return OTLPSpanExporter()


def build_file():

    return JsonFileExporter(...)


config = {"service.name": "chat service"}

resource = build_resource(config)
trace_provider = build_provider(resource)


trace_provider = TracerProvider(resource=resource)

exporter = ConsoleSpanExporter()
trace_provider.add_span_processor(BatchSpanProcessor(exporter))


trace.set_tracer_provider(trace_provider)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("foo"):
    print("Hello world!")