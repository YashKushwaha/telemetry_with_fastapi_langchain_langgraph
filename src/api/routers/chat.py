from fastapi import APIRouter
#from orchestration.workflow import create_workflow

from orchestration.workflow import create_workflow


router = APIRouter()

@router.get("/chat", tags=["Chat"])
async def chat():
    workflow = await create_workflow()
    compiled_workflow = workflow.compile()
    result = await compiled_workflow.ainvoke({"input": "Hello, World!"})
    return {"message": "Welcome to the chat!", "result": result}
