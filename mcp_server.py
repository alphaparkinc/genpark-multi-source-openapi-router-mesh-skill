"""MCP Server for Multi-Source OpenAPI Router Mesh.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import MultiSourceOpenApiRouterMesh

mesh = MultiSourceOpenApiRouterMesh()

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "register_service",
                                "description": "Register OpenAPI specification with service namespace prefix",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "service_prefix": {"type": "string"},
                                        "spec": {"type": "object"}
                                    },
                                    "required": ["service_prefix", "spec"]
                                }
                            },
                            {
                                "name": "route_invocation",
                                "description": "Resolve namespaced operation ID to target endpoint metadata",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "namespaced_op_id": {"type": "string"}
                                    },
                                    "required": ["namespaced_op_id"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                call_name = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if call_name == "register_service":
                    res = mesh.register_service(args.get("service_prefix", ""), args.get("spec", {}))
                elif call_name == "route_invocation":
                    res = mesh.route_invocation(args.get("namespaced_op_id", ""))
                else:
                    res = {"error": "Unknown tool"}
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
