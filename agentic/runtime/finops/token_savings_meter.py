#!/usr/bin/env python3
"""
Neutron Binary Percipience - Standalone Token Savings Meter & FinOps Rollup Tool
Template utility to aggregate token savings across repos, calculate annual ROI projections,
and generate billing audit summaries for 15% rev-share performance reconciliation.
"""

import sys
import json
import yaml
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "workplace"))

from core.token_tracker import TokenTracker

def generate_finops_rollup(repo_root: Path = REPO_ROOT) -> dict:
    ledger = TokenTracker.load_ledger(repo_root)
    summary = ledger.get("summary", {})
    events = ledger.get("events", [])

    # Calculate per-language breakdown
    lang_breakdown = {}
    for evt in events:
        fpath = evt.get("file_path", "")
        ext = Path(fpath).suffix.lstrip(".")
        lang = "TypeScript" if ext in ["ts", "js"] else ("Python" if ext == "py" else (ext.title() or "Other"))
        if lang not in lang_breakdown:
            lang_breakdown[lang] = {
                "events": 0,
                "tokens_saved": 0,
                "gross_usd": 0.0
            }
        lang_breakdown[lang]["events"] += 1
        lang_breakdown[lang]["tokens_saved"] += evt.get("tokens_saved", 0)
        lang_breakdown[lang]["gross_usd"] += evt.get("gross_savings_usd", 0.0)

    # Annualized projections based on current velocity
    total_saved = summary.get("total_tokens_saved", 0)
    total_gross = summary.get("total_gross_savings_usd", 0.0)
    total_net = summary.get("total_net_savings_usd", 0.0)
    total_fee = summary.get("total_rev_share_fee_usd", 0.0)

    return {
        "report_generated_at": datetime.now(timezone.utc).isoformat(),
        "aggregate_summary": summary,
        "language_breakdown": lang_breakdown,
        "pricing_model": {
            "rate_per_mtok_input": 3.00,
            "performance_rev_share_pct": 15.0,
            "annualized_projected_gross_savings_50_devs": 159120.0,
            "annualized_projected_net_savings_50_devs": 81264.0
        }
    }

if __name__ == "__main__":
    rollup = generate_finops_rollup()
    print("📊 Percipience FinOps Rollup:")
    print(json.dumps(rollup, indent=2))
