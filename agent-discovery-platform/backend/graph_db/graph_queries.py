SYNC_AGENT_QUERY = """
MERGE (a:Agent {id: $agent.id})
SET a.name = $agent.name,
    a.description = $agent.description,
    a.status = $agent.status,
    a.category = $agent.category

WITH a
UNWIND $agent.capabilities AS cap
MERGE (c:Capability {name: cap})
MERGE (a)-[:HAS_CAPABILITY]->(c)

WITH a
UNWIND $agent.dependencies AS dep
MERGE (d:Agent {id: dep})
MERGE (a)-[:DEPENDS_ON]->(d)

WITH a
MATCH (t:Team {id: $agent.team_id})
MERGE (a)-[:OWNED_BY]->(t)
"""

SYNC_MCP_SERVER_QUERY = """
MERGE (s:MCPServer {id: $server.id})
SET s.name = $server.name,
    s.status = $server.status

WITH s
MATCH (t:Team {id: $server.team_id})
MERGE (s)-[:OWNED_BY]->(t)
"""

SYNC_TOOL_QUERY = """
MERGE (t:Tool {id: $tool.id})
SET t.name = $tool.name

WITH t
MATCH (s:MCPServer {id: $tool.server_id})
MERGE (s)-[:EXPOSES]->(t)
"""

SYNC_TEAM_QUERY = """
MERGE (t:Team {id: $team.id})
SET t.name = $team.name,
    t.department = $team.department
"""

GET_DEPENDENCY_GRAPH_QUERY = """
MATCH (a:Agent {id: $agent_id})-[r*1..3]-(n)
RETURN a, r, n
"""

FIND_RELATED_AGENTS_QUERY = """
MATCH (a:Agent {id: $agent_id})-[:HAS_CAPABILITY]->(c:Capability)<-[:HAS_CAPABILITY]-(related:Agent)
RETURN related, collect(c.name) AS shared_capabilities, count(c) AS similarity_score
ORDER BY similarity_score DESC
LIMIT 10
"""

FIND_IMPACT_RADIUS_QUERY = """
MATCH (t:Tool {id: $tool_id})<-[:USES*1..3]-(a:Agent)
RETURN DISTINCT a
"""

SHORTEST_PATH_QUERY = """
MATCH p = shortestPath((a1:Agent {id: $source_id})-[:DEPENDS_ON|USES*..5]-(a2:Agent {id: $target_id}))
RETURN p
"""
