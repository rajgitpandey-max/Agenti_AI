from backend.graph_db.neo4j_client import neo4j_client
from backend.graph_db.graph_queries import (
    SYNC_AGENT_QUERY,
    SYNC_MCP_SERVER_QUERY,
    SYNC_TOOL_QUERY,
    SYNC_TEAM_QUERY,
    GET_DEPENDENCY_GRAPH_QUERY,
    FIND_RELATED_AGENTS_QUERY,
    FIND_IMPACT_RADIUS_QUERY,
    SHORTEST_PATH_QUERY
)

class KnowledgeGraphService:
    @staticmethod
    async def sync_agent(agent_data: dict):
        return await neo4j_client.execute_query(SYNC_AGENT_QUERY, {"agent": agent_data})

    @staticmethod
    async def sync_mcp_server(mcp_data: dict):
        return await neo4j_client.execute_query(SYNC_MCP_SERVER_QUERY, {"server": mcp_data})

    @staticmethod
    async def sync_tool(tool_data: dict):
        return await neo4j_client.execute_query(SYNC_TOOL_QUERY, {"tool": tool_data})

    @staticmethod
    async def sync_team(team_data: dict):
        return await neo4j_client.execute_query(SYNC_TEAM_QUERY, {"team": team_data})

    @staticmethod
    async def get_dependency_graph(agent_id: str):
        result = await neo4j_client.execute_query(GET_DEPENDENCY_GRAPH_QUERY, {"agent_id": agent_id})
        return result

    @staticmethod
    async def find_related_agents(agent_id: str):
        result = await neo4j_client.execute_query(FIND_RELATED_AGENTS_QUERY, {"agent_id": agent_id})
        return result

    @staticmethod
    async def find_impact_radius(tool_id: str):
        result = await neo4j_client.execute_query(FIND_IMPACT_RADIUS_QUERY, {"tool_id": tool_id})
        return result

    @staticmethod
    async def shortest_path(source_agent_id: str, target_agent_id: str):
        result = await neo4j_client.execute_query(SHORTEST_PATH_QUERY, {
            "source_id": source_agent_id,
            "target_id": target_agent_id
        })
        return result
