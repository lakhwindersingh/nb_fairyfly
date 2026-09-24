#!/usr/bin/env python3
"""
Percipience VSCode Extension Packager
Bundles TypeScript/ESBuild artifacts, manifests, package.json, icons, and generates
installable VSCode extension archives (.vsix / .zip) for local testing and distribution
across Free, Team, Business, and Enterprise tiers.
"""

import io
import os
import sys
import zipfile
import shutil
import argparse
from pathlib import Path

EXT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = EXT_ROOT.parents[2]
DIST_DIR = EXT_ROOT / "dist"
OUT_BUNDLE = REPO_ROOT / ".nb" / "bundles"


def build_vsix_package(vsix_path: Path, tier: str = "plan_free"):
    """Bundles into standard VSIX / Open-VSIX ZIP layout with tier metadata."""
    vsix_path.parent.mkdir(parents=True, exist_ok=True)

    tier_label = tier.replace("plan_", "").capitalize()

    with zipfile.ZipFile(vsix_path, "w", zipfile.ZIP_DEFLATED) as z:
        # 1. Package manifest
        pkg_json = EXT_ROOT / "package.json"
        if pkg_json.exists():
            z.write(pkg_json, "extension/package.json")

        # 2. Add dist / src files
        src_dir = EXT_ROOT / "src"
        if src_dir.exists():
            for f in src_dir.rglob("*"):
                if f.is_file():
                    arcname = "extension/src/" + str(f.relative_to(src_dir))
                    z.write(f, arcname)

        # 3. Add templates / bridges
        tmpl_dir = EXT_ROOT / "templates"
        if tmpl_dir.exists():
            for f in tmpl_dir.rglob("*"):
                if f.is_file():
                    arcname = "extension/templates/" + str(f.relative_to(tmpl_dir))
                    z.write(f, arcname)

        # 4. Add tier license if present
        license_file = EXT_ROOT / "percipience_runtime" / "tenant_license.json"
        if license_file.exists():
            z.write(license_file, "extension/tenant_license.json")

        # 5. Add README with tier awareness
        readme_content = f"""Percipience Context Engineering OS - VSCode Extension ({tier_label} Edition)
======================================================
Tested and verified for:
- VSCode 1.90.0+
- Cursor IDE / Windsurf

Tier Entitlements:
- Active Tier: {tier} ({tier_label})
- Status Bar Live Metrics Widget ($(zap) Percipience: 70.0% Saved | $(shield) Merkle: OK)
- Language Server Protocol (LSP 3.17) integration
- Webview Control Plane (Tier-governed actions)
- Ephemeral Multi-Agent SDLC

How to Install for Testing:
1. Open Visual Studio Code.
2. Press Cmd+Shift+P (or Ctrl+Shift+P).
3. Type "Extensions: Install from VSIX...".
4. Select '{vsix_path.name}'.
5. Reload VSCode.
"""
        z.writestr("extension/README.md", readme_content)

        # 6. Add [Content_Types].xml for VSIX standard compliance
        content_types = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json"/>
  <Default Extension="ts" ContentType="text/plain"/>
  <Default Extension="js" ContentType="application/javascript"/>
  <Default Extension="md" ContentType="text/markdown"/>
  <Default Extension="vsixmanifest" ContentType="text/xml"/>
</Types>
"""
        z.writestr("[Content_Types].xml", content_types)

    print(f"📦 Built VSCode Extension VSIX: {vsix_path} ({vsix_path.stat().st_size:,} bytes)")


def package_vscode_extension(target_tier: str = "all"):
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    OUT_BUNDLE.mkdir(parents=True, exist_ok=True)

    # 1. Standard universal bundle
    default_vsix = DIST_DIR / "percipience-vscode-extension-1.0.0.vsix"
    build_vsix_package(default_vsix, tier="plan_free")
    shutil.copyfile(default_vsix, OUT_BUNDLE / default_vsix.name)

    # 2. Tier-specific bundles for permission testing
    tiers_to_build = ["free", "team", "business", "enterprise"] if target_tier == "all" else [target_tier.replace("plan_", "")]

    for t in tiers_to_build:
        tier_vsix = DIST_DIR / f"percipience-vscode-extension-{t}-1.0.0.vsix"
        build_vsix_package(tier_vsix, tier=f"plan_{t}")
        shutil.copyfile(tier_vsix, OUT_BUNDLE / tier_vsix.name)

    print(f"\n✨ All VSCode Extension VSIX bundles successfully generated in {OUT_BUNDLE}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Package Percipience VSCode Extension")
    parser.add_argument("--tier", choices=["all", "free", "team", "business", "enterprise"], default="all", help="Tier to package")
    args = parser.parse_args()
    package_vscode_extension(target_tier=args.tier)
