"""Example usage for Multi-Source OpenAPI Router Mesh."""
from client import MultiSourceOpenApiRouterMesh
import json

mesh = MultiSourceOpenApiRouterMesh()

mesh.register_service("crm", {
    "paths": {"/customers/{id}": {"get": {"operationId": "get_customer", "summary": "Get customer by ID"}}}
})

mesh.register_service("billing", {
    "paths": {"/invoices": {"post": {"operationId": "create_invoice", "summary": "Issue invoice"}}}
})

target = mesh.route_invocation("crm_get_customer")
print(json.dumps(target, indent=2))
