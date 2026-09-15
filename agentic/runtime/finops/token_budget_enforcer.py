#!/usr/bin/env python3
"""
Neutron Binary Percipience - Token Budget Enforcer & Anti-Bloat Pre-Flight Gate
Template utility enforcing that no agent turn or context compilation transmits > 15,000
unpruned raw tokens without triggering an AST skeletonization pass.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "workplace"))

from core.ast_optimizer import ASTOptimizer

MAX_UNPRUNED_TOKEN_LIMIT = 15000

def enforce_turn_budget(file_path: Path, max_limit: int = MAX_UNPRUNED_TOKEN_LIMIT) -> dict:
    if not file_path.exists():
        return {"status": "ERROR", "reason": f"File {file_path} not found"}

    content = file_path.read_text(encoding="utf-8", errors="ignore")
    ext = file_path.suffix.lstrip(".")
    lang = "typescript" if ext in ["ts", "js"] else ("python" if ext == "py" else ext)

    _, stats = ASTOptimizer.prune_source(content, lang)
    uncompressed = stats["uncompressed_tokens"]

    if uncompressed > max_limit:
        return {
            "status": "FLAGGED",
            "uncompressed_tokens": uncompressed,
            "pruned_tokens": stats["pruned_tokens"],
            "tokens_saved": stats["saved_tokens"],
            "action_required": "APPLY_AST_PRUNING",
            "message": f"Turn exceeded token budget: {uncompressed:,} > {max_limit:,} tokens! AST skeletonization required."
        }

    return {
        "status": "APPROVED",
        "uncompressed_tokens": uncompressed,
        "pruned_tokens": stats["pruned_tokens"],
        "tokens_saved": stats["saved_tokens"],
        "message": f"Turn within budget: {uncompressed:,} tokens."
    }

if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else (REPO_ROOT / "workplace" / "core" / "merkle_engine.py")
    res = enforce_turn_budget(target)
    print("🛡️ Token Budget Enforcer Gate Check:")
    print(res)
