from backend.agents.state import DiscoveryState
import time
import logging

logger = logging.getLogger(__name__)

async def governance_agent(state: DiscoveryState) -> DiscoveryState:
    """Verifies compliance, access controls, and certifications for recommended agents."""
    start_time = time.time()
    recommended_agents = state.get("recommended_agents", [])
    
    logger.info("GovernanceAgent auditing recommendations")
    
    governance_status = []
    for agent in recommended_agents:
        # Mock governance check
        status = {
            "agent_id": agent.get("id"),
            "approved": agent.get("status") in ["APPROVED", "PRODUCTION"],
            "requires_access_request": agent.get("classification") != "PUBLIC",
            "certifications": ["Security", "Responsible AI"]
        }
        governance_status.append(status)
        
    duration = int((time.time() - start_time) * 1000)
    step_info = {
        "step": "governance_agent",
        "status": "success",
        "duration_ms": duration,
        "model_used": "N/A (Policy Engine)",
        "tokens": 0
    }
    
    return {
        "governance_status": governance_status,
        "workflow_steps": state.get("workflow_steps", []) + [step_info]
    }
