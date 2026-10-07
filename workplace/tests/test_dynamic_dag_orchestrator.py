#!/usr/bin/env python3
"""
Unit Test Suite for Dynamic Task DAGs & Runtime Sub-Goal Expansion (TODO-AGT-01 / GAP-AGT-01)
Validates runtime DAG mutation, topological sorting, blast-radius subgraphs,
backtracking, and graph invariant ceilings.
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

from core.dynamic_dag_orchestrator import (
    DynamicDAGOrchestrator,
    StepNode,
    DAGConstraintViolationError,
    CycleDetectedError
)


class TestDynamicDAGOrchestrator(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.trace_path = Path(self.tmp_dir.name) / "dynamic_dag_traces.jsonl"
        self.orchestrator = DynamicDAGOrchestrator(
            dag_id="test_dag",
            max_depth=3,
            max_steps=10,
            trace_log_path=self.trace_path
        )

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_01_initial_load_and_topological_sort(self):
        """Validates loading initial nodes and computing Kahn topological order."""
        dag_def = {
            "dag_id": "sdlc_pipeline",
            "nodes": [
                {"id": "step_a", "action": "fetch_spec", "dependencies": []},
                {"id": "step_b", "action": "generate_code", "dependencies": ["step_a"]},
                {"id": "step_c", "action": "run_tests", "dependencies": ["step_b"]},
            ]
        }
        self.orchestrator.load_graph(dag_def)
        order = self.orchestrator.topological_sort()
        self.assertEqual(order, ["step_a", "step_b", "step_c"])

    def test_02_dynamic_subgoal_expansion(self):
        """Validates runtime sub-goal expansion rewires dependencies correctly."""
        dag_def = {
            "nodes": [
                {"id": "step_1", "action": "init"},
                {"id": "step_2", "action": "complex_task", "dependencies": ["step_1"]},
                {"id": "step_3", "action": "finalize", "dependencies": ["step_2"]},
            ]
        }
        self.orchestrator.load_graph(dag_def)

        # Expand step_2 into two subgoals
        subgoals = [
            {"id": "step_2_sub_a", "action": "subtask_a"},
            {"id": "step_2_sub_b", "action": "subtask_b"}
        ]
        created = self.orchestrator.expand_subgoals("step_2", subgoals)
        self.assertEqual(created, ["step_2_sub_a", "step_2_sub_b"])

        # step_3 must now wait on step_2_sub_b instead of step_2
        self.assertIn("step_2_sub_b", self.orchestrator.nodes["step_3"].dependencies)
        self.assertNotIn("step_2", self.orchestrator.nodes["step_3"].dependencies)

        order = self.orchestrator.topological_sort()
        self.assertEqual(order, ["step_1", "step_2", "step_2_sub_a", "step_2_sub_b", "step_3"])

    def test_03_blast_radius_subgraph_generation(self):
        """Validates automatic blast-radius validation subgraph creation."""
        dag_def = {"nodes": [{"id": "code_edit", "action": "edit"}]}
        self.orchestrator.load_graph(dag_def)

        subgraph = self.orchestrator.generate_blast_radius_subgraph(
            parent_step_id="code_edit",
            affected_files=["workplace/core/foo.py", "workplace/core/bar.py"],
            affected_symbols=["FooClass", "bar_function"]
        )
        self.assertEqual(len(subgraph), 3)
        self.assertEqual(subgraph[0].action, "validate_syntax")
        self.assertEqual(subgraph[1].action, "run_focused_tests")
        self.assertEqual(subgraph[2].action, "check_contract_parity")

        # Expand into the DAG
        self.orchestrator.expand_subgoals("code_edit", subgraph)
        self.assertEqual(len(self.orchestrator.nodes), 4)

    def test_04_backtracking_and_alternate_route(self):
        """Validates branch backtracking on step failure and routing to fallback branch."""
        dag_def = {
            "nodes": [
                {"id": "plan_step", "action": "plan"},
                {"id": "try_fast_path", "action": "fast_path", "dependencies": ["plan_step"]},
                {"id": "downstream", "action": "deploy", "dependencies": ["try_fast_path"]}
            ]
        }
        self.orchestrator.load_graph(dag_def)

        # Fail try_fast_path and backtrack to alternate robust_path
        alt_route = self.orchestrator.backtrack_and_route(
            failed_step_id="try_fast_path",
            alternate_branches=[{"id": "robust_path", "action": "robust_path"}]
        )
        self.assertEqual(alt_route, "robust_path")
        self.assertEqual(self.orchestrator.nodes["try_fast_path"].status, "BACKTRACKED")
        self.assertEqual(self.orchestrator.nodes["downstream"].status, "SKIPPED")
        self.assertIn("robust_path", self.orchestrator.nodes)

    def test_05_depth_and_node_count_ceilings(self):
        """Enforces recursion depth ceiling (D <= 3) and max node count (N <= 10)."""
        orch = DynamicDAGOrchestrator(max_depth=2, max_steps=5, trace_log_path=self.trace_path)
        orch.load_graph({"nodes": [{"id": "n0", "action": "init"}]})

        # Depth 1
        orch.expand_subgoals("n0", [{"id": "n1", "action": "a"}])
        # Depth 2
        orch.expand_subgoals("n1", [{"id": "n2", "action": "b"}])

        # Attempt Depth 3 when max is 2 -> Should raise
        with self.assertRaises(DAGConstraintViolationError):
            orch.expand_subgoals("n2", [{"id": "n3", "action": "c"}])

        # Attempt adding too many nodes -> Should raise
        with self.assertRaises(DAGConstraintViolationError):
            orch.add_node(StepNode(id="n4", action="x"))
            orch.add_node(StepNode(id="n5", action="y"))
            orch.add_node(StepNode(id="n6", action="z"))

    def test_06_cycle_detection(self):
        """Validates Kahn algorithm cycle detection and rejection."""
        dag_def = {
            "nodes": [
                {"id": "a", "action": "act", "dependencies": ["c"]},
                {"id": "b", "action": "act", "dependencies": ["a"]},
                {"id": "c", "action": "act", "dependencies": ["b"]},
            ]
        }
        with self.assertRaises(CycleDetectedError):
            self.orchestrator.load_graph(dag_def)

    def test_07_end_to_end_runtime_execution_and_traces(self):
        """Validates execution loop with runtime subgoal expansion and trace logging."""
        dag_def = {
            "nodes": [
                {"id": "start", "action": "init"},
                {"id": "dynamic_step", "action": "expandable"},
                {"id": "end", "action": "finish", "dependencies": ["dynamic_step"]}
            ]
        }
        self.orchestrator.load_graph(dag_def)

        def expand_executor(node, orch):
            # Synthesize sub-goals at runtime
            orch.expand_subgoals(node.id, [
                {"id": "dynamic_sub1", "action": "sub1"},
                {"id": "dynamic_sub2", "action": "sub2"}
            ])
            return {"status": "SUCCESS"}

        executors = {
            "expandable": expand_executor,
            "init": lambda n, o: {"status": "SUCCESS"},
            "sub1": lambda n, o: {"status": "SUCCESS"},
            "sub2": lambda n, o: {"status": "SUCCESS"},
            "finish": lambda n, o: {"status": "SUCCESS"}
        }

        res = self.orchestrator.execute(executors)
        self.assertEqual(res["status"], "COMPLETED")
        self.assertIn("dynamic_sub1", res["executed_steps"])
        self.assertIn("dynamic_sub2", res["executed_steps"])
        self.assertTrue(self.trace_path.exists())
        self.assertGreater(len(self.orchestrator.execution_log), 0)


if __name__ == "__main__":
    unittest.main()
