import time
from typing import List

from fastapi import APIRouter, Query
from pydantic import BaseModel

from db.vector_db import MockVectorDB

router = APIRouter(prefix="/search", tags=["search"])


class SearchResponse(BaseModel):
    query: str
    results: List[str]
    total_results: int
    took_ms: float


@router.get("", response_model=SearchResponse)
async def search(q: str = Query(..., min_length=1, examples={"example": {"value": "remote work"}})) -> SearchResponse:
    start = time.perf_counter()
    vector_db = MockVectorDB()
    results = await vector_db.retrieve(q, top_k=10)
    took_ms = (time.perf_counter() - start) * 1000.0
    return SearchResponse(query=q, results=results, total_results=len(results), took_ms=round(took_ms, 1))
