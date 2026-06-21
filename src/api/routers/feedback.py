from datetime import datetime
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from telemetry.metrics import add_feedback

router = APIRouter(prefix="/feedback", tags=["feedback"])


class FeedbackRequest(BaseModel):
    user_id: Optional[str] = Field(None, example="alice")
    rating: int = Field(..., ge=1, le=5, example=5)
    comment: Optional[str] = Field(None, example="The answer was helpful.")


class FeedbackResponse(BaseModel):
    feedback_id: str
    user_id: Optional[str]
    rating: int
    comment: Optional[str]
    created_at: str


@router.post("", response_model=FeedbackResponse)
async def feedback(input: FeedbackRequest) -> FeedbackResponse:
    feedback_id = add_feedback(input.user_id, input.rating, input.comment)
    return FeedbackResponse(
        feedback_id=feedback_id,
        user_id=input.user_id,
        rating=input.rating,
        comment=input.comment,
        created_at=datetime.utcnow().isoformat() + "Z",
    )
