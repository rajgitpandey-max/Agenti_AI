import re
import logging
from backend.agents.state import DiscoveryState
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GuardrailsManager:
    """Manages input/output safety, PII detection, and injection defense."""
    
    # Very basic PII mock (in production use Presidio or similar)
    SSN_PATTERN = re.compile(r'\d{3}-\d{2}-\d{4}')
    EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    
    INJECTION_KEYWORDS = ["ignore previous instructions", "system prompt", "bypass"]
    
    def check_input(self, query: str) -> Dict[str, Any]:
        """Detect PII and injections in input query."""
        violations = []
        sanitized = query
        
        # Check Injection
        for kw in self.INJECTION_KEYWORDS:
            if kw in query.lower():
                violations.append("prompt_injection")
                break
                
        # Check PII
        if self.SSN_PATTERN.search(query):
            violations.append("pii_ssn")
            sanitized = self.SSN_PATTERN.sub("[REDACTED_SSN]", sanitized)
            
        if self.EMAIL_PATTERN.search(query):
            violations.append("pii_email")
            sanitized = self.EMAIL_PATTERN.sub("[REDACTED_EMAIL]", sanitized)
            
        return {
            "safe": len(violations) == 0,
            "violations": violations,
            "sanitized_query": sanitized
        }
        
    def check_output(self, response_text: str) -> Dict[str, Any]:
        """Detect PII leakage or toxic content in output."""
        violations = []
        
        if self.SSN_PATTERN.search(response_text) or self.EMAIL_PATTERN.search(response_text):
            violations.append("pii_leakage")
            
        return {
            "safe": len(violations) == 0,
            "violations": violations
        }

guardrails_manager = GuardrailsManager()

async def input_guardrail_node(state: DiscoveryState) -> DiscoveryState:
    query = state["user_query"]
    result = guardrails_manager.check_input(query)
    
    # In production, we would log audit events for violations here
    
    if not result["safe"] and "prompt_injection" in result["violations"]:
        logger.warning("Prompt injection detected. Halting pipeline.")
        return {
            "input_guardrail_result": result,
            "sanitized_query": result["sanitized_query"],
            "errors": ["Query blocked by security guardrails."]
        }
        
    return {
        "input_guardrail_result": result,
        "sanitized_query": result["sanitized_query"]
    }

async def output_guardrail_node(state: DiscoveryState) -> DiscoveryState:
    # Just a stub implementation for the node, although the response validation node handles most of the output.
    return {"output_guardrail_result": {"safe": True, "violations": []}}
