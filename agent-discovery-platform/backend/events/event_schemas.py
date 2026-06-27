from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class BaseEvent(BaseModel):
    event_id: str
    timestamp: datetime
    tenant_id: str
    
class AgentLifecycleEvent(BaseEvent):
    agent_id: str
    previous_status: str
    new_status: str
    user_id: str

class DiscoveryFeedbackEvent(BaseEvent):
    log_id: str
    user_id: str
    feedback_type: str
    selected_agent_id: Optional[str] = None
    rating: Optional[int] = None

class GuardrailViolationEvent(BaseEvent):
    user_id: str
    violation_type: str
    action_taken: str

class ContinuousImprovementEvent(BaseEvent):
    suggestion_id: str
    action: str # generated|approved|rejected
