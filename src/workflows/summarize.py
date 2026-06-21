from typing import List, Tuple

from telemetry.provider import trace_span
from llm.mock_llm import summarize_text


def chunk_document(document: str, chunk_size: int = 120) -> List[str]:
    words = document.split()
    chunks = [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return [chunk for chunk in chunks if chunk.strip()]


async def run_summarize_workflow(document: str) -> Tuple[str, int]:
    chunks = chunk_document(document)
    summaries = []

    for chunk in chunks:
        with trace_span("Chunk", {"chunk_length": str(len(chunk))}):
            summary = await summarize_text(chunk)
            summaries.append(summary)

    return "\n".join(summaries), len(chunks)
