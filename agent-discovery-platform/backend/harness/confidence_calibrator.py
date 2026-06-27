from backend.agents.state import DiscoveryState
import logging

logger = logging.getLogger(__name__)

class ConfidenceCalibrator:
    """Calculates overall confidence based on multiple pipeline signals."""
    
    def calibrate(self, state: DiscoveryState) -> dict:
        # Mock Bayesian calibration
        intent_conf = state.get("intent", {}).get("confidence", 0.5)
        eval_score = state.get("quality_score", 0.5)
        
        # If evaluation says it's good, and intent was confident, we are highly confident
        overall = (intent_conf * 0.4) + (eval_score * 0.6)
        
        return {
            "overall": overall,
            "intent_confidence": intent_conf,
            "evaluation_score": eval_score
        }

confidence_calibrator = ConfidenceCalibrator()

async def confidence_calibrator_node(state: DiscoveryState) -> DiscoveryState:
    scores = confidence_calibrator.calibrate(state)
    return {
        "confidence_scores": scores
    }
