from fastapi import APIRouter, Depends
from backend.graph_db.knowledge_graph import KnowledgeGraphService

router = APIRouter()

@router.get("/dependencies/{agent_id}")
async def get_agent_dependencies(agent_id: str):
    return await KnowledgeGraphService.get_dependency_graph(agent_id)

@router.get("/impact/{tool_id}")
async def get_tool_impact(tool_id: str):
    return await KnowledgeGraphService.find_impact_radius(tool_id)
