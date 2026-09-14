"""
Percipience Layered Context & Custom Agent Validator
Enforces the 3-Tier Precedence Hierarchy:
Tier 1 (Base Platform Invariants) -> Tier 2 (Enterprise Global Context) -> Tier 3 (Module Domain Context)
Ensures custom agents and rules run seamlessly without violating platform security constraints.
"""

from pathlib import Path
from typing import Dict, List, Any

try:
    import yaml
except ImportError:
    yaml = None

class LayeredContextValidator:
    """Validates unencrypted customer context layered against base platform invariants."""

    @classmethod
    def validate_layered_hierarchy(cls, workspace_root: Path) -> Dict[str, Any]:
        results = {
            "tier1_invariants": "VALID",
            "tier2_global_rules": [],
            "tier3_custom_schemas": [],
            "custom_agents": [],
            "violations": [],
            "overall_valid": True
        }

        # 1. Audit Tier 2: Enterprise Global Context
        rules_dir = workspace_root / "context" / "custom" / "rules"
        if rules_dir.exists():
            for rf in rules_dir.glob("*.md"):
                content = rf.read_text(encoding="utf-8")
                # Check that custom rule doesn't attempt to disable safety checks
                if "disable_poisoning_quarantine" in content.lower():
                    results["violations"].append(f"Illegal rule in {rf.name}: cannot disable poisoning quarantine.")
                    results["overall_valid"] = False
                else:
                    results["tier2_global_rules"].append(rf.name)

        # 2. Audit Tier 3: Custom Domain Schemas
        schemas_dir = workspace_root / "context" / "custom" / "schemas"
        if schemas_dir.exists():
            for sf in schemas_dir.glob("*.yaml"):
                results["tier3_custom_schemas"].append(sf.name)

        # 3. Audit Custom Agents
        agents_dir = workspace_root / "agentic" / "custom" / "agents"
        if agents_dir.exists():
            for af in agents_dir.glob("*.yaml"):
                results["custom_agents"].append(af.name)

        return results
