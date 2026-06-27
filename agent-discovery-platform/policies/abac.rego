package discovery.abac

default allow = false

# Allow if the user belongs to the same tenant as the resource
allow {
    input.user.tenant_id == input.resource.tenant_id
}

# Allow if the agent classification is PUBLIC
allow {
    input.resource.type == "agent"
    input.resource.classification == "PUBLIC"
}

# Restrict CONFIDENTIAL agents to specific teams
allow {
    input.resource.type == "agent"
    input.resource.classification == "CONFIDENTIAL"
    input.user.team_id == input.resource.team_id
}
