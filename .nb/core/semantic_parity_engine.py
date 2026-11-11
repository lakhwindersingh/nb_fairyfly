#!/usr/bin/env python3
"""
workplace/core/semantic_parity_engine.py

Percipience Composite 6-Vector Semantic Parity Engine (CAP-09, CAP-26)
Calculates overall S_SP metric across AST symbols, wire contracts, TDD behaviors,
multi-agent handovers, living documentation, and supply-chain purity.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List
import hashlib
import json
import xml.etree.ElementTree as ET

from .contract_compatibility_checker import ContractCompatibilityChecker
from .living_doc_engine import LivingDocEngine
from .dependency_cve_sentinel import DependencyCVESentinel
from .merkle_engine import MerkleEngine
from .orchestrator_state_manager import OrchestratorStateManager
from .plan_dependency_resolver import PlanDependencyResolver
from .plan_handover import PlanHandoverVerifier


class SemanticParityEngine:
    """Evaluates 6-vector composite semantic parity score (S_SP)."""

    WEIGHTS = {
        "ast_symbols": 0.20,
        "wire_contracts": 0.25,
        "behavior_tests": 0.20,
        "handover_integrity": 0.15,
        "living_docs": 0.10,
        "supply_chain": 0.10
    }

    @classmethod
    def evaluate_ast_symbols(cls, workspace_root: Path) -> float:
        """AST parity has no verified evidence implementation yet; fail closed."""
        return 0.0

    @staticmethod
    def _read_hashed_artifact(workspace_root: Path, relative_path: str, expected_hash: str) -> bytes:
        root = Path(workspace_root).resolve()
        if not isinstance(relative_path, str) or not relative_path or Path(relative_path).is_absolute():
            raise ValueError("Evidence path must be workspace-relative")
        artifact = (root / relative_path).resolve()
        if not artifact.is_relative_to(root) or not artifact.is_file():
            raise ValueError("Evidence file is missing or outside the workspace")
        content = artifact.read_bytes()
        if not isinstance(expected_hash, str) or hashlib.sha256(content).hexdigest() != expected_hash:
            raise ValueError("Evidence hash mismatch")
        return content

    @staticmethod
    def _conservative_contract_compatibility(base: Dict[str, Any], head: Dict[str, Any]) -> bool:
        if not isinstance(base, dict) or not isinstance(head, dict):
            return False
        base_properties, head_properties = base.get("properties"), head.get("properties")
        base_required, head_required = base.get("required", []), head.get("required", [])
        if not isinstance(base_properties, dict) or not isinstance(head_properties, dict):
            return False
        if not isinstance(base_required, list) or not isinstance(head_required, list):
            return False
        if any(not isinstance(field, str) for field in base_required + head_required):
            return False
        if any(not isinstance(spec, dict) for spec in list(base_properties.values()) + list(head_properties.values())):
            return False
        if set(base_required) != set(head_required):
            return False
        if not set(base_required) <= set(base_properties):
            return False
        if {k: v for k, v in base.items() if k not in ("properties", "required")} != {
            k: v for k, v in head.items() if k not in ("properties", "required")
        }:
            return False
        if any(field not in head_properties or head_properties[field] != spec for field, spec in base_properties.items()):
            return False
        added_fields = set(head_properties) - set(base_properties)
        if added_fields and (base.get("additionalProperties") is not False or base.get("patternProperties")):
            return False
        return bool(ContractCompatibilityChecker.check_compatibility(base, head).get("is_compatible"))

    @classmethod
    def evaluate_wire_contracts(cls, workspace_root: Path) -> float:
        """Score explicit compatibility evidence; missing baselines fail closed."""
        evidence_path = workspace_root / ".nb" / "context" / "ledger" / "contract_compatibility_results.json"
        try:
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            checks = evidence.get("checks")
            if not isinstance(checks, list) or not checks:
                return 0.0
            for check in checks:
                if not isinstance(check, dict):
                    return 0.0
                base = json.loads(cls._read_hashed_artifact(
                    workspace_root, check.get("baseline_path"), check.get("baseline_sha256")
                ))
                head = json.loads(cls._read_hashed_artifact(
                    workspace_root, check.get("candidate_path"), check.get("candidate_sha256")
                ))
                if not cls._conservative_contract_compatibility(base, head):
                    return 0.0
            return 1.0
        except (OSError, ValueError, TypeError, KeyError):
            return 0.0

    @classmethod
    def evaluate_behavior_tests(cls, workspace_root: Path) -> float:
        """Score a complete test-run report rather than assuming tests passed."""
        evidence_path = workspace_root / ".nb" / "context" / "ledger" / "test_results.json"
        try:
            evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
            report = cls._read_hashed_artifact(
                workspace_root, evidence.get("junit_path"), evidence.get("junit_sha256")
            )
            root = ET.fromstring(report)
            suites = [root] if root.tag == "testsuite" else list(root) if root.tag == "testsuites" else []
            if not suites or any(suite.tag != "testsuite" for suite in suites):
                return 0.0
            total = 0
            passed = 0
            for suite in suites:
                tests = int(suite.attrib["tests"])
                failures = int(suite.get("failures", 0))
                errors = int(suite.get("errors", 0))
                skipped = int(suite.get("skipped", 0))
                if min(tests, failures, errors, skipped) < 0 or failures + errors + skipped > tests:
                    return 0.0
                test_cases = suite.findall(".//testcase")
                if (
                    len(test_cases) != tests
                    or sum(case.find("failure") is not None for case in test_cases) != failures
                    or sum(case.find("error") is not None for case in test_cases) != errors
                    or sum(case.find("skipped") is not None for case in test_cases) != skipped
                ):
                    return 0.0
                total += tests
                passed += tests - failures - errors - skipped
            return 1.0 if total > 0 and passed == total else 0.0
        except (OSError, ValueError, TypeError, KeyError, ET.ParseError):
            return 0.0

    @classmethod
    def evaluate_handover_integrity(cls, workspace_root: Path) -> float:
        """Validate persisted plan handovers against specs, artifacts, and Merkle RPs."""
        ledger_path = workspace_root / ".nb" / "context" / "ledger" / "plan_handovers.json"
        try:
            payload = json.loads(ledger_path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                return 0.0
            handovers = payload.get("handovers")
            if payload.get("schema_version") != PlanHandoverVerifier.SCHEMA_VERSION:
                return 0.0
            if not isinstance(handovers, list) or not handovers:
                return 0.0

            resolver = PlanDependencyResolver(workspace_root / ".nb" / "plan")
            by_plan_id = {}
            for entry in handovers:
                if not isinstance(entry, dict) or not isinstance(entry.get("plan_id"), str):
                    return 0.0
                if entry["plan_id"] in by_plan_id:
                    return 0.0
                by_plan_id[entry["plan_id"]] = entry.get("handover")

            target_plan_id = payload.get("target_plan_id")
            if not isinstance(target_plan_id, str) or not target_plan_id:
                return 0.0
            state_path = OrchestratorStateManager.target_state_path(workspace_root, target_plan_id)
            state = OrchestratorStateManager(str(state_path)).load_and_verify_state()
            if not state or state.get("target_plan_id") != target_plan_id:
                return 0.0
            completed_steps = state.get("completed_steps")
            if not isinstance(completed_steps, list):
                return 0.0
            signed_handovers = {}
            for record in completed_steps:
                if not isinstance(record, dict) or record.get("status") != "SUCCESS":
                    return 0.0
                plan_id = record.get("plan_id")
                handover = record.get("handover")
                if (
                    not isinstance(plan_id, str)
                    or plan_id in signed_handovers
                    or record.get("step_id") != f"plan:{plan_id}"
                    or not isinstance(handover, dict)
                    or record.get("recovery_point") != handover.get("recovery_point_id")
                ):
                    return 0.0
                signed_handovers[plan_id] = handover
            if signed_handovers != by_plan_id:
                return 0.0
            target_closure = resolver.resolve(target_plan_id)
            if set(by_plan_id) != {plan["plan_id"] for plan in target_closure}:
                return 0.0

            for plan in target_closure:
                plan_id = plan["plan_id"]
                handover = by_plan_id[plan_id]
                prerequisites = {
                    dependency_id: by_plan_id[dependency_id]
                    for dependency_id in plan["dependency_ids"]
                    if dependency_id in by_plan_id
                }
                valid, _ = PlanHandoverVerifier.validate_handover(
                    handover,
                    plan,
                    workspace_root,
                    prerequisites,
                    lambda recovery_point: MerkleEngine.verify_recovery_point(workspace_root, recovery_point),
                )
                if not valid:
                    return 0.0
            return 1.0
        except (OSError, ValueError, TypeError, KeyError):
            return 0.0

    @classmethod
    def evaluate_living_docs(cls, workspace_root: Path) -> float:
        """Evaluates living doc synchronization and Mermaid syntax validity."""
        doc_res = LivingDocEngine.sync_all_docs(workspace_root)
        if doc_res.get("all_mermaid_valid") and doc_res.get("generated_count", 0) > 0:
            return 1.00
        return 0.65

    @classmethod
    def evaluate_supply_chain(cls, workspace_root: Path) -> float:
        """Evaluates supply chain purity and dependency CVEs."""
        req_file = workspace_root / "requirements.txt"
        manifest = req_file.read_text(encoding="utf-8") if req_file.exists() else "fastapi==0.110.0\npydantic==2.6.4\npytest==8.4.1"
        cve_res = DependencyCVESentinel.audit_manifest(manifest, "python")
        return 1.00 if cve_res.get("clean") else 0.50

    @classmethod
    def compute_parity_report(cls, workspace_root: Path) -> Dict[str, Any]:
        """Computes composite S_SP and returns structured scorecard."""
        s_ast = cls.evaluate_ast_symbols(workspace_root)
        s_contract = cls.evaluate_wire_contracts(workspace_root)
        s_tests = cls.evaluate_behavior_tests(workspace_root)
        s_handover = cls.evaluate_handover_integrity(workspace_root)
        s_docs = cls.evaluate_living_docs(workspace_root)
        s_supply = cls.evaluate_supply_chain(workspace_root)

        s_sp = (
            cls.WEIGHTS["ast_symbols"] * s_ast +
            cls.WEIGHTS["wire_contracts"] * s_contract +
            cls.WEIGHTS["behavior_tests"] * s_tests +
            cls.WEIGHTS["handover_integrity"] * s_handover +
            cls.WEIGHTS["living_docs"] * s_docs +
            cls.WEIGHTS["supply_chain"] * s_supply
        )

        if s_sp >= 0.95:
            classification = "ALIGNED_MERGE_READY"
            color = "GREEN"
            action_required = "None. Safe for PR merge and Merkle sealing."
        elif s_sp >= 0.85:
            classification = "RECONCILIATION_REQUIRED"
            color = "AMBER"
            action_required = "Trigger Dual-Reconciliation Loop (Revert or Evolve mode)."
        else:
            classification = "CRITICAL_DRIFT_QUARANTINED"
            color = "RED"
            action_required = "Immediate surgical rollback to Recovery Point RP_k."

        return {
            "composite_s_sp": round(s_sp, 4),
            "classification": classification,
            "color": color,
            "action_required": action_required,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "vector_scores": {
                "ast_symbols": {"score": s_ast, "weight": cls.WEIGHTS["ast_symbols"]},
                "wire_contracts": {"score": s_contract, "weight": cls.WEIGHTS["wire_contracts"]},
                "behavior_tests": {"score": s_tests, "weight": cls.WEIGHTS["behavior_tests"]},
                "handover_integrity": {"score": s_handover, "weight": cls.WEIGHTS["handover_integrity"]},
                "living_docs": {"score": s_docs, "weight": cls.WEIGHTS["living_docs"]},
                "supply_chain": {"score": s_supply, "weight": cls.WEIGHTS["supply_chain"]}
            }
        }
