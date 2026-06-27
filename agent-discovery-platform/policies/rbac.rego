package discovery.rbac

default allow = false

# Platform admins can do anything
allow {
    "platform_admin" == input.user.roles[_]
}

# Tenant admins can manage resources in their tenant
allow {
    "tenant_admin" == input.user.roles[_]
    input.user.tenant_id == input.resource.tenant_id
}

# Developers can read/discover
allow {
    "developer" == input.user.roles[_]
    input.action == "read"
}
