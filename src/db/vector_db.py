import asyncio
import random
from typing import List

DOCUMENT_STORE = [
    "The company policy on remote work allows two days from home per week.",
    "Our code style guide requires type hints and black formatting.",
    "The onboarding process includes security training and access requests.",
    "Release cycles are planned monthly and coordinated through the product team.",
    "The mock LLM returns responses based on the provided user query and retrieved documents.",
    "Security approval is required before issuing cloud credentials.",
    "Customer support hours are 9am to 6pm in the local time zone.",
    "The deployment checklist includes backups and a rollback plan.",
    "Our analytics dashboard shows usage, latency, and error rates.",
    "The data retention policy keeps logs for 90 days.",
]


class MockVectorDB:
    async def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        await asyncio.sleep(random.uniform(0.05, 0.2))
        if random.random() < 0.1:
            return []

        query_terms = {token.strip(".,").lower() for token in query.split() if token}
        scored = []
        for document in DOCUMENT_STORE:
            document_terms = {token.strip(".,").lower() for token in document.split()}
            score = len(query_terms.intersection(document_terms))
            if score > 0:
                scored.append((score, document))

        if not scored:
            return random.sample(DOCUMENT_STORE, min(top_k, len(DOCUMENT_STORE)))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [document for _, document in scored[:top_k]]

    async def rank_documents(self, documents: List[str], query: str) -> List[str]:
        query_terms = {token.strip(".,").lower() for token in query.split() if token}
        scored = []
        for document in documents:
            document_terms = {token.strip(".,").lower() for token in document.split()}
            score = len(query_terms.intersection(document_terms))
            scored.append((score, document))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [document for _, document in scored]
