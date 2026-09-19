"""
Synthetic Virtual LSP 3.17 Protocol Fixture Generator for Offline CI Testing
"""

import time
from typing import Dict, Any, List

class VirtualLspFixture:
    """Generates synthetic LSP 3.17 request/response payloads for offline verification."""

    @staticmethod
    def simulate_document_diagnostics(contract_text: str, uri: str = "file:///.nb/context/contracts/test.yaml") -> Dict[str, Any]:
        start = time.time()
        diagnostics = []

        if "contract_id" not in contract_text and "$schema" not in contract_text:
            diagnostics.append({
                "range": {
                    "start": {"line": 0, "character": 0},
                    "end": {"line": 0, "character": 10}
                },
                "severity": 1, # Error
                "source": "percipience-lsp",
                "message": "Missing required contract_id or $schema in contract definition"
            })

        duration_ms = (time.time() - start) * 1000

        return {
            "uri": uri,
            "diagnostics": diagnostics,
            "latency_ms": round(duration_ms, 2),
            "is_valid": len(diagnostics) == 0
        }

    @staticmethod
    def generate_codelens_response(uri: str) -> List[Dict[str, Any]]:
        return [
            {
                "range": {
                    "start": {"line": 0, "character": 0},
                    "end": {"line": 0, "character": 0}
                },
                "command": {
                    "title": "▶ Run Percipience Verification Workflow",
                    "command": "percipience.executeWorkflow",
                    "arguments": ["vscode_plugin_delivery_flow"]
                }
            }
        ]
