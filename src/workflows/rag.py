from typing import List, Optional

from telemetry.provider import trace_span
from db.vector_db import MockVectorDB
from llm.mock_llm import generate_response


async def run_rag_workflow(message: str, user_id: str, conversation_id: Optional[str] = None) -> tuple[str, List[str]]:
    with trace_span("Planner", {"conversation.id": conversation_id or "pending", "user.id": user_id}):
        plan = {"query": message, "strategy": "keyword_search"}

    with trace_span("Retriever", {"strategy": plan["strategy"], "conversation.id": conversation_id or "pending"}):
        vector_db = MockVectorDB()
        documents = await vector_db.retrieve(plan["query"], top_k=5)

    with trace_span("LLM", {"model.version": "mock-v1", "conversation.id": conversation_id or "pending"}):
        response = await generate_response(message, documents)

    return response, documents
