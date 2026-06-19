from fastapi import APIRouter
#from orchestration.workflow import create_workflow

from orchestration.workflow import create_workflow


router = APIRouter()
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

@router.get("/chat", tags=["Chat"])
async def chat():
    workflow = await create_workflow()
    compiled_workflow = workflow.compile()
    invoke_params = {"input": "Hello, World!"}
    with tracer.start_as_current_span("chat") as span:
        result = await compiled_workflow.ainvoke(invoke_params)
        span.set_attribute("chat.input", invoke_params["input"])
        span.set_attribute("chat.output", result["input"])
    
    return {"message": "Welcome to the chat!", "result": result}
