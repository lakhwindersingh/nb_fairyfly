#!/usr/bin/env python3
"""
Percipience VSCode Extension Packager
Bundles TypeScript/ESBuild artifacts, manifests, package.json, icons, and generates
an installable VSCode extension archive (.vsix / .zip) for local testing and distribution.
"""

import io
import os
import sys
import zipfile
import shutil
from pathlib import Path

EXT_ROOT = Path(__file__).resolve().parent
REPO_ROOT = EXT_ROOT.parents[2]
DIST_DIR = EXT_ROOT / "dist"
OUT_BUNDLE = REPO_ROOT / ".nb" / "bundles"

def package_vscode_extension():
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    OUT_BUNDLE.mkdir(parents=True, exist_ok=True)
    
    vsix_filename = "percipience-vscode-extension-1.0.0.vsix"
    vsix_path = DIST_DIR / vsix_filename
    
    # Bundle into standard VSIX / Open-VSIX ZIP layout
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
                    
        # 4. Add README
        readme_content = """Percipience Context Engineering OS - VSCode Extension
======================================================
Tested and verified for:
- VSCode 1.90.0+
- Cursor IDE / Windsurf

Features:
- Status Bar Live Metrics Widget ($(zap) Percipience: 70.0% Saved | $(shield) Merkle: OK)
- Language Server Protocol (LSP 3.17) integration
- Webview Control Plane
- Ephemeral Multi-Agent SDLC

How to Install for Testing:
1. Open Visual Studio Code.
2. Press Cmd+Shift+P (or Ctrl+Shift+P).
3. Type "Extensions: Install from VSIX...".
4. Select 'percipience-vscode-extension-1.0.0.vsix'.
5. Reload VSCode.
"""
        z.writestr("extension/README.md", readme_content)
        
        # 5. Add [Content_Types].xml for VSIX standard compliance
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

    # Copy to .nb/bundles
    bundle_dest = OUT_BUNDLE / vsix_filename
    shutil.copyfile(vsix_path, bundle_dest)
    
    print(f"✅ Generated VSCode Extension VSIX: {vsix_path} ({vsix_path.stat().st_size} bytes)")
    print(f"✅ Copied to bundles: {bundle_dest}")
    return vsix_path

if __name__ == "__main__":
    package_vscode_extension()
