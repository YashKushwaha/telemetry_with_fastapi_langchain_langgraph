
## Running the FastAPI app
> uvicorn api.app.create_app --factory --reload

```console
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [27329] using StatReload
INFO:     Started server process [27339]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:56826 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:56826 - "GET /openapi.json HTTP/1.1" 200 OK
INFO:     127.0.0.1:56826 - "GET /chat HTTP/1.1" 200 OK
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): otlp.arize.com:443
DEBUG:urllib3.connectionpool:https://otlp.arize.com:443 "POST /v1/traces HTTP/1.1" 200 0
INFO:     127.0.0.1:52622 - "GET /chat HTTP/1.1" 200 OK
{
    "name": "process_input",
    "context": {
        "trace_id": "0x0af8dfb5d1a89f01210ee73c1d58fe4b",
        "span_id": "0x200cc6e17cec1356",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": "0x06e69548110a8ad1",
    "start_time": "2026-06-20T09:52:51.255533Z",
    "end_time": "2026-06-20T09:52:51.255561Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "input.value": "Hello, World!",
        "output.value": "HELLO, WORLD!",
        "openinference.span.kind": "LC_NODE",
        "openinference.workflow.name": "process_input"
    },
    "events": [
        {
            "name": "Inside process_input function",
            "timestamp": "2026-06-20T09:52:51.255553Z",
            "attributes": {}
        }
    ],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.42.1",
            "service.name": "chat-service",
            "openinference.project.name": "my-chatbot"
        },
        "schema_url": ""
    }
}
{
    "name": "chat",
    "context": {
        "trace_id": "0x0af8dfb5d1a89f01210ee73c1d58fe4b",
        "span_id": "0x06e69548110a8ad1",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": null,
    "start_time": "2026-06-20T09:52:51.253888Z",
    "end_time": "2026-06-20T09:52:51.255844Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "http.request.method": "get",
        "http.route": "/chat",
        "http.status_code": 200,
        "input.value": "Hello, World!",
        "output.value": "{\"message\": \"Welcome to the chat!\", \"result\": {\"input\": \"HELLO, WORLD!\"}}",
        "openinference.span.kind": "FASTAPI",
        "openinference.workflow.name": "/chat"
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.42.1",
            "service.name": "chat-service",
            "openinference.project.name": "my-chatbot"
        },
        "schema_url": ""
    }
}
DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): otlp.arize.com:443
DEBUG:urllib3.connectionpool:https://otlp.arize.com:443 "POST /v1/traces HTTP/1.1" 200 0

DEBUG:urllib3.connectionpool:Starting new HTTPS connection (1): otlp.arize.com:443
DEBUG:urllib3.connectionpool:https://otlp.arize.com:443 "POST /v1/traces HTTP/1.1" 200 0
{
    "name": "process_input",
    "context": {
        "trace_id": "0x0efc4745a152b89828f09e96cfe979cb",
        "span_id": "0x5576054efdfccfb8",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": "0x0026fc23f8d30e4c",
    "start_time": "2026-06-20T10:03:35.113271Z",
    "end_time": "2026-06-20T10:03:37.113373Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "input.value": "Hello, World!",
        "output.value": "HELLO, WORLD!",
        "openinference.span.kind": "LC_NODE",
        "openinference.workflow.name": "process_input"
    },
    "events": [
        {
            "name": "Inside process_input function",
            "timestamp": "2026-06-20T10:03:35.113292Z",
            "attributes": {}
        }
    ],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.42.1",
            "service.name": "chat-service",
            "openinference.project.name": "my-chatbot"
        },
        "schema_url": ""
    }
}
DEBUG:urllib3.connectionpool:https://otlp.arize.com:443 "POST /v1/traces HTTP/1.1" 200 0
{
    "name": "chat",
    "context": {
        "trace_id": "0x0efc4745a152b89828f09e96cfe979cb",
        "span_id": "0x0026fc23f8d30e4c",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": null,
    "start_time": "2026-06-20T10:03:35.111920Z",
    "end_time": "2026-06-20T10:03:37.641282Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "http.request.method": "get",
        "http.route": "/chat",
        "http.status_code": 200,
        "input.value": "Hello, World!",
        "output.value": "{\"message\": \"Welcome to the chat!\", \"result\": {\"input\": \"HELLO, WORLD!\"}}",
        "openinference.span.kind": "FASTAPI",
        "openinference.workflow.name": "/chat"
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.42.1",
            "service.name": "chat-service",
            "openinference.project.name": "my-chatbot"
        },
        "schema_url": ""
    }
}
INFO:     127.0.0.1:50864 - "GET /chat HTTP/1.1" 200 OK
^CINFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process [49538]
INFO:     Stopping reloader process [27329]

```