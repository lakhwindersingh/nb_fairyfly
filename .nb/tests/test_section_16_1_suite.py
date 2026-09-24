"""
Unit and Integration Test Suite for Percipience Section 16.1 Modules:
- TODO-COMP-01: OpenTelemetry GenAI Exporter (OpenTelemetryGenAIExporter)
- TODO-COMP-02: Quantitative LLM Evals & Hallucination Scoring (EvalScoringEngine)
- TODO-COMP-03: Side-by-Side Prompt Benchmark Engine (PromptBenchmarkEngine)
- TODO-COMP-04: Semantic Prompt & LLM Response Cache (SemanticPromptCache)
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(REPO_ROOT / "workplace") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "workplace"))

import pytest
import time

from core.otel_exporter import OpenTelemetryGenAIExporter
from core.eval_scoring_engine import EvalScoringEngine
from core.prompt_benchmark_engine import PromptBenchmarkEngine
from core.semantic_prompt_cache import SemanticPromptCache


class TestOpenTelemetryGenAIExporter:
    """Verifies W3C traceparent generation, GenAI span lifecycle, and token tracking."""

    def test_w3c_traceparent_format(self):
        tp = OpenTelemetryGenAIExporter.generate_w3c_traceparent()
        parsed = OpenTelemetryGenAIExporter.parse_w3c_traceparent(tp)
        assert parsed["version"] == "00"
        assert len(parsed["trace_id"]) == 32
        assert len(parsed["parent_span_id"]) == 16
        assert parsed["is_sampled"] is True

    def test_span_lifecycle_and_ttft(self):
        exporter = OpenTelemetryGenAIExporter()
        span = exporter.start_genai_span(
            name="generate_module_catalog",
            model_name="claude-3-7-sonnet",
            system_vendor="anthropic",
            temperature=0.2
        )
        span_id = span["context"]["span_id"]
        assert span_id in exporter.active_spans

        exporter.record_ttft(span_id, 0.45)
        assert len(exporter.active_spans[span_id]["events"]) == 1

        completed = exporter.end_genai_span(
            span_id=span_id,
            input_tokens=1500,
            output_tokens=350,
            finish_reason="stop"
        )
        assert completed["attributes"]["gen_ai.usage.total_tokens"] == 1850
        assert completed["duration_ms"] >= 0.0
        assert completed["status"]["code"] == "STATUS_CODE_OK"


class TestEvalScoringEngine:
    """Verifies syntax checks, hallucination indicators, and multi-dimensional G-Eval scores."""

    def test_syntax_validity(self):
        valid_code = "def add(a: int, b: int) -> int:\n    return a + b\n"
        res = EvalScoringEngine.evaluate_code_correctness(valid_code)
        assert res["is_valid_syntax"] is True
        assert res["score"] == 1.0

        invalid_code = "def broken(a, b\n    return a +"
        res_inv = EvalScoringEngine.evaluate_code_correctness(invalid_code)
        assert res_inv["is_valid_syntax"] is False
        assert res_inv["score"] == 0.0

    def test_hallucination_indicators(self):
        clean_code = "import json\nfrom pathlib import Path\ndef parse(p): return json.loads(Path(p).read_text())"
        res_clean = EvalScoringEngine.evaluate_hallucination_indicators(clean_code)
        assert res_clean["is_hallucination_free"] is True
        assert res_clean["hallucination_freedom_score"] >= 0.9

        hallucinated_code = "import fake_magic_library\ndef compute(): TODO: implement_this_real_api()"
        res_hall = EvalScoringEngine.evaluate_hallucination_indicators(hallucinated_code)
        assert res_hall["is_hallucination_free"] is False
        assert len(res_hall["detected_hallucinations"]) >= 2

    def test_full_generation_evaluation(self):
        spec = "Create an authentication token generator in python"
        context = "Use standard hashlib and secrets module for crypto tokens"
        code = "import hashlib\nimport secrets\ndef generate_token() -> str:\n    return secrets.token_hex(32)\n"

        eval_res = EvalScoringEngine.evaluate_generation(
            generated_code=code,
            requirement_spec=spec,
            context_provided=context,
            valid_symbols=["generate_token", "secrets", "hashlib"]
        )
        assert eval_res["evaluation_status"] == "PASSED"
        assert eval_res["composite_geval_score"] >= 0.75
        assert eval_res["rubrics"]["code_correctness"] == 1.0


class TestPromptBenchmarkEngine:
    """Verifies prompt variation matrix benchmarking and cost calculations."""

    def test_cost_calculation(self):
        cost_a = PromptBenchmarkEngine.calculate_cost("tier_a_frontier", 100000, 20000)
        assert cost_a > 0.0
        cost_b = PromptBenchmarkEngine.calculate_cost("tier_b_compact", 100000, 20000)
        assert cost_b < cost_a

    def test_run_benchmark_matrix_and_report(self, tmp_path):
        variants = {
            "prompt_v1_concise": "You are a concise engineer. Output minimal code.",
            "prompt_v2_detailed": "You are a meticulous architect. Provide types, docstrings, and invariants."
        }
        test_cases = [
            {"id": "test_1", "expected_keywords": ["def", "return"]},
            {"id": "test_2", "expected_keywords": ["class", "init"]}
        ]

        results = PromptBenchmarkEngine.run_benchmark_matrix(variants, test_cases)
        assert results["total_variants_evaluated"] == 2
        assert "prompt_v1_concise" in results["matrix_results"]

        report_file = PromptBenchmarkEngine.generate_markdown_report(results, out_path=tmp_path / "bench.md")
        assert report_file.exists()
        content = report_file.read_text(encoding="utf-8")
        assert "prompt_v1_concise" in content
        assert "Tier A Cost" in content


class TestSemanticPromptCache:
    """Verifies semantic similarity retrieval, cache hits, misses, and FinOps savings."""

    def test_exact_and_semantic_cache_hit(self):
        cache = SemanticPromptCache(default_threshold=0.80)
        p1 = "How do I configure Redis Redlock worktree leases for concurrent agents?"
        r1 = "Set redis_url and lease_ttl_seconds in worktree_manager.py"

        cache.set(p1, r1, tokens_saved=450)

        # Semantically near prompt
        p2 = "How can I configure Redis Redlock leases for concurrent worktrees?"
        match = cache.get(p2)
        assert match is not None
        assert match["cache_hit"] is True
        assert match["similarity_score"] >= 0.80
        assert match["cached_response"] == r1
        assert match["tokens_saved"] == 450

    def test_semantic_cache_miss(self):
        cache = SemanticPromptCache(default_threshold=0.80)
        cache.set("Analyze AST pruning algorithms", "AST bodies are replaced with placeholders", tokens_saved=200)

        miss_match = cache.get("What is the weather today in San Francisco?")
        assert miss_match is None

    def test_metrics_telemetry(self):
        cache = SemanticPromptCache()
        cache.set("hello world", "greeting", tokens_saved=100)
        cache.get("hello world") # Hit
        cache.get("completely unrelated query about physics") # Miss

        metrics = cache.get_metrics()
        assert metrics["total_requests"] == 2
        assert metrics["hits"] == 1
        assert metrics["misses"] == 1
        assert metrics["hit_rate_pct"] == 50.0
        assert metrics["tokens_saved_total"] == 100
