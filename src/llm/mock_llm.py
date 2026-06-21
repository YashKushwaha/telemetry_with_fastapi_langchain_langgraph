import asyncio
import random
from typing import List


async def generate_response(prompt: str, documents: List[str]) -> str:
    delay = random.uniform(0.3, 1.5)
    await asyncio.sleep(delay)

    if random.random() < 0.1:
        raise TimeoutError("LLM request timed out")
    if random.random() < 0.1:
        return f"This is a speculative response for: '{prompt}'. Please verify with the source documents."

    if documents:
        context = "\n".join(f"- {document}" for document in documents)
        return (
            f"Answer: {prompt}\n\n"
            f"Retrieved {len(documents)} document(s) to answer your question:\n{context}"
        )

    return f"Answer: {prompt}\n\nNo relevant documents were available in the retriever."


async def summarize_text(text: str) -> str:
    delay = random.uniform(0.2, 0.8)
    await asyncio.sleep(delay)
    sentences = [sentence.strip() for sentence in text.split(".") if sentence.strip()]
    if not sentences:
        return "No content to summarize."
    return f"Summary: {sentences[0]}"
