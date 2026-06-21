from fastapi import APIRouter
from pydantic import BaseModel, Field

from workflows.summarize import run_summarize_workflow

router = APIRouter(prefix="/summarize", tags=["summarize"])


class SummarizeRequest(BaseModel):
    document: str = Field(..., title="Document text", example="This is the text to summarize.")


class SummarizeResponse(BaseModel):
    summary: str
    chunk_count: int


@router.post("", response_model=SummarizeResponse)
async def summarize(input: SummarizeRequest) -> SummarizeResponse:
    summary, chunk_count = await run_summarize_workflow(input.document)
    return SummarizeResponse(summary=summary, chunk_count=chunk_count)
