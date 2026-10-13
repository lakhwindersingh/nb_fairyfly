#!/usr/bin/env python3
"""
Neutron Binary Percipience - Registry & Context Synchronizer

Reconciles the curated registry sections embedded in the Claude settings files
with the canonical filesystem sources of truth:

    agent_registry     <- .nb/agentic/custom/agents/*.yaml      (list, agent_id)
    context_rules      <- .nb/context/rules/**                  (map, key -> path)
    context_contracts  <- .nb/context/contracts/**              (map, key -> path)

Synchronization Targets:
    settings.json
    .claude/settings.json

Semantics
---------
* agent_registry is projected as a sorted, de-duplicated list of declared agent_ids.
* context_rules / context_contracts are reconciled as maps. Existing symbolic keys
  are preserved when they already point at a discovered file (so friendly aliases
  survive). Newly discovered files receive a deterministic key derived from their
  filename. Entries that point outside the managed directory (e.g. the ledger) are
  retained untouched.

The synchronizer is deterministic and idempotent so it can be wired as a mandatory
preflight step of the CI/CD gatekeeper workflow. It never mutates the underlying
rule, contract, or agent artifacts.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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
    """Projects canonical agents, rules, and contracts into settings.json registries."""

    AGENTS_DIR = ".nb/agentic/custom/agents"
    RULES_DIR = ".nb/context/rules"
    CONTRACTS_DIR = ".nb/context/contracts"
    SETTINGS_FILES = ("settings.json", ".claude/settings.json")

    # (settings_key, kind, source_spec)
    SPECS: Tuple[Tuple[str, str, str], ...] = (
        ("agent_registry", "list", AGENTS_DIR),
        ("context_rules", "map", RULES_DIR),
        ("context_contracts", "map", CONTRACTS_DIR),
    )

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
    # Canonical sources
    # ------------------------------------------------------------------
    def scan_agent_ids(self) -> List[str]:
        """
        Returns the sorted, de-duplicated set of agent_ids declared by every
        YAML manifest under the canonical custom agents directory.
        """
        agent_ids: List[str] = []
        agents_dir = self.workspace_root / self.AGENTS_DIR
        if not agents_dir.exists():
            return agent_ids

        for manifest in sorted(agents_dir.glob("*.yaml")) + sorted(agents_dir.glob("*.yml")):
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

    def scan_files(self, rel_dir: str) -> List[str]:
        """Returns sorted, repo-relative POSIX paths for every file under rel_dir."""
        base = self.workspace_root / rel_dir
        if not base.exists():
            return []
        files = [
            p.relative_to(self.workspace_root).as_posix()
            for p in base.rglob("*")
            if p.is_file() and not p.name.startswith(".")
        ]
        return sorted(files)

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

    # ------------------------------------------------------------------
    # Reconciliation primitives
    # ------------------------------------------------------------------
    @staticmethod
    def _derive_key(rel_path: str, used: set) -> str:
        stem = Path(rel_path).stem
        key = re.sub(r"[^a-z0-9]+", "_", stem.lower()).strip("_") or "item"
        if key not in used:
            return key
        ext = Path(rel_path).suffix.lstrip(".")
        base = f"{key}_{ext}" if ext else key
        candidate, i = base, 2
        while candidate in used:
            candidate = f"{base}_{i}"
            i += 1
        return candidate

    def _build_map(self, current: Any, rel_dir: str) -> Dict[str, str]:
        """Projects discovered files into a symbolic-key -> path map."""
        current = current if isinstance(current, dict) else {}
        prefix = rel_dir.rstrip("/") + "/"

        existing_key_by_path: Dict[str, str] = {}
        retained: Dict[str, str] = {}
        for key, value in current.items():
            if isinstance(value, str) and value.startswith(prefix):
                existing_key_by_path[value] = key
            else:
                retained[key] = value

        result: Dict[str, str] = dict(retained)
        used = set(result.keys())
        for rel in self.scan_files(rel_dir):
            key = existing_key_by_path.get(rel)
            if not key or key in used:
                key = self._derive_key(rel, used)
            result[key] = rel
            used.add(key)
        return result

    def _project(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Returns the fully synchronized settings document (non-mutating)."""
        projected = json.loads(json.dumps(data))  # deep copy, preserves order
        for settings_key, kind, source in self.SPECS:
            if kind == "list":
                projected[settings_key] = self.scan_agent_ids()
            else:
                projected[settings_key] = self._build_map(data.get(settings_key), source)
        return projected

    def _section_drift(self, current: Any, desired: Any, source: str, kind: str) -> Dict[str, Any]:
        if kind == "list":
            current_list = [x for x in current if isinstance(x, str)] if isinstance(current, list) else []
            desired_list = list(desired)
            return {
                "in_sync": current_list == desired_list,
                "count": len(desired_list),
                "missing": sorted(set(desired_list) - set(current_list)),
                "extra": sorted(set(current_list) - set(desired_list)),
            }

        current_map = current if isinstance(current, dict) else {}
        desired_map = desired if isinstance(desired, dict) else {}
        managed_current = {k: v for k, v in current_map.items() if isinstance(v, str) and v.startswith(source.rstrip("/") + "/")}
        return {
            "in_sync": current_map == desired_map,
            "count": len(desired_map),
            "missing": sorted(set(desired_map.values()) - set(managed_current.values())),
            "extra": sorted(set(managed_current.values()) - set(desired_map.values())),
        }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def check(self) -> Dict[str, Any]:
        """Non-mutating drift report for every managed section of every settings file."""
        report: Dict[str, Any] = {"files": {}, "drift": False}
        for path in self.settings_paths():
            if not path.exists():
                continue
            data = self._read_settings(path)
            desired = self._project(data)
            sections: Dict[str, Any] = {}
            for settings_key, kind, source in self.SPECS:
                drift = self._section_drift(data.get(settings_key), desired[settings_key], source, kind)
                sections[settings_key] = drift
                if not drift["in_sync"]:
                    report["drift"] = True
            report["files"][str(path.relative_to(self.workspace_root))] = sections
        return report

    def sync(self) -> Dict[str, Any]:
        """
        Writes the fully synchronized registry sections into every settings file.
        Idempotent: files already in sync are left byte-identical.
        """
        result: Dict[str, Any] = {"status": "IN_SYNC", "updated": [], "unchanged": [], "sections": {}}
        for path in self.settings_paths():
            if not path.exists():
                continue
            data = self._read_settings(path)
            desired = self._project(data)
            rel = str(path.relative_to(self.workspace_root))

            changed_sections = [k for k, kind, src in self.SPECS if data.get(k) != desired[k]]
            if not changed_sections:
                result["unchanged"].append(rel)
                continue

            self._write_settings(path, desired)
            result["updated"].append(rel)
            result["sections"][rel] = changed_sections

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
