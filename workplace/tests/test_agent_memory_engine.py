#!/usr/bin/env python3
"""
Unit Test Suite for 3-Tier Persistent Agent Memory Architecture (TODO-AGT-03 / GAP-AGT-03)
Validates Working Memory isolation, Episodic Memory error signature recall (>0.85),
Semantic Memory conceptual lookup, and Merkle block memory consolidation.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for p in [REPO_ROOT / ".nb", REPO_ROOT / ".nb" / "core", REPO_ROOT / "workplace", REPO_ROOT / "workplace" / "core"]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from core.agent_memory_engine import AgentMemoryEngine


class TestAgentMemoryEngine(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        base = Path(self.tmp_dir.name)
        self.engine = AgentMemoryEngine(
            base_dir=base,
            working_dir=base / "working",
            episodic_dir=base / "episodic",
            semantic_dir=base / "semantic"
        )

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_01_working_memory_crud_and_isolation(self):
        """Validates working memory session isolation, updates, and eviction."""
        session_a = "sess_worker_101"
        session_b = "sess_worker_102"

        self.engine.set_working_memory(session_a, {
            "in_flight_hypotheses": ["AST symbol mismatch in auth.py"],
            "symbol_diffs": {"UserAuth": "modified"}
        })

        self.engine.set_working_memory(session_b, {
            "in_flight_hypotheses": ["Flaky test timeout in payment_gateway"],
            "symbol_diffs": {"ChargeService": "added"}
        })

        mem_a = self.engine.get_working_memory(session_a)
        mem_b = self.engine.get_working_memory(session_b)

        self.assertIn("AST symbol mismatch in auth.py", mem_a["in_flight_hypotheses"])
        self.assertIn("Flaky test timeout in payment_gateway", mem_b["in_flight_hypotheses"])

        # Update session A
        self.engine.update_working_memory(session_a, {
            "in_flight_hypotheses": ["Resolved by importing Optional"]
        })
        updated_a = self.engine.get_working_memory(session_a)
        self.assertEqual(len(updated_a["in_flight_hypotheses"]), 2)

        # Evict session A
        self.assertTrue(self.engine.evict_working_memory(session_a))
        evicted_a = self.engine.get_working_memory(session_a)
        self.assertEqual(len(evicted_a["in_flight_hypotheses"]), 0)

        # Session B remains intact
        self.assertEqual(len(self.engine.get_working_memory(session_b)["in_flight_hypotheses"]), 1)

    def test_02_episodic_memory_recording_and_high_recall(self):
        """Validates episodic memory persistence and recall > 0.85 on error signature matches."""
        target_sig = "TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'"

        self.engine.record_episode(
            task_id="task_calc_fix",
            error_signature=target_sig,
            root_cause="Uninitialized counter variable defaulting to None",
            patch_summary="Added `count = count or 0` before summation",
            resolution_status="RESOLVED"
        )

        self.engine.record_episode(
            task_id="task_network_retry",
            error_signature="ConnectionRefusedError: [Errno 61] Connection refused",
            root_cause="Local Redis mock was down",
            patch_summary="Started loopback container fixture",
            resolution_status="RESOLVED"
        )

        # Query with exact error signature
        results = self.engine.query_episodic_memory(
            query_text="TypeError addition NoneType",
            error_signature=target_sig,
            top_k=2
        )

        self.assertGreater(len(results), 0)
        top_match = results[0]
        self.assertEqual(top_match["task_id"], "task_calc_fix")
        # Recall / match score must exceed 0.85
        self.assertGreater(top_match["match_score"], 0.85)
        self.assertIn("Added `count = count or 0`", top_match["patch_summary"])

    def test_03_semantic_memory_concepts_lookup(self):
        """Validates semantic conceptual store lookups across tags and text."""
        # Store a custom domain concept
        self.engine.store_concept(
            concept_id="finops_token_share",
            title="15% Token Savings FinOps Rev-Share",
            description="All verified AST prunings record 15% token savings into customer revenue ledger.",
            rules=["Ledger entries must be sealed atomically in Merkle block."],
            tags=["finops", "billing", "tokens"]
        )

        lookup = self.engine.lookup_concepts(["billing"])
        self.assertGreaterEqual(len(lookup), 1)
        self.assertEqual(lookup[0]["concept_id"], "finops_token_share")

        # Built-in default concepts
        arch_lookup = self.engine.lookup_concepts(["quad_space"])
        self.assertGreaterEqual(len(arch_lookup), 1)
        self.assertEqual(arch_lookup[0]["concept_id"], "quad_space_architecture")

    def test_04_memory_consolidation_into_merkle_block(self):
        """Validates consolidating working scratchpad into episodic memory anchored by Merkle block hash."""
        session_id = "sess_consolidate_test"
        self.engine.set_working_memory(session_id, {
            "in_flight_hypotheses": ["Pipelined AST tree-sitter bindings"],
            "symbol_diffs": {"TreeSitterDaemon": "v1.2.0"},
            "step_returns": [{"status": "PASSED"}]
        })

        merkle_hash = "0015d5b593f30cbe_block_2393"
        episode = self.engine.consolidate_working_memory(session_id, merkle_block_hash=merkle_hash)

        self.assertIsNotNone(episode)
        self.assertEqual(episode["merkle_block_hash"], merkle_hash)
        self.assertIn("TreeSitterDaemon", episode["patch_summary"])

        # Working scratchpad must be evicted
        self.assertEqual(len(self.engine.get_working_memory(session_id)["in_flight_hypotheses"]), 0)


if __name__ == "__main__":
    unittest.main()
