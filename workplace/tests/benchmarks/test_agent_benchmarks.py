#!/usr/bin/env python3
"""
Continuous Quality Evaluation Benchmark Test Suite (TODO-AGT-20).
Exercises agents across 5 core disciplines and validates the 5-Metric Scoring Radar.
"""

from pathlib import Path
import tempfile
import pytest

from workplace.core.agent_benchmark_harness import (
    AgentBenchmarkHarness,
    BenchmarkChallenge,
    RadarScorecard
)


@pytest.fixture
def harness():
    """Initializes AgentBenchmarkHarness."""
    return AgentBenchmarkHarness()


def test_standard_challenges_structure(harness):
    """Verifies that all 5 core disciplines are present in the challenge suite."""
    challenges = harness.get_standard_challenges()
    assert len(challenges) == 5
    disciplines = {c.discipline for c in challenges}
    expected = {"AST_PRUNING", "WIRE_CONTRACT", "LIVING_DOCS", "CVE_REMEDIATION", "FLAKY_ISOLATION"}
    assert disciplines == expected


def test_run_single_challenge(harness):
    """Verifies execution of a single challenge with metric tracking."""
    chal = harness.get_standard_challenges()[0]
    result = harness.execute_challenge(chal)

    assert result.passed is True
    assert result.discipline == "AST_PRUNING"
    assert result.latency_s > 0.0
    assert result.tokens_consumed > 0
    assert result.semantic_parity >= 0.95
    assert result.invariant_violations == 0


def test_run_benchmark_suite_radar_metrics(harness):
    """Verifies aggregate 5-Metric Radar calculation."""
    scorecard = harness.run_benchmark_suite()

    assert scorecard.challenges_count == 5
    assert scorecard.passed_count == 5
    assert scorecard.tsr_pct >= 90.0
    assert scorecard.avg_semantic_parity >= 0.95
    assert scorecard.avg_tokens_consumed < 5000
    assert scorecard.avg_latency_s < 10.0
    assert scorecard.invariant_compliance_pct == 100.0
    assert scorecard.overall_grade in ["A+", "A"]
    assert scorecard.merkle_receipt_id.startswith("RP_BENCHMARK_")


def test_scorecard_markdown_generation_and_saving(harness):
    """Verifies that Markdown scorecard generation formats tables and saves to disk."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_report = Path(tmp_dir) / "test_scorecard.md"
        card = harness.run_benchmark_suite()
        saved_path = harness.save_report(card, output_file=tmp_report)

        assert saved_path.exists()
        content = saved_path.read_text(encoding="utf-8")
        assert "# 🎯 Multi-Agent Quality & Continuous Evaluation Scorecard" in content
        assert "Task Success Rate (TSR)" in content
        assert "Semantic Parity" in content
        assert "Granular Challenge Breakdown" in content


def test_underperforming_agent_regression_detection(harness):
    """Verifies that an underperforming challenge is flagged and degrades the grade."""
    failing_challenge = BenchmarkChallenge(
        challenge_id="CHAL_FAIL_99",
        name="Broken Agent",
        discipline="UNKNOWN_DISCIPLINE",
        target_agent="agent_broken",
        description="Failing challenge test"
    )

    card = harness.run_benchmark_suite(challenges=[failing_challenge])
    assert card.passed_count == 0
    assert card.tsr_pct == 0.0
    assert card.overall_grade == "FAIL"
