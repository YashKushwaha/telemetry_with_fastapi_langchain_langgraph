from fastapi import APIRouter
#from orchestration.workflow import create_workflow

from orchestration.workflow import create_workflow
from opentelemetry import trace

router = APIRouter()
tracer = trace.get_tracer(__name__)

@router.get("/chat", tags=["Chat"])
async def chat():
    workflow = await create_workflow()
    compiled_workflow = workflow.compile()
    invoke_params = {"input": "Hello, World!"}
    result = await compiled_workflow.ainvoke(invoke_params)

    with tracer.start_as_current_span("chat") as span:

        span.set_attribute("chat.input", invoke_params["input"])
        span.set_attribute("chat.output", result["input"])


    return {"message": "Welcome to the chat!", "result": result}
