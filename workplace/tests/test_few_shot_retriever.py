#!/usr/bin/env python3
"""
Unit tests for FewShotRetriever (TODO-AGT-16).
Verifies multi-factor similarity scoring, top-k retrieval ranking,
attention token budgeting, counter-factual injection, and zero-shot fallback.
"""

from pathlib import Path
import pytest

from workplace.core.few_shot_retriever import FewShotRetriever, Exemplar


@pytest.fixture
def retriever():
    """Initializes FewShotRetriever using repository exemplar library."""
    return FewShotRetriever()


def test_load_default_library(retriever):
    """Verifies that the exemplar library is successfully loaded."""
    assert len(retriever.exemplars) >= 5
    ids = [ex.exemplar_id for ex in retriever.exemplars]
    assert "ex_fastapi_endpoint_01" in ids
    assert "ex_ast_visitor_01" in ids
    assert "ex_negative_dangerous_eval_01" in ids


def test_similarity_scoring_formula(retriever):
    """Verifies mathematical correctness of multi-factor scoring formula."""
    ex = Exemplar(
        exemplar_id="test_ex",
        title="Test FastApi",
        language="python",
        ast_pattern="fastapi_endpoint",
        domain_tags=["api", "rest", "auth"],
        code_snippet="def foo(): pass",
        explanation="test"
    )

    # Perfect match: lang=1.0, pattern=1.0, tags=1.0 -> 0.40 + 0.35 + 0.25 = 1.00
    score_perfect = retriever.compute_similarity_score(
        ex, query_lang="python", query_pattern="fastapi_endpoint", domain_tags=["api", "rest", "auth"]
    )
    assert score_perfect == 1.0

    # Partial tags: 2 out of 4 union -> 2/4 = 0.50 -> 0.40 + 0.35 + 0.25*0.50 = 0.875
    score_partial = retriever.compute_similarity_score(
        ex, query_lang="python", query_pattern="fastapi_endpoint", domain_tags=["api", "other"]
    )
    assert 0.70 < score_partial < 1.0

    # Mismatched language: lang=0.0 -> max score <= 0.60
    score_diff_lang = retriever.compute_similarity_score(
        ex, query_lang="rust", query_pattern="fastapi_endpoint", domain_tags=["api"]
    )
    assert score_diff_lang <= 0.60


def test_retrieve_ranked_exemplars(retriever):
    """Verifies that retrieval ranks the most relevant exemplars first."""
    results = retriever.retrieve(
        query_lang="python",
        query_pattern="fastapi_endpoint",
        domain_tags=["api", "auth", "rest"],
        top_k=2
    )

    assert len(results) >= 1
    top = results[0]
    assert top.exemplar_id == "ex_fastapi_endpoint_01"
    assert top.score >= 0.80


def test_token_budget_enforcement(retriever):
    """Verifies that retrieved exemplars stay strictly within the token budget."""
    # Small budget allowed: only 1 small or none
    results = retriever.retrieve(
        query_lang="python",
        query_pattern="ast_visitor",
        domain_tags=["ast", "parser"],
        max_token_budget=50,
        top_k=5
    )
    # Total tokens of selected exemplars must be <= 50
    total_tokens = sum(retriever.estimate_tokens(x.code_snippet + x.explanation) for x in results)
    assert total_tokens <= 50


def test_zero_shot_fallback(retriever):
    """Verifies graceful fallback to zero-shot when no relevant exemplars match."""
    results = retriever.retrieve(
        query_lang="fortran",
        query_pattern="unheard_matrix_routine",
        domain_tags=["obsolete"],
        min_score_threshold=0.50
    )
    assert len(results) == 0
    prompt_text = retriever.format_prompt_injection(results)
    assert prompt_text == ""


def test_format_prompt_injection(retriever):
    """Verifies formatted Markdown output containing golden pattern and guidance."""
    results = retriever.retrieve(
        query_lang="python",
        query_pattern="merkle_hook",
        domain_tags=["ledger", "security"],
        top_k=1,
        include_negative=True
    )
    assert len(results) >= 1
    markdown = retriever.format_prompt_injection(results)
    assert "### Reference Implementation Exemplars" in markdown
    assert "SHA-256 Merkle Ledger" in markdown
    assert "```python" in markdown
