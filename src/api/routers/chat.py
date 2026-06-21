from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

from telemetry.context import get_request_context
from workflows.rag import run_rag_workflow

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str = Field(..., title="User message", example="Hello, how can I help you?")
    conversation_id: Optional[str] = Field(
        None,
        title="Conversation ID",
        description="Optional existing conversation ID to continue an existing chat.",
    )
    user_id: Optional[str] = Field(
        None,
        title="User ID",
        description="Optional user identifier for tracking and conversation grouping.",
    )

    @field_validator("message")
    def message_must_not_be_blank(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("message must not be empty")
        return value.strip()


class ChatResponse(BaseModel):
    conversation_id: str
    request_id: str
    response: str
    retrieved_documents: List[str]
    created_at: str


class Conversation(BaseModel):
    id: str
    user_id: Optional[str]
    created_at: str
    history: List[Dict[str, str]] = []


CONVERSATION_STORE: Dict[str, Conversation] = {}


def create_conversation(user_id: Optional[str], existing_id: Optional[str] = None) -> Conversation:
    if existing_id and existing_id in CONVERSATION_STORE:
        return CONVERSATION_STORE[existing_id]

    conversation_id = existing_id or f"conv-{uuid4().hex[:8]}"
    conversation = Conversation(
        id=conversation_id,
        user_id=user_id,
        created_at=datetime.utcnow().isoformat() + "Z",
        history=[],
    )
    CONVERSATION_STORE[conversation_id] = conversation
    return conversation


def save_conversation_turn(conversation: Conversation, role: str, text: str) -> None:
    conversation.history.append(
        {"role": role, "text": text, "timestamp": datetime.utcnow().isoformat() + "Z"}
    )


@router.post("", response_model=ChatResponse)
async def chat(input: ChatRequest) -> ChatResponse:
    request_context = get_request_context()
    user_id = input.user_id or request_context.user_id
    conversation = create_conversation(user_id, input.conversation_id)
    save_conversation_turn(conversation, "user", input.message)

    response_text, retrieved_documents = await run_rag_workflow(
        input.message, user_id=user_id, conversation_id=conversation.id
    )
    save_conversation_turn(conversation, "assistant", response_text)

    return ChatResponse(
        conversation_id=conversation.id,
        request_id=f"req-{uuid4().hex[:8]}",
        response=response_text,
        retrieved_documents=retrieved_documents,
        created_at=datetime.now().isoformat(),
    )