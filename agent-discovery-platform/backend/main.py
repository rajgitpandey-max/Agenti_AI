import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings

# Import routers
from backend.api.routes import discovery, feedback, agents, mcp, graph, governance, analytics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For MVP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(discovery.router, prefix=f"{settings.API_V1_STR}/discovery", tags=["discovery"])
app.include_router(feedback.router, prefix=f"{settings.API_V1_STR}/feedback", tags=["feedback"])
app.include_router(agents.router, prefix=f"{settings.API_V1_STR}/agents", tags=["agents"])
app.include_router(mcp.router, prefix=f"{settings.API_V1_STR}/mcp", tags=["mcp"])
app.include_router(graph.router, prefix=f"{settings.API_V1_STR}/graph", tags=["graph"])
app.include_router(governance.router, prefix=f"{settings.API_V1_STR}/governance", tags=["governance"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}
