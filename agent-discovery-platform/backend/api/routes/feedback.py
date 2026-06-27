from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.api.deps import get_current_user
from backend.harness.feedback_service import feedback_service
from backend.harness.continuous_improvement import ci_engine

router = APIRouter()

class FeedbackRequest(BaseModel):
    discovery_log_id: str
    feedback_type: str # thumbs_up, thumbs_down, correction
    selected_agent_id: str = None
    rating: int = None
    correction_text: str = None

@router.post("/")
async def submit_feedback(request: FeedbackRequest, current_user: dict = Depends(get_current_user)):
    await feedback_service.submit_feedback(
        log_id=request.discovery_log_id,
        user_id=current_user["id"],
        feedback_type=request.feedback_type,
        selected_agent_id=request.selected_agent_id,
        rating=request.rating,
        correction_text=request.correction_text
    )
    return {"status": "success"}

@router.get("/stats")
async def get_feedback_stats(current_user: dict = Depends(get_current_user)):
    stats = await feedback_service.get_feedback_stats()
    return stats

@router.get("/improvement-suggestions")
async def get_improvement_suggestions(current_user: dict = Depends(get_current_user)):
    suggestions = await ci_engine.analyze_recent_feedback()
    return suggestions
