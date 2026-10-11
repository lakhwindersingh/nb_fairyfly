#!/usr/bin/env python3
"""
Automated Capability Matrix Generator.
Extracts capabilities, maturity levels, and dependencies from all 13 active plan manifests
and compiles .nb/plan/CAPABILITY_MATRIX.md.
"""

from pathlib import Path
from typing import Dict, List, Any
import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
PLAN_ROOT = REPO_ROOT / ".nb/plan"
OUTPUT_FILE = PLAN_ROOT / "CAPABILITY_MATRIX.md"


def generate_capability_matrix():
    manifests: Dict[str, Dict[str, Any]] = {}
    for p in sorted(PLAN_ROOT.glob("**/MANIFEST.yaml")):
        if "templates" in p.parts or "archive" in p.parts:
            continue
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            pid = data.get("plan_id")
            if pid:
                manifests[pid] = {
                    "data": data,
                    "rel_dir": p.parent.relative_to(PLAN_ROOT)
                }
        except Exception as e:
            print(f"Error reading {p}: {e}")

    md_lines = [
        "# 📊 Percipience Master Capability Cross-Reference Matrix",
        "",
        "> **Generated Automatically**: Certified via `.nb/plan/scripts/generate_capability_index.py`  ",
        f"> **Total Plans Tracked**: {len(manifests)}  ",
        "",
        "---",
        "",
        "## 1. Master Plan Capabilities & Governance Matrix",
        "",
        "| Plan ID | Layer | Stage | Parity ($S_{SP}$) | Production Ready | Capabilities Count |",
        "| :--- | :---: | :---: | :---: | :---: | :---: |",
    ]

    for pid, item in sorted(manifests.items(), key=lambda x: (x[1]["data"].get("layer", ""), pid)):
        d = item["data"]
        layer = d.get("layer", "master")
        mat = d.get("maturity", {})
        stage = mat.get("stage", "N/A")
        parity = d.get("semantic_parity", {}).get("composite_score", "N/A")
        prod = "✅ Ready" if mat.get("production_ready") else "⚠️ Pending"
        caps = d.get("key_capabilities") or d.get("capabilities") or []
        caps_cnt = len(caps) if isinstance(caps, list) else len(caps.keys()) if isinstance(caps, dict) else 0

        md_lines.append(f"| [`{pid}`](./{item['rel_dir']}) | `{layer}` | `{stage}` | `{parity}` | {prod} | {caps_cnt} |")

    md_lines.extend([
        "",
        "---",
        "",
        "## 2. Detailed Capability Inventory by Plan",
        ""
    ])

    for pid, item in sorted(manifests.items(), key=lambda x: (x[1]["data"].get("layer", ""), pid)):
        d = item["data"]
        name = d.get("plan_name", pid)
        layer = d.get("layer", "master")
        caps = d.get("key_capabilities") or d.get("capabilities") or []
        deps = d.get("dependencies", {})
        reqs = deps.get("requires", []) if isinstance(deps, dict) else deps

        md_lines.extend([
            f"### `{pid}`: {name}",
            f"- **Location**: [{item['rel_dir']}](./{item['rel_dir']})",
            f"- **Layer**: `{layer}`",
            f"- **Requires**: {', '.join(f'`{r}`' for r in reqs) if reqs else '*None (Root)*'}",
            "- **Key Capabilities**:"
        ])

        if isinstance(caps, list):
            for cap in caps:
                md_lines.append(f"  - {cap}")
        elif isinstance(caps, dict):
            for k, v in caps.items():
                md_lines.append(f"  - **{k}**: {v}")
        else:
            md_lines.append("  - *No explicit capabilities declared*")

        md_lines.append("")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines) + "\n")

    print(f"✅ Generated Capability Matrix at: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_capability_matrix()
