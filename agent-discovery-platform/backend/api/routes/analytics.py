from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_metrics():
    return {
        "total_discoveries": 1024,
        "reuse_rate": 0.45,
        "cost_saved_usd": 125000,
        "top_agents": ["customer-support-agent", "hr-policy-assistant"]
    }
