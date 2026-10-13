#!/usr/bin/env python3
"""
Neutron Binary Percipience - Registry & Context Synchronizer

Reconciles the curated registry sections embedded in the Claude settings files
with the canonical filesystem sources of truth:

    agent_registry     <- .nb/agentic/custom/agents/*.yaml      (list, agent_id)
    context_rules      <- .nb/context/rules/**                  (map, key -> path)
    context_contracts  <- .nb/context/contracts/**              (map, key -> path)
    workflow_registry  <- .nb/agentic/workflows/**              (map, key -> path)
                          .nb/agentic/custom/workflows/**
    workflow_hooks     <- agent autonomous_cicd_hooks /         (map, key -> path)
                          workflow_bindings + workflow triggers

Synchronization Targets:
    settings.json
    .claude/settings.json

Semantics
---------
* agent_registry is projected as a sorted, de-duplicated list of declared agent_ids.
* context_rules / context_contracts / workflow_registry are reconciled as maps.
  Existing symbolic keys are preserved when they already point at a discovered
  file (so friendly aliases survive). Newly discovered files receive a
  deterministic key derived from their filename. Entries that point outside the
  managed directory (e.g. the ledger) are retained untouched.
* workflow_hooks reconciles the workflow hook bindings declared by agent
  manifests (autonomous_cicd_hooks.target_workflows, workflow_bindings) and the
  event triggers declared inside workflow files across both workflow
  directories. Each key is ``<agent_id>__<workflow_id>__<step_id>`` (or
  ``<workflow_key>__<event>`` for event triggers) and its value is the workflow
  artifact that implements the hook (falling back to the raw workflow_id when
  the target workflow is not yet materialized).

The synchronizer is deterministic and idempotent so it can be wired as a mandatory
preflight step of the CI/CD gatekeeper workflow. It never mutates the underlying
rule, contract, agent, or workflow artifacts.
"""

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

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
    """Projects canonical agents, rules, contracts & workflows into settings registries."""

    AGENTS_DIR = ".nb/agentic/custom/agents"
    RULES_DIR = ".nb/context/rules"
    CONTRACTS_DIR = ".nb/context/contracts"
    WORKFLOWS_DIR = ".nb/agentic/workflows"
    CUSTOM_WORKFLOWS_DIR = ".nb/agentic/custom/workflows"
    SETTINGS_FILES = ("settings.json", ".claude/settings.json")

    # (settings_key, kind, source_dirs)
    SPECS: Tuple[Tuple[str, str, Tuple[str, ...]], ...] = (
        ("agent_registry", "list", (AGENTS_DIR,)),
        ("context_rules", "map", (RULES_DIR,)),
        ("context_contracts", "map", (CONTRACTS_DIR,)),
        ("workflow_registry", "map", (WORKFLOWS_DIR, CUSTOM_WORKFLOWS_DIR)),
        ("workflow_hooks", "hooks", (WORKFLOWS_DIR, CUSTOM_WORKFLOWS_DIR)),
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
        data = self._load_yaml(manifest)
        stem = manifest.stem
        fallback = stem if stem.startswith("agent_") else f"agent_{stem}"
        if not isinstance(data, dict):
            return fallback
        meta = data.get("metadata", {}) if isinstance(data.get("metadata"), dict) else {}
        return meta.get("agent_id") or data.get("agent_id") or fallback

    def _load_yaml(self, path: Path) -> Any:
        if yaml is None:
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                if SafeLoader is not None:
                    return yaml.load(f, Loader=SafeLoader) or {}
                return yaml.safe_load(f) or {}
        except Exception:
            return None

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

    def scan_files_multi(self, rel_dirs: Tuple[str, ...]) -> List[str]:
        """Returns the sorted union of files across several canonical directories."""
        found: Set[str] = set()
        for rel_dir in rel_dirs:
            found.update(self.scan_files(rel_dir))
        return sorted(found)

    # ------------------------------------------------------------------
    # Workflow indexing & hook extraction
    # ------------------------------------------------------------------
    def _iter_workflows(self, rel_dirs: Tuple[str, ...]):
        for rel in self.scan_files_multi(rel_dirs):
            if not rel.endswith((".yaml", ".yml")):
                continue
            data = self._load_yaml(self.workspace_root / rel)
            if isinstance(data, dict):
                yield rel, data

    @staticmethod
    def _slug(value: Any) -> str:
        slug = re.sub(r"[^a-z0-9]+", "_", str(value).lower()).strip("_")
        return slug or "item"

    def _workflow_index(self, rel_dirs: Tuple[str, ...]) -> Tuple[Dict[str, str], Set[str]]:
        """Maps each workflow_id/id/stem alias to its artifact path."""
        id_to_path: Dict[str, str] = {}
        for rel, data in self._iter_workflows(rel_dirs):
            aliases: Set[str] = set()
            for key in ("workflow_id", "id"):
                val = data.get(key)
                if isinstance(val, str) and val:
                    aliases.add(val)
            stem = Path(rel).stem
            aliases.add(stem)
            if stem.startswith("wf_"):
                aliases.add(stem[3:])
            else:
                aliases.add(f"wf_{stem}")
            for alias in aliases:
                id_to_path.setdefault(alias, rel)
        return id_to_path, set(id_to_path.keys())

    @staticmethod
    def _hook_ids(raw: Any) -> List[str]:
        if isinstance(raw, dict):
            return [str(k) for k in raw.keys()]
        if isinstance(raw, list):
            ids: List[str] = []
            for item in raw:
                if isinstance(item, str):
                    ids.append(item)
                elif isinstance(item, dict):
                    val = item.get("id") or item.get("name") or item.get("event")
                    if val:
                        ids.append(str(val))
            return ids
        return []

    @staticmethod
    def _trigger_events(trigger: Any) -> List[str]:
        if isinstance(trigger, dict):
            events = trigger.get("events")
            if isinstance(events, list) and events:
                return [str(e) for e in events]
            ttype = trigger.get("type")
            if isinstance(ttype, str) and ttype:
                return [ttype]
            return []
        if isinstance(trigger, str) and trigger:
            return [trigger]
        if isinstance(trigger, list):
            return [str(e) for e in trigger if isinstance(e, str)]
        return []

    def _collect_hooks(self, rel_dirs: Tuple[str, ...]) -> Dict[str, str]:
        id_to_path, _ = self._workflow_index(rel_dirs)
        hooks: Dict[str, str] = {}

        for rel, data in self._iter_workflows(rel_dirs):
            wf_key = self._slug(data.get("workflow_id") or data.get("id") or Path(rel).stem)
            for hid in self._hook_ids(data.get("hooks")):
                hooks[f"{wf_key}__{self._slug(hid)}"] = rel
            for event in self._trigger_events(data.get("trigger")):
                hooks[f"{wf_key}__{self._slug(event)}"] = rel

        agents_dir = self.workspace_root / self.AGENTS_DIR
        if agents_dir.exists():
            for manifest in sorted(agents_dir.glob("*.yaml")) + sorted(agents_dir.glob("*.yml")):
                data = self._load_yaml(manifest)
                if not isinstance(data, dict):
                    continue
                meta = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
                agent_id = meta.get("agent_id") or data.get("agent_id") or self._read_agent_id(manifest)

                bindings: List[Tuple[Any, Any]] = []
                cicd = data.get("autonomous_cicd_hooks")
                if isinstance(cicd, dict):
                    for tw in cicd.get("target_workflows", []) or []:
                        if isinstance(tw, dict):
                            bindings.append((tw.get("workflow_id"), tw.get("step_id") or tw.get("insertion_point")))
                for wb in data.get("workflow_bindings", []) or []:
                    if isinstance(wb, dict):
                        bindings.append((wb.get("workflow_id"), wb.get("stage") or wb.get("step_id")))

                for workflow_id, step in bindings:
                    if not workflow_id:
                        continue
                    target = id_to_path.get(str(workflow_id), str(workflow_id))
                    key = f"{agent_id}__{self._slug(workflow_id)}__{self._slug(step or 'default')}"
                    hooks[key] = target

        return dict(sorted(hooks.items()))

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

    @staticmethod
    def _prefixes(rel_dirs: Tuple[str, ...]) -> Tuple[str, ...]:
        return tuple(rel.rstrip("/") + "/" for rel in rel_dirs)

    def _build_map(self, current: Any, rel_dirs: Tuple[str, ...]) -> Dict[str, str]:
        """Projects discovered files into a symbolic-key -> path map."""
        current = current if isinstance(current, dict) else {}
        prefixes = self._prefixes(rel_dirs)

        existing_key_by_path: Dict[str, str] = {}
        retained: Dict[str, str] = {}
        for key, value in current.items():
            if isinstance(value, str) and value.startswith(prefixes):
                existing_key_by_path[value] = key
            else:
                retained[key] = value

        result: Dict[str, str] = dict(retained)
        used = set(result.keys())
        for rel in self.scan_files_multi(rel_dirs):
            key = existing_key_by_path.get(rel)
            if not key or key in used:
                key = self._derive_key(rel, used)
            result[key] = rel
            used.add(key)
        return result

    def _build_hooks(self, current: Any, rel_dirs: Tuple[str, ...]) -> Dict[str, str]:
        """Reconciles workflow hook bindings into a symbolic-key -> workflow map."""
        current = current if isinstance(current, dict) else {}
        prefixes = self._prefixes(rel_dirs)
        _, workflow_ids = self._workflow_index(rel_dirs)
        desired = self._collect_hooks(rel_dirs)

        retained = {
            key: value
            for key, value in current.items()
            if key not in desired
            and not (isinstance(value, str) and (value.startswith(prefixes) or value in workflow_ids))
        }
        result: Dict[str, str] = dict(retained)
        result.update(desired)
        return result

    def _project(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Returns the fully synchronized settings document (non-mutating)."""
        projected = json.loads(json.dumps(data))  # deep copy, preserves order
        for settings_key, kind, sources in self.SPECS:
            if kind == "list":
                projected[settings_key] = self.scan_agent_ids()
            elif kind == "hooks":
                projected[settings_key] = self._build_hooks(data.get(settings_key), sources)
            else:
                projected[settings_key] = self._build_map(data.get(settings_key), sources)
        return projected

    def _section_drift(self, current: Any, desired: Any, sources: Tuple[str, ...], kind: str) -> Dict[str, Any]:
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
        prefixes = self._prefixes(sources)
        if kind == "hooks":
            _, workflow_ids = self._workflow_index(sources)
        else:
            workflow_ids = set()
        managed_current = {
            k: v
            for k, v in current_map.items()
            if k in desired_map
            or (isinstance(v, str) and (v.startswith(prefixes) or v in workflow_ids))
        }
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
            for settings_key, kind, sources in self.SPECS:
                drift = self._section_drift(data.get(settings_key), desired[settings_key], sources, kind)
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
