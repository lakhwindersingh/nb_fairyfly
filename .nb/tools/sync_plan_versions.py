#!/usr/bin/env python3
"""
Plan Version Synchronization Tool

Ensures concise, detailed, readme, and companion mini versions of plans stay synchronized.
Tracks SHA-256 content hashes, line counts, validates manifests, and reports drift.
"""

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import yaml


class PlanVersionSync:
    def __init__(self, plan_root: Path):
        self.plan_root = Path(plan_root)
        self.manifests: Dict[str, Dict] = {}

    def scan_plans(self) -> List[Path]:
        """Find all MANIFEST.yaml files."""
        return sorted(self.plan_root.rglob("MANIFEST.yaml"))

    def load_manifest(self, manifest_path: Path) -> Dict:
        """Load and validate manifest."""
        with open(manifest_path, encoding="utf-8") as f:
            manifest = yaml.safe_load(f)
        return manifest if isinstance(manifest, dict) else {}

    @staticmethod
    def compute_stats(file_path: Optional[Path]) -> Tuple[Optional[str], Optional[int]]:
        """Compute SHA-256 hash and line count of file content."""
        if not file_path or not file_path.is_file():
            return None, None
        raw = file_path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        lines = len(raw.decode("utf-8", errors="replace").splitlines())
        return digest, lines

    def compute_hash(self, file_path: Path) -> Optional[str]:
        """Compute SHA-256 hash of file content."""
        return self.compute_stats(file_path)[0]

    @staticmethod
    def _plan_identity(plan_dir: Path, manifest: Dict) -> Tuple[str, str]:
        plan_meta = manifest.get("plan") if isinstance(manifest.get("plan"), dict) else {}
        name = (
            plan_meta.get("name")
            or manifest.get("plan_name")
            or plan_meta.get("id")
            or manifest.get("plan_id")
            or plan_dir.name
        )
        layer = (
            plan_meta.get("layer")
            or manifest.get("layer")
            or manifest.get("layer_level")
            or manifest.get("capability_rating")
            or plan_dir.parent.name.upper()
        )
        return str(name), str(layer)

    def check_sync_status(self, plan_dir: Path, manifest: Dict) -> Dict:
        """Check if all tracked versions and line counts are in sync."""
        versions = manifest.get("versions") if isinstance(manifest.get("versions"), dict) else {}
        file_versions = manifest.get("file_versions") if isinstance(manifest.get("file_versions"), dict) else {}

        def resolve_rel(key: str, default: str) -> Optional[str]:
            if isinstance(versions.get(key), dict) and versions[key].get("file"):
                return versions[key]["file"]
            if isinstance(file_versions.get(key), dict) and file_versions[key].get("path"):
                return file_versions[key]["path"]
            return default

        concise_rel = resolve_rel("concise", "concise.md")
        detailed_rel = resolve_rel("detailed", "detailed.md")
        readme_rel = resolve_rel("readme", "README.md")

        concise_path = plan_dir / concise_rel if concise_rel else None
        detailed_path = plan_dir / detailed_rel if detailed_rel else None
        readme_path = plan_dir / readme_rel if readme_rel else None

        concise_hash, concise_lines = self.compute_stats(concise_path)
        detailed_hash, detailed_lines = self.compute_stats(detailed_path)
        readme_hash, readme_lines = self.compute_stats(readme_path)

        drift = False
        sync_meta = manifest.get("sync_status")
        if isinstance(sync_meta, dict) and sync_meta.get("in_sync") is False:
            drift = True
        if not versions and not file_versions:
            drift = True

        for section_name, section in (("versions", versions), ("file_versions", file_versions)):
            for key, entry in section.items():
                if not isinstance(entry, dict):
                    continue
                if entry.get("exists") is False and not entry.get("file") and not entry.get("path"):
                    continue
                rel = entry.get("file") or entry.get("path")
                if not rel:
                    drift = True
                    continue
                actual_hash, actual_lines = self.compute_stats(plan_dir / rel)
                if actual_hash is None:
                    drift = True
                    continue
                stored_hash = str(entry.get("content_hash") or "").removeprefix("sha256:")
                if not stored_hash or stored_hash != actual_hash:
                    drift = True
                for line_key in ("lines", "line_count"):
                    if line_key in entry and entry[line_key] != actual_lines:
                        drift = True

        concise_changed = False
        if concise_hash and isinstance(versions.get("concise"), dict):
            stored_c = str(versions["concise"].get("content_hash") or "").removeprefix("sha256:")
            concise_changed = bool(stored_c != concise_hash)
        detailed_changed = False
        if detailed_hash and isinstance(versions.get("detailed"), dict):
            stored_d = str(versions["detailed"].get("content_hash") or "").removeprefix("sha256:")
            detailed_changed = bool(stored_d != detailed_hash)

        return {
            "concise_exists": concise_hash is not None,
            "detailed_exists": detailed_hash is not None,
            "readme_exists": readme_hash is not None,
            "concise_changed": concise_changed,
            "detailed_changed": detailed_changed,
            "in_sync": not drift,
            "concise_hash": concise_hash,
            "concise_lines": concise_lines,
            "detailed_hash": detailed_hash,
            "detailed_lines": detailed_lines,
            "readme_hash": readme_hash,
            "readme_lines": readme_lines,
        }

    def update_manifest(self, plan_dir: Path, sync_status: Dict):
        """Ensure canonical plan block, versions hashes, line counts, and sync_status are synchronized."""
        manifest_path = plan_dir / "MANIFEST.yaml"
        manifest = self.load_manifest(manifest_path)
        now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Ensure top-level 'plan' mapping exists while preserving existing keys & order
        if not isinstance(manifest.get("plan"), dict):
            rel_dir = plan_dir.relative_to(self.plan_root).as_posix()
            inferred_id = rel_dir.replace("/", "_").replace("-", "_")
            pid = manifest.get("plan_id") or inferred_id
            pname = manifest.get("plan_name") or plan_dir.name
            layer = (
                manifest.get("layer")
                or manifest.get("layer_level")
                or manifest.get("capability_rating")
                or plan_dir.parent.name.upper()
            )
            plan_block = {
                "id": pid,
                "name": pname,
                "category": plan_dir.parent.name,
                "layer": layer,
            }
            if manifest.get("language"):
                plan_block["language"] = manifest["language"]
            if manifest.get("cargo_crate"):
                plan_block["cargo_crate"] = manifest["cargo_crate"]
            manifest = {"plan": plan_block, **manifest}

        if not isinstance(manifest.get("versions"), dict):
            manifest["versions"] = {}
        versions = manifest["versions"]

        for key, filename, fmt, target_tok in (
            ("concise", "concise.md", "token_optimized", 3500),
            ("detailed", "detailed.md", "implementation_spec", 35000),
            ("readme", "README.md", "overview", 1500),
        ):
            entry = versions.get(key)
            rel_file = entry.get("file", filename) if isinstance(entry, dict) else filename
            digest, line_cnt = self.compute_stats(plan_dir / rel_file)
            if digest is None:
                continue
            if not isinstance(entry, dict):
                if key == "readme" and "readme" not in versions:
                    # Add readme entry so README.md is also hash-tracked
                    entry = {"file": rel_file, "format": fmt, "version": str(manifest.get("version", "latest"))}
                else:
                    entry = {
                        "file": rel_file,
                        "format": fmt,
                        "target_tokens": target_tok,
                        "version": str(manifest.get("version", "latest")),
                    }
            entry["file"] = rel_file
            entry["last_updated"] = now_iso
            entry["content_hash"] = f"sha256:{digest}"
            entry["lines"] = line_cnt
            versions[key] = entry

        # Update any additional entries inside versions (e.g., mini, specification, architecture)
        for key, entry in list(versions.items()):
            if key in ("concise", "detailed", "readme") or not isinstance(entry, dict):
                continue
            rel_file = entry.get("file") or entry.get("path")
            if not rel_file:
                continue
            digest, line_cnt = self.compute_stats(plan_dir / rel_file)
            if digest is not None:
                entry["exists"] = True
                entry["last_updated"] = now_iso
                entry["content_hash"] = f"sha256:{digest}"
                entry["lines"] = line_cnt

        # If file_versions is also present, keep it strictly synchronized too
        if isinstance(manifest.get("file_versions"), dict):
            for key, entry in manifest["file_versions"].items():
                if not isinstance(entry, dict):
                    continue
                rel_file = entry.get("path") or entry.get("file")
                if not rel_file:
                    continue
                digest, line_cnt = self.compute_stats(plan_dir / rel_file)
                if digest is not None:
                    use_prefix = str(entry.get("content_hash", "")).startswith("sha256:")
                    entry["content_hash"] = f"sha256:{digest}" if use_prefix else digest
                    entry["line_count"] = line_cnt
                    entry["last_modified"] = today_str

        if not isinstance(manifest.get("sync_status"), dict):
            manifest["sync_status"] = {}
        manifest["sync_status"]["in_sync"] = True
        manifest["sync_status"]["last_sync"] = now_iso
        manifest["sync_status"].setdefault("sync_direction", "concise_to_detailed")
        manifest["sync_status"]["differences"] = []

        with open(manifest_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(manifest, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

    def generate_sync_report(self) -> str:
        """Generate markdown report of sync status across all plans."""
        now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        report = ["# Plan Version Sync Report\n", f"Generated: {now_iso}\n\n"]

        manifests = self.scan_plans()
        if not manifests:
            report.append("⚠️  No MANIFEST.yaml files found.\n")
            return "".join(report)

        report.append("| Plan | Layer | Concise | Detailed | README | In Sync | Status |\n")
        report.append("|------|-------|---------|----------|--------|---------|--------|\n")

        for manifest_path in manifests:
            plan_dir = manifest_path.parent
            manifest = self.load_manifest(manifest_path)
            if not manifest:
                continue
            sync_status = self.check_sync_status(plan_dir, manifest)
            plan_name, layer = self._plan_identity(plan_dir, manifest)

            concise_icon = "✅" if sync_status["concise_exists"] else "❌"
            detailed_icon = "✅" if sync_status["detailed_exists"] else "⚠️"
            readme_icon = "✅" if sync_status["readme_exists"] else "⚠️"
            sync_icon = "✅" if sync_status["in_sync"] else "❌"
            status = "In Sync" if sync_status["in_sync"] else "⚠️ Drift Detected"

            report.append(
                f"| {plan_name} | {layer} | {concise_icon} | {detailed_icon} | {readme_icon} | {sync_icon} | {status} |\n"
            )

        return "".join(report)

    def sync_all(self):
        """Update all manifests with current file hashes and line counts."""
        manifests = self.scan_plans()
        if not manifests:
            print("⚠️  No MANIFEST.yaml files found.")
            return

        for manifest_path in manifests:
            plan_dir = manifest_path.parent
            manifest = self.load_manifest(manifest_path)
            if not manifest:
                continue
            sync_status = self.check_sync_status(plan_dir, manifest)
            self.update_manifest(plan_dir, sync_status)
            plan_name, _ = self._plan_identity(plan_dir, manifest)
            if sync_status["in_sync"]:
                print(f"✅ {plan_name}: Verified in sync")
            else:
                print(f"🔄 {plan_name}: Synchronized manifest hashes & line counts")


if __name__ == "__main__":
    import sys

    plan_root = Path(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else ".nb/plan")
    sync = PlanVersionSync(plan_root)

    if "--report" in sys.argv:
        print(sync.generate_sync_report())
    else:
        sync.sync_all()
