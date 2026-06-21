from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel, Field, field_validator

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    """Request payload for the chat endpoint."""

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
    """Response returned by the chat endpoint."""

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

# Simple in-memory stores for demonstration.
CONVERSATION_STORE: Dict[str, Conversation] = {}
DOCUMENT_STORE: List[str] = [
    "The company policy on remote work allows two days from home per week.",
    "Our code style guide requires type hints and black formatting.",
    "The onboarding process includes security training and access requests.",
    "Release cycles are planned monthly and coordinated through the product team.",
    "The mock LLM returns responses based on the provided user query and retrieved documents.",
]


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


def plan_chat(message: str) -> Dict[str, str]:
    """Planner step: decide the query for the retriever."""
    return {
        "query": message,
        "strategy": "keyword_search",
    }


def retrieve_documents(query: str, limit: int = 3) -> List[str]:
    """Retriever step: fetch documents relevant to the query."""
    query_terms = {token.lower() for token in query.split() if token}
    scored = []

    for doc in DOCUMENT_STORE:
        score = len(query_terms.intersection({token.strip(".,").lower() for token in doc.split()}))
        if score > 0:
            scored.append((score, doc))

    if not scored:
        return DOCUMENT_STORE[:limit]

    scored.sort(key=lambda item: item[0], reverse=True)
    return [doc for _, doc in scored[:limit]]


def call_llm(query: str, documents: List[str]) -> str:
    """LLM step: generate a response from the query and retrieved documents."""
    context = "\n".join(f"- {doc}" for doc in documents)
    return (
        f"Here is an answer to your question: '{query}'.\n"
        f"I used {len(documents)} document(s) from the conversation context.\n\n"
        f"Context:\n{context}"
    )


def save_conversation_turn(conversation: Conversation, role: str, text: str) -> None:
    conversation.history.append({"role": role, "text": text, "timestamp": datetime.utcnow().isoformat() + "Z"})


@router.post("/", response_model=ChatResponse)
async def chat(input: ChatRequest) -> ChatResponse:
    """Normal chatbot endpoint implementing the request -> planner -> retriever -> LLM workflow."""
    conversation = create_conversation(input.user_id, input.conversation_id)
    save_conversation_turn(conversation, "user", input.message)

    plan = plan_chat(input.message)
    documents = retrieve_documents(plan["query"])
    llm_response = call_llm(input.message, documents)

    save_conversation_turn(conversation, "assistant", llm_response)

    return ChatResponse(
        conversation_id=conversation.id,
        request_id=f"req-{uuid4().hex[:8]}",
        response=llm_response,
        retrieved_documents=documents,
        created_at=datetime.utcnow().isoformat() + "Z",
    )
