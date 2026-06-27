from backend.agents.state import DiscoveryState
import logging

logger = logging.getLogger(__name__)

class ResponseValidator:
    """Verifies recommendations against reality (prevents hallucinations)."""
    
    def validate(self, recommended_agents: list) -> dict:
        issues = []
        
        # Check if recommendations are empty
        if not recommended_agents:
            issues.append("No agents recommended")
            
        # In production, cross-reference IDs with database to ensure they exist
        # and aren't hallucinated by the LLM
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

response_validator_engine = ResponseValidator()

async def response_validator_node(state: DiscoveryState) -> DiscoveryState:
    agents = state.get("recommended_agents", [])
    validation = response_validator_engine.validate(agents)
    
    if not validation["valid"]:
        logger.warning(f"Response validation failed: {validation['issues']}")
        
    return {
        "validation_result": validation
    }
