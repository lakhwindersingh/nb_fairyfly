#!/usr/bin/env python3
"""
Neutron Binary Percipience - Agent Registry Synchronizer

Reconciles the `agent_registry` manifest embedded in the Claude settings files
with the canonical set of custom agent manifests declared under
`.nb/agentic/custom/agents/`.

Canonical Source of Truth:
    .nb/agentic/custom/agents/*.yaml   (each declares an `agent_id`)

Synchronization Targets:
    settings.json
    .claude/settings.json

The synchronizer is intentionally deterministic and idempotent so it can be wired
as a mandatory preflight step of the CI/CD gatekeeper workflow. It never mutates
agent manifests; it only projects the canonical agent-id set into the settings
registries.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml

    try:
        from yaml import CSafeLoader as SafeLoader
    except ImportError:
        from yaml import SafeLoader
except ImportError:
    yaml = None
    SafeLoader = None


class AgentRegistrySynchronizer:
    """Projects canonical custom-agent manifests into settings.json registries."""

    AGENTS_DIR = ".nb/agentic/custom/agents"
    SETTINGS_FILES = ("settings.json", ".claude/settings.json")
    REGISTRY_KEY = "agent_registry"

    def __init__(self, workspace_root: Optional[Path] = None):
        if workspace_root:
            self.workspace_root = Path(workspace_root).resolve()
        else:
            cur = Path(__file__).resolve()
            if len(cur.parents) >= 3 and cur.parents[1].name in (".nb", "workplace"):
                self.workspace_root = cur.parents[2]
            else:
                self.workspace_root = cur.parents[1]

    # ------------------------------------------------------------------
    # Canonical source
    # ------------------------------------------------------------------
    @property
    def agents_dir(self) -> Path:
        return self.workspace_root / self.AGENTS_DIR

    def scan_agent_ids(self) -> List[str]:
        """
        Returns the sorted, de-duplicated set of agent_ids declared by every
        YAML manifest under the canonical custom agents directory.
        """
        agent_ids: List[str] = []
        if not self.agents_dir.exists():
            return agent_ids

        for manifest in sorted(self.agents_dir.glob("*.yaml")) + sorted(self.agents_dir.glob("*.yml")):
            agent_id = self._read_agent_id(manifest)
            if agent_id:
                agent_ids.append(agent_id)

        return sorted(set(agent_ids))

    def _read_agent_id(self, manifest: Path) -> Optional[str]:
        stem = manifest.stem
        fallback = stem if stem.startswith("agent_") else f"agent_{stem}"
        if yaml is None:
            return fallback
        try:
            with open(manifest, "r", encoding="utf-8") as f:
                if SafeLoader is not None:
                    data = yaml.load(f, Loader=SafeLoader) or {}
                else:
                    data = yaml.safe_load(f) or {}
        except Exception:
            return fallback

        if not isinstance(data, dict):
            return fallback
        meta = data.get("metadata", {}) if isinstance(data.get("metadata"), dict) else {}
        return meta.get("agent_id") or data.get("agent_id") or fallback

    # ------------------------------------------------------------------
    # Targets
    # ------------------------------------------------------------------
    def settings_paths(self) -> List[Path]:
        return [self.workspace_root / rel for rel in self.SETTINGS_FILES]

    def _read_settings(self, path: Path) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_settings(self, path: Path, data: Dict[str, Any]) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")

    def _current_registry(self, data: Dict[str, Any]) -> List[str]:
        reg = data.get(self.REGISTRY_KEY)
        return list(reg) if isinstance(reg, list) else []

    # ------------------------------------------------------------------
    # Drift detection & reconciliation
    # ------------------------------------------------------------------
    def check(self) -> Dict[str, Any]:
        """
        Non-mutating drift report comparing the canonical agent set against each
        settings registry. Returns per-file missing/extra entries and a summary.
        """
        canonical = self.scan_agent_ids()
        report: Dict[str, Any] = {
            "canonical_count": len(canonical),
            "canonical": canonical,
            "files": {},
            "drift": False,
        }

        for path in self.settings_paths():
            if not path.exists():
                continue
            data = self._read_settings(path)
            current = self._current_registry(data)
            missing = sorted(set(canonical) - set(current))
            extra = sorted(set(current) - set(canonical))
            in_sync = not missing and not extra and current == canonical
            report["files"][str(path.relative_to(self.workspace_root))] = {
                "in_sync": in_sync,
                "registry_count": len(current),
                "missing": missing,
                "extra": extra,
            }
            if not in_sync:
                report["drift"] = True

        return report

    def sync(self) -> Dict[str, Any]:
        """
        Writes the canonical agent set into every settings registry. Idempotent:
        unchanged files are left byte-identical.
        """
        canonical = self.scan_agent_ids()
        result: Dict[str, Any] = {
            "status": "IN_SYNC",
            "canonical_count": len(canonical),
            "updated": [],
            "unchanged": [],
        }

        for path in self.settings_paths():
            if not path.exists():
                continue
            data = self._read_settings(path)
            current = self._current_registry(data)
            rel = str(path.relative_to(self.workspace_root))

            if current == canonical:
                result["unchanged"].append(rel)
                continue

            data[self.REGISTRY_KEY] = canonical
            self._write_settings(path, data)
            result["updated"].append(rel)

        if result["updated"]:
            result["status"] = "SYNCHRONIZED"
        return result

    def run(self, apply: bool = True) -> Dict[str, Any]:
        """Entrypoint used by the workflow executor."""
        return self.sync() if apply else self.check()

    @classmethod
    def cli(cls, argv: Optional[List[str]] = None) -> int:
        argv = list(sys.argv[1:] if argv is None else argv)
        apply = "--check" not in argv
        result = cls().run(apply=apply)
        print(json.dumps(result, indent=2))
        return 0 if not (apply is False and result.get("drift")) else 1


if __name__ == "__main__":
    raise SystemExit(AgentRegistrySynchronizer.cli())
