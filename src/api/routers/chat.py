from fastapi import APIRouter
#from orchestration.workflow import create_workflow

from orchestration.workflow import create_workflow


router = APIRouter()
from opentelemetry import trace
tracer = trace.get_tracer(__name__)
import json

@router.get("/chat", tags=["Chat"])
async def chat():
    workflow = await create_workflow()
    compiled_workflow = workflow.compile()
    invoke_params = {"input": "Hello, World!"}
    with tracer.start_as_current_span("chat") as span:
        result = await compiled_workflow.ainvoke(invoke_params)
        output = {"message": "Welcome to the chat!", "result": result}

        attributes ={'http.request.method': 'get', 'http.route': '/chat', 'http.status_code': 200,
                     'input.value': invoke_params["input"], 'output.value': json.dumps(output),
                     'openinference.span.kind': 'FASTAPI', 'openinference.workflow.name': '/chat',
                      }
        span.set_attributes(attributes)

    return output
