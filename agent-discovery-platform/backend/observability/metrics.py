from opentelemetry import metrics
import logging

logger = logging.getLogger(__name__)

# Initialize OTel meter
meter = metrics.get_meter("agent-discovery-meter")

# Define Harness metrics as per gap analysis
discovery_requests_total = meter.create_counter(
    "discovery_requests_total",
    description="Total number of discovery requests"
)

guardrail_violations_total = meter.create_counter(
    "guardrail_violations_total",
    description="Total number of guardrail violations (PII/Injection)"
)

feedback_submissions_total = meter.create_counter(
    "feedback_submissions_total",
    description="Total number of user feedback submissions"
)

model_cost_per_query = meter.create_histogram(
    "model_cost_per_query_dollars",
    description="Cost incurred per query due to LLM routing"
)

class MetricsService:
    @staticmethod
    def record_discovery_request(tenant_id: str):
        discovery_requests_total.add(1, {"tenant": tenant_id})
        
    @staticmethod
    def record_guardrail_violation(violation_type: str, action: str):
        guardrail_violations_total.add(1, {"type": violation_type, "action": action})
        
    @staticmethod
    def record_feedback(feedback_type: str):
        feedback_submissions_total.add(1, {"type": feedback_type})
        
    @staticmethod
    def record_cost(model: str, cost: float):
        model_cost_per_query.record(cost, {"model": model})

metrics_service = MetricsService()
