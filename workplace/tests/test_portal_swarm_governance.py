"""
Integration Test Suite for Percipience Cloud SaaS Portal:
Swarm Topologies, Autonomous Multi-Agent Coordination & Cryptographic Governance (Section 17.1):
- GAP-AGT-01: Dynamic Task DAGs & Runtime Sub-Goal Expansion (/api/swarm/dynamic-dag, /api/swarm/dynamic-dag/simulate)
- GAP-AGT-02: Structured Multi-Pass Reflexion & 5-Pillar Critic Verification (/api/swarm/reflexion/evaluate)
- GAP-AGT-03: 3-Tier Persistent Memory Engine (/api/swarm/memory/status, /api/swarm/memory/episodic, /api/swarm/memory/consolidate)
- GAP-AGT-04: Declarative Tool Contracts & JSON Schema Draft-07 Validation (/api/swarm/tools, /api/swarm/tools/validate-execute)
- GAP-AGT-05: Capability-Based Access Control (CBAC) Sandbox Tokens (/api/swarm/cbac/mint, /api/swarm/cbac/verify-access)
"""

import sys
import json
import threading
import time
from pathlib import Path
from http.client import HTTPConnection
from http.server import HTTPServer

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "workplace") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "workplace"))

import pytest
from portal.server import PortalRequestHandler


@pytest.fixture(scope="module")
def portal_server():
    """Spins up a lightweight ephemeral instance of PortalRequestHandler."""
    server = HTTPServer(("127.0.0.1", 0), PortalRequestHandler)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.1)
    yield f"127.0.0.1:{port}"
    server.shutdown()


def test_swarm_tab_in_html(portal_server):
    """Verifies that the HTML portal page renders Tab 15 and swarm navigation button."""
    conn = HTTPConnection(portal_server)
    conn.request("GET", "/")
    res = conn.getresponse()
    assert res.status == 200
    html = res.read().decode("utf-8")
    assert 'id="swarmNavBtn"' in html
    assert 'id="swarm-governance"' in html
    assert 'GAP-AGT-01: Dynamic Task DAGs' in html
    assert 'GAP-AGT-02: Structured Multi-Pass Reflexion' in html
    assert 'GAP-AGT-03: 3-Tier Persistent Memory Engine' in html
    assert 'GAP-AGT-04: Declarative Tool Contracts' in html
    assert 'GAP-AGT-05: Capability-Based Access Control' in html


def test_dynamic_dag_api(portal_server):
    """Tests GET /api/swarm/dynamic-dag for structure, topological ordering, and limits."""
    conn = HTTPConnection(portal_server)
    conn.request("GET", "/api/swarm/dynamic-dag")
    res = conn.getresponse()
    assert res.status == 200
    data = json.loads(res.read().decode("utf-8"))
    assert data["status"] == "SUCCESS"
    assert "percipience_swarm_pipeline" in data["dag_id"]
    assert len(data["nodes"]) >= 4
    assert len(data["topological_order"]) >= 4
    assert data["max_depth"] == 3
    assert data["max_steps"] == 20


def test_dynamic_dag_simulate_expand_and_reset(portal_server):
    """Tests POST /api/swarm/dynamic-dag/simulate with runtime sub-goal expansion and reset."""
    conn = HTTPConnection(portal_server)

    # 1. Reset first to ensure clean state
    conn.request(
        "POST",
        "/api/swarm/dynamic-dag/simulate",
        body=json.dumps({"action": "reset"}),
        headers={"Content-Type": "application/json"}
    )
    res = conn.getresponse()
    assert res.status == 200
    reset_data = json.loads(res.read().decode("utf-8"))
    assert reset_data["status"] == "SUCCESS"
    assert len(reset_data["nodes"]) == 4

    # 2. Expand sub-goals under step_code_derivation
    payload = {
        "action": "expand",
        "parent_step_id": "step_code_derivation",
        "subgoals": [
            {"id": "step_code_derivation_ast_strict_typing", "action": "ast_strict_typing", "name": "AST Strict Typing"},
            {"id": "step_code_derivation_reflexion_critic", "action": "reflexion_critic", "name": "Reflexion Critic"}
        ]
    }
    conn.request(
        "POST",
        "/api/swarm/dynamic-dag/simulate",
        body=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )
    res = conn.getresponse()
    assert res.status == 200
    expand_data = json.loads(res.read().decode("utf-8"))
    assert expand_data["status"] == "SUCCESS"
    assert len(expand_data["created_ids"]) == 2
    assert "step_code_derivation_ast_strict_typing" in expand_data["topological_order"]
    assert "step_code_derivation_reflexion_critic" in expand_data["topological_order"]

    # 3. Simulate execution
    conn.request(
        "POST",
        "/api/swarm/dynamic-dag/simulate",
        body=json.dumps({"action": "simulate_execution"}),
        headers={"Content-Type": "application/json"}
    )
    res = conn.getresponse()
    assert res.status == 200
    exec_data = json.loads(res.read().decode("utf-8"))
    assert exec_data["status"] == "SUCCESS"
    assert exec_data["execution_result"]["status"] in ("SUCCESS", "COMPLETED")


def test_reflexion_critic_evaluation(portal_server):
    """Tests POST /api/swarm/reflexion/evaluate across 5 pillars."""
    conn = HTTPConnection(portal_server)

    # Clean compliant code
    clean_code = '''
def process_settlement(account_id: str, amount_usd: float) -> bool:
    if not account_id or amount_usd <= 0:
        raise ValueError("Invalid parameters")
    try:
        return True
    except Exception:
        return False
'''
    conn.request(
        "POST",
        "/api/swarm/reflexion/evaluate",
        body=json.dumps({"code_or_artifact": clean_code, "task_context": {"task": "settlement"}}),
        headers={"Content-Type": "application/json"}
    )
    res = conn.getresponse()
    assert res.status == 200
    data = json.loads(res.read().decode("utf-8"))
    assert data["status"] == "SUCCESS"
    critique = data["critique"]
    assert "pillar_scores" in critique
    assert "wire_contract_conformity" in critique["pillar_scores"]
    assert "convergence_score" in critique

    # Defective code (missing types, error handling, defensive guards)
    bad_code = "def bad(x): return x"
    conn.request(
        "POST",
        "/api/swarm/reflexion/evaluate",
        body=json.dumps({"code_or_artifact": bad_code, "task_context": {}}),
        headers={"Content-Type": "application/json"}
    )
    res = conn.getresponse()
    assert res.status == 200
    bad_data = json.loads(res.read().decode("utf-8"))
    assert bad_data["status"] == "SUCCESS"
    bad_critique = bad_data["critique"]
    assert bad_critique["passes_invariants"] is False
    assert len(bad_critique["defects_found"]) > 0


def test_memory_api_status_and_episodic_search(portal_server):
    """Tests GET /api/swarm/memory/status, /api/swarm/memory/episodic, and /api/swarm/memory/semantic."""
    conn = HTTPConnection(portal_server)

    # 1. Status
    conn.request("GET", "/api/swarm/memory/status")
    res = conn.getresponse()
    assert res.status == 200
    status_data = json.loads(res.read().decode("utf-8"))
    assert status_data["status"] == "SUCCESS"
    assert status_data["episodes_count"] >= 1
    assert status_data["concepts_count"] >= 2

    # 2. Episodic query
    conn.request("GET", "/api/swarm/memory/episodic?q=bootstrap&limit=3")
    res = conn.getresponse()
    assert res.status == 200
    ep_data = json.loads(res.read().decode("utf-8"))
    assert ep_data["status"] == "SUCCESS"
    assert len(ep_data["episodes"]) >= 1

    # 3. Semantic query
    conn.request("GET", "/api/swarm/memory/semantic?tags=dag,security")
    res = conn.getresponse()
    assert res.status == 200
    sem_data = json.loads(res.read().decode("utf-8"))
    assert sem_data["status"] == "SUCCESS"
    assert len(sem_data["concepts"]) >= 1


def test_memory_working_consolidation(portal_server):
    """Tests POST /api/swarm/memory/consolidate to seal working memory into episodic & Merkle block."""
    conn = HTTPConnection(portal_server)
    payload = {
        "session_id": "session_test_integration",
        "merkle_block_hash": "0000testblockhash"
    }
    conn.request(
        "POST",
        "/api/swarm/memory/consolidate",
        body=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )
    res = conn.getresponse()
    assert res.status == 200
    data = json.loads(res.read().decode("utf-8"))
    assert data["status"] == "SUCCESS"
    consolidation = data["consolidation"]
    assert consolidation["merkle_block_hash"] == "0000testblockhash"
    assert "session_test_integration" in consolidation["task_id"]


def test_tools_catalog_and_validation(portal_server):
    """Tests GET /api/swarm/tools and POST /api/swarm/tools/validate-execute."""
    conn = HTTPConnection(portal_server)

    # 1. Tools list
    conn.request("GET", "/api/swarm/tools")
    res = conn.getresponse()
    assert res.status == 200
    tools_data = json.loads(res.read().decode("utf-8"))
    assert tools_data["status"] == "SUCCESS"
    tool_names = [t["name"] for t in tools_data["tools"]]
    assert "ast_pruner" in tool_names
    assert "contract_checker" in tool_names
    assert "merkle_auditor" in tool_names
    assert "cve_sentinel" in tool_names

    # 2. Valid execution: ast_pruner
    conn.request(
        "POST",
        "/api/swarm/tools/validate-execute",
        body=json.dumps({
            "tool_name": "ast_pruner",
            "args": {"source_code": "def compute(): pass", "language": "python"}
        }),
        headers={"Content-Type": "application/json"}
    )
    res = conn.getresponse()
    assert res.status == 200
    exec_data = json.loads(res.read().decode("utf-8"))
    assert exec_data["status"] == "SUCCESS"
    assert exec_data["tool_result"]["status"] == "SUCCESS"
    assert exec_data["tool_result"]["result"]["reduction_pct"] > 0

    # 3. Invalid schema arguments (missing required language) -> 400
    conn.request(
        "POST",
        "/api/swarm/tools/validate-execute",
        body=json.dumps({
            "tool_name": "ast_pruner",
            "args": {"source_code": "def compute(): pass"}
        }),
        headers={"Content-Type": "application/json"}
    )
    res = conn.getresponse()
    assert res.status == 400


def test_cbac_token_minting_and_sandbox_verification(portal_server):
    """Tests POST /api/swarm/cbac/mint and POST /api/swarm/cbac/verify-access."""
    conn = HTTPConnection(portal_server)

    # 1. Mint token
    mint_payload = {
        "agent_id": "agent_test_runner",
        "worktree_path": str(REPO_ROOT),
        "allowed_operations": ["CAP_FS_READ", "CAP_FS_WRITE_MODULE_ONLY", "CAP_EXEC_SUBPROCESS"],
        "ttl_seconds": 1800
    }
    conn.request(
        "POST",
        "/api/swarm/cbac/mint",
        body=json.dumps(mint_payload),
        headers={"Content-Type": "application/json"}
    )
    res = conn.getresponse()
    assert res.status == 200
    mint_data = json.loads(res.read().decode("utf-8"))
    assert mint_data["status"] == "SUCCESS"
    token = mint_data["token"]
    assert "." in token

    # 2. Check permitted filesystem access
    conn.request(
        "POST",
        "/api/swarm/cbac/verify-access",
        body=json.dumps({
            "token": token,
            "check_type": "fs",
            "target_path": str(REPO_ROOT / "workplace/core/candidate.py"),
            "operation": "write"
        }),
        headers={"Content-Type": "application/json"}
    )
    res = conn.getresponse()
    assert res.status == 200
    fs_ok = json.loads(res.read().decode("utf-8"))
    assert fs_ok["allowed"] is True

    # 3. Check blocked filesystem access to protected .nb/core
    conn.request(
        "POST",
        "/api/swarm/cbac/verify-access",
        body=json.dumps({
            "token": token,
            "check_type": "fs",
            "target_path": str(REPO_ROOT / ".nb/core/protected_kernel.py"),
            "operation": "write"
        }),
        headers={"Content-Type": "application/json"}
    )
    res = conn.getresponse()
    assert res.status == 200
    fs_blocked = json.loads(res.read().decode("utf-8"))
    assert fs_blocked["allowed"] is False
    assert "PERMISSION_DENIED" in fs_blocked["reason"]

    # 4. Check whitelisted subprocess command
    conn.request(
        "POST",
        "/api/swarm/cbac/verify-access",
        body=json.dumps({
            "token": token,
            "check_type": "subprocess",
            "command": "pytest workplace/tests"
        }),
        headers={"Content-Type": "application/json"}
    )
    res = conn.getresponse()
    assert res.status == 200
    subproc_ok = json.loads(res.read().decode("utf-8"))
    assert subproc_ok["allowed"] is True

    # 5. Check blocked dangerous subprocess command
    conn.request(
        "POST",
        "/api/swarm/cbac/verify-access",
        body=json.dumps({
            "token": token,
            "check_type": "subprocess",
            "command": "rm -rf /tmp"
        }),
        headers={"Content-Type": "application/json"}
    )
    res = conn.getresponse()
    assert res.status == 200
    subproc_blocked = json.loads(res.read().decode("utf-8"))
    assert subproc_blocked["allowed"] is False
    assert "PERMISSION_DENIED" in subproc_blocked["reason"]

    # 6. Check network egress without CAP_NET_EGRESS
    conn.request(
        "POST",
        "/api/swarm/cbac/verify-access",
        body=json.dumps({
            "token": token,
            "check_type": "network",
            "host": "api.github.com",
            "port": 443
        }),
        headers={"Content-Type": "application/json"}
    )
    res = conn.getresponse()
    assert res.status == 200
    net_blocked = json.loads(res.read().decode("utf-8"))
    assert net_blocked["allowed"] is False
    assert "CAP_NETWORK_EGRESS" in net_blocked["reason"] or "CAP_NET_EGRESS" in net_blocked["reason"]
