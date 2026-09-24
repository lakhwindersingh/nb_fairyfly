#!/usr/bin/env python3
"""
Percipience IntelliJ IDEA & PyCharm Plugin Packager
Bundles Kotlin/Java classes, resources, plugin.xml, percipience runtime assets,
and generates both standard JetBrains Plugin distribution JAR & ZIP archives
as well as the encrypted domain .nbpack envelope.
"""

import io
import os
import sys
import zipfile
import shutil
import hashlib
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PLUGIN_ROOT.parents[2]
DIST_DIR = PLUGIN_ROOT / "build" / "distributions"
OUT_BUNDLE = REPO_ROOT / ".nb" / "bundles"
PLANS_DIR = REPO_ROOT / ".nb" / "plan"

sys.path.insert(0, str(REPO_ROOT / ".nb" / "core"))
sys.path.insert(0, str(REPO_ROOT / "workplace" / "core"))
from nbpack_envelope import NBPackEnvelope
from commercial_packager_provisioner import CommercialPackagerProvisioner


def build_intellij_plugin_jar(jar_path: Path):
    """Builds the plugin JAR containing classes, META-INF, and embedded runtime."""
    classes_dir = PLUGIN_ROOT / "build" / "classes" / "kotlin" / "main"
    src_kotlin = PLUGIN_ROOT / "src" / "main" / "kotlin"
    resources_dir = PLUGIN_ROOT / "src" / "main" / "resources"

    jar_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(jar_path, "w", zipfile.ZIP_DEFLATED) as z:
        # 1. Add compiled classes if present
        if classes_dir.exists():
            for f in classes_dir.rglob("*"):
                if f.is_file():
                    arcname = str(f.relative_to(classes_dir))
                    z.write(f, arcname)

        # 2. Add Kotlin source files (for source JAR & SDK inspection)
        if src_kotlin.exists():
            for f in src_kotlin.rglob("*.kt"):
                if f.is_file():
                    arcname = "src/" + str(f.relative_to(src_kotlin))
                    z.write(f, arcname)

        # 3. Add resources (META-INF, percipience runtime)
        if resources_dir.exists():
            for f in resources_dir.rglob("*"):
                if f.is_file():
                    arcname = str(f.relative_to(resources_dir))
                    z.write(f, arcname)

    print(f"📦 Built Plugin JAR: {jar_path} ({jar_path.stat().st_size:,} bytes)")


def build_intellij_plugin_zip(jar_path: Path, zip_path: Path):
    """Builds the standard JetBrains plugin distribution ZIP (lib/plugin.jar structure)."""
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    plugin_folder_name = "percipience-intellij-plugin"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        # Put jar under <plugin-name>/lib/<plugin-name>.jar
        arcname = f"{plugin_folder_name}/lib/{jar_path.name}"
        z.write(jar_path, arcname)

        # Add README & license inside zip root
        guide = PLUGIN_ROOT / "PLUGIN_USER_GUIDE.md"
        if guide.exists():
            z.write(guide, f"{plugin_folder_name}/PLUGIN_USER_GUIDE.md")

        # Add plugin manifest copy
        plugin_xml = PLUGIN_ROOT / "src" / "main" / "resources" / "META-INF" / "plugin.xml"
        if plugin_xml.exists():
            z.write(plugin_xml, f"{plugin_folder_name}/META-INF/plugin.xml")

    print(f"📦 Built Plugin ZIP Distribution: {zip_path} ({zip_path.stat().st_size:,} bytes)")


def package_intellij_bundle():
    """Generates JAR, ZIP, and .nbpack layer package for IntelliJ / PyCharm."""
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    OUT_BUNDLE.mkdir(parents=True, exist_ok=True)

    # 1. Provision runtime assets first
    print("🚀 Provisioning runtime bundle to IntelliJ plugin resources...")
    CommercialPackagerProvisioner.provision_target(
        workspace_root=REPO_ROOT,
        tenant_id="tenant_community_default",
        tier="plan_free",
        target="intellij"
    )

    # 2. Build JAR & ZIP
    jar_filename = "percipience-intellij-plugin-1.0.0.jar"
    zip_filename = "percipience-intellij-plugin-1.0.0.zip"
    
    jar_path = DIST_DIR / jar_filename
    zip_path = DIST_DIR / zip_filename

    build_intellij_plugin_jar(jar_path)
    build_intellij_plugin_zip(jar_path, zip_path)

    # 3. Copy to .nb/bundles
    bundle_jar = OUT_BUNDLE / jar_filename
    bundle_zip = OUT_BUNDLE / zip_filename
    shutil.copy2(jar_path, bundle_jar)
    shutil.copy2(zip_path, bundle_zip)

    # 4. Compile .nbpack layer
    plan_file = PLANS_DIR / "l1" / "intellij-pycharm-plugin" / "detailed.md"
    nbpack_path = OUT_BUNDLE / "intellij_pycharm_plugin_domain.nbpack"
    if plan_file.exists():
        print(f"🔒 Compiling Ed25519-signed .nbpack layer from {plan_file}...")
        res_nbpack = NBPackEnvelope.compile_layer_pack(REPO_ROOT, plan_file, nbpack_path)
        print(f"✅ Generated .nbpack domain layer: {res_nbpack} ({res_nbpack.stat().st_size:,} bytes)")

    print(f"\n✨ All IntelliJ Plugin bundles successfully created:")
    print(f"   • JAR: {bundle_jar} ({bundle_jar.stat().st_size:,} bytes)")
    print(f"   • ZIP: {bundle_zip} ({bundle_zip.stat().st_size:,} bytes)")
    print(f"   • NBPACK: {nbpack_path} ({nbpack_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    package_intellij_bundle()
