"""
Mock VSCode IPC Host & JSON-RPC Loopback Socket Server
Simulates VSCode extension host interaction with the local Percipience daemon.
"""

import json
from typing import Dict, Any

class MockVsCodeIpcHost:
    """Simulates IPC exchange between VSCode extension host and Percipience daemon."""

    @staticmethod
    def handle_message(message_dict: Dict[str, Any]) -> Dict[str, Any]:
        command = message_dict.get("command")
        req_id = message_dict.get("requestId", "req_001")

        if command == "fetch_merkle_state":
            return {
                "responseId": req_id,
                "status": "SUCCESS",
                "data": {
                    "chain_valid": True,
                    "tip_hash": "3a7f8b9c0d1e2f3a4b5c6d7e8f9a0b1c",
                    "merkle_height": 42
                }
            }
        elif command == "execute_workflow":
            payload = message_dict.get("payload", {})
            wf = payload.get("workflow_id", "vscode_plugin_delivery_flow")
            return {
                "responseId": req_id,
                "status": "SUCCESS",
                "data": {
                    "workflow_id": wf,
                    "status": "COMPLETED",
                    "sealed_block": "RP_VSCODE_PLUGIN_001"
                }
            }
        elif command == "fetch_token_savings":
            return {
                "responseId": req_id,
                "status": "SUCCESS",
                "data": {
                    "uncompressed": 2500,
                    "pruned": 750,
                    "saved_pct": 70.0
                }
            }
        else:
            return {
                "responseId": req_id,
                "status": "ERROR",
                "error": f"Unknown command: {command}"
            }
