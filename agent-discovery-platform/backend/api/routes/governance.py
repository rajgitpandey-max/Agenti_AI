from fastapi import APIRouter
from backend.harness.guardrails import guardrails_manager

router = APIRouter()

@router.get("/guardrail-audit")
async def get_guardrail_audits():
    # Mock fetching audit logs from DB
    return [
        {"timestamp": "2023-10-27T10:00:00Z", "violation_type": "pii_ssn", "action_taken": "sanitized"}
    ]
