from typing import Dict, Any

from fastapi import APIRouter
from pydantic import BaseModel

from telemetry.metrics import get_metrics_snapshot

router = APIRouter(prefix="/analytics", tags=["analytics"])


class AnalyticsResponse(BaseModel):
    requests: int
    failed_requests: int
    average_latency_ms: float
    requests_by_path: Dict[str, int]
    feedback_count: int


@router.get("", response_model=AnalyticsResponse)
async def analytics() -> AnalyticsResponse:
    metrics = get_metrics_snapshot()
    return AnalyticsResponse(
        requests=metrics["requests"],
        failed_requests=metrics["failed_requests"],
        average_latency_ms=metrics["average_latency_ms"],
        requests_by_path=metrics["requests_by_path"],
        feedback_count=metrics["feedback_count"],
    )
