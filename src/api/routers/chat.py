from fastapi import APIRouter, Depends

router = APIRouter(prefix="/chat",tags=["chat"])
from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel

class ChatRequest(BaseModel):
    """
    Pydantic model for the chat request body.
    """
    message: str = "Hello, how can I help you?"  # Default message for demonstration

router = APIRouter(prefix="/chat",tags=["chat"])

@router.post("/chat")
async def chat(request: Request, response: Response, input: ChatRequest):
    """
    Endpoint to handle chat requests.
    """
    # Here you would implement the logic to process the chat request
    # For example, you might extract the message from the request body,
    # send it to a chat service, and return the response.
    
    # Placeholder response for demonstration purposes

    return {"message": input.message}