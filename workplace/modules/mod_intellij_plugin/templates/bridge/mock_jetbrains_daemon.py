"""
Mock JetBrains Daemon & JSON-RPC 2.0 Loopback Server
Simulates IntelliJ IDEA / PyCharm plugin interaction with the local Percipience daemon.
"""

import json
from typing import Dict, Any

class MockJetBrainsDaemon:
    """Simulates JSON-RPC 2.0 communication with IntelliJ plugin."""

    @staticmethod
    def handle_request(raw_payload: str) -> Dict[str, Any]:
        data = json.loads(raw_payload)
        req_id = data.get("id", 1)
        method = data.get("method")
        params = data.get("params", {})

        if method == "get_merkle_dag":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "status": "HEALTHY",
                    "merkle_height": 42,
                    "tip_hash": "3a7f8b9c0d1e2f3a4b5c6d7e8f9a0b1c"
                }
            }
        elif method == "execute_workflow":
            wf = params.get("workflow_id", "default")
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "workflow_id": wf,
                    "status": "COMPLETED",
                    "execution_time_ms": 234,
                    "merkle_block_id": "RP_INTELLIJ_PLUGIN_001"
                }
            }
        elif method == "calculate_token_savings":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "uncompressed_tokens": 1500,
                    "pruned_tokens": 450,
                    "reduction_pct": 70.0
                }
            }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }
