from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from backend.agents.graph import discovery_pipeline
from backend.api.deps import get_current_user

router = APIRouter()

class DiscoveryRequest(BaseModel):
    query: str
    filters: Optional[Dict[str, Any]] = None

@router.post("/")
async def discover_agents(request: DiscoveryRequest, current_user: dict = Depends(get_current_user)):
    initial_state = {
        "user_query": request.query,
        "user_id": current_user["id"],
        "tenant_id": current_user["tenant_id"],
        "filters": request.filters or {},
        "trace_id": "trace-uuid-here",
        "cost_budget_remaining": 0.05
    }
    
    # Run LangGraph pipeline
    final_state = await discovery_pipeline.ainvoke(initial_state)
    
    return {
        "recommendations": final_state.get("recommended_agents", []),
        "mcp_servers": final_state.get("recommended_mcp", []),
        "composition_strategy": final_state.get("composition_strategy"),
        "citations": final_state.get("citations", []),
        "confidence": final_state.get("confidence_scores", {}),
        "validation": final_state.get("validation_result", {}),
        "workflow_trace": final_state.get("workflow_steps", []),
        "errors": final_state.get("errors", [])
    }
