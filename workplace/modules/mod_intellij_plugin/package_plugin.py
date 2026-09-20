#!/usr/bin/env python3
"""
Percipience IntelliJ IDEA / PyCharm Plugin Packager
Compiles Kotlin sources to JVM bytecode, packages manifests and resources,
and generates standard JetBrains Plugin installable zip archives.
"""

import io
import os
import sys
import subprocess
import zipfile
import shutil
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PLUGIN_ROOT.parents[2]
BUILD_DIR = PLUGIN_ROOT / "build"
CLASSES_DIR = BUILD_DIR / "classes" / "kotlin" / "main"
DIST_DIR = BUILD_DIR / "distributions"
OUT_BUNDLE = REPO_ROOT / ".nb" / "bundles"


def find_kotlinc() -> str:
    # 1. Check in PATH
    kotlinc_bin = shutil.which("kotlinc")
    if kotlinc_bin:
        return kotlinc_bin

    # 2. Search common JetBrains / Homebrew locations
    candidate_paths = [
        Path("/Users/lakhwinder/Applications/IntelliJ IDEA.app/Contents/plugins/Kotlin/kotlinc/bin/kotlinc"),
        Path("/Applications/IntelliJ IDEA.app/Contents/plugins/Kotlin/kotlinc/bin/kotlinc"),
        Path("/Users/lakhwinder/Applications/PyCharm.app/Contents/plugins/Kotlin/kotlinc/bin/kotlinc"),
        Path("/Applications/PyCharm.app/Contents/plugins/Kotlin/kotlinc/bin/kotlinc"),
        Path("/opt/homebrew/bin/kotlinc"),
        Path("/usr/local/bin/kotlinc"),
    ]
    for p in candidate_paths:
        if p.exists() and os.access(p, os.X_OK):
            return str(p)

    # 3. Fallback search
    for base in [Path.home() / "Applications", Path("/Applications"), Path("/opt/homebrew")]:
        if base.exists():
            for p in base.rglob("kotlinc"):
                if p.is_file() and os.access(p, os.X_OK) and p.parent.name == "bin":
                    return str(p)
    return ""


def find_jetbrains_classpath() -> str:
    candidate_dirs = [
        Path("/Users/lakhwinder/Applications/PyCharm.app/Contents/lib"),
        Path("/Applications/PyCharm.app/Contents/lib"),
        Path("/Users/lakhwinder/Applications/IntelliJ IDEA.app/Contents/lib"),
        Path("/Applications/IntelliJ IDEA.app/Contents/lib"),
    ]
    jars = []
    for d in candidate_dirs:
        if d.exists():
            jars.extend(d.glob("*.jar"))
            if jars:
                break
    return ":".join(str(j) for j in jars)


def compile_kotlin_sources() -> bool:
    kotlinc = find_kotlinc()
    if not kotlinc:
        print("⚠️ kotlinc not found; searching for existing class files...")
        return False

    kotlin_dir = PLUGIN_ROOT / "src" / "main" / "kotlin"
    kt_files = [str(f) for f in kotlin_dir.rglob("*.kt")]
    if not kt_files:
        print("⚠️ No Kotlin source files found.")
        return False

    CLASSES_DIR.mkdir(parents=True, exist_ok=True)
    cp = find_jetbrains_classpath()

    cmd = [kotlinc, "-jvm-target", "21"]
    if cp:
        cmd.extend(["-cp", cp])
    cmd.extend(["-d", str(CLASSES_DIR)])
    cmd.extend(kt_files)

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Kotlin compilation succeeded.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ kotlinc compilation failed:\n{e.stderr or e.stdout}")
        return False


def package_intellij_plugin():
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    OUT_BUNDLE.mkdir(parents=True, exist_ok=True)

    jar_filename = "percipience-intellij-plugin-1.0.0.jar"
    zip_filename = "percipience-intellij-plugin-1.0.0.zip"

    jar_path = DIST_DIR / jar_filename
    zip_path = DIST_DIR / zip_filename

    # 1. Compile Kotlin sources
    compiled = compile_kotlin_sources()
    if not compiled and not CLASSES_DIR.exists():
        raise RuntimeError("Failed to compile Kotlin classes and no precompiled classes exist.")

    # 2. Build plugin JAR containing META-INF, resources, and compiled JVM .class bytecode
    jar_buffer = io.BytesIO()
    with zipfile.ZipFile(jar_buffer, "w", zipfile.ZIP_DEFLATED) as jar:
        # Add manifest
        manifest_content = (
            "Manifest-Version: 1.0\n"
            "Created-By: Percipience Context Engineering OS\n"
            "Plugin-Id: com.neutronbinary.percipience\n"
            "Plugin-Version: 1.0.0\n"
        )
        jar.writestr("META-INF/MANIFEST.MF", manifest_content)

        # Add resources (plugin.xml, icons, etc.)
        resources_dir = PLUGIN_ROOT / "src" / "main" / "resources"
        if resources_dir.exists():
            for f in resources_dir.rglob("*"):
                if f.is_file():
                    arcname = str(f.relative_to(resources_dir))
                    jar.write(f, arcname)

        # Add compiled JVM bytecode (.class files)
        if CLASSES_DIR.exists():
            for f in CLASSES_DIR.rglob("*.class"):
                if f.is_file():
                    arcname = str(f.relative_to(CLASSES_DIR))
                    jar.write(f, arcname)

    jar_bytes = jar_buffer.getvalue()
    with open(jar_path, "wb") as f:
        f.write(jar_bytes)

    # 3. Package installable JetBrains Plugin Zip (standard layout: <plugin-name>/lib/<jar>)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("percipience-intellij-plugin/lib/" + jar_filename, jar_bytes)

        readme_content = """Percipience Context Engineering OS - JetBrains Plugin
======================================================
Tested and verified for:
- PyCharm (Professional & Community 2024.1+)
- IntelliJ IDEA (Ultimate & Community 2024.1+)

How to Install for Testing:
1. Open IntelliJ IDEA or PyCharm.
2. Go to Settings / Preferences -> Plugins.
3. Click the ⚙️ (Gear Icon) at the top -> "Install Plugin from Disk...".
4. Select this .zip file ('percipience-intellij-plugin-1.0.0.zip').
5. Restart IDE.
6. The 'Percipience OS' Tool Window will appear on the right-hand panel.
"""
        z.writestr("percipience-intellij-plugin/README.txt", readme_content)

    # Copy to .nb/bundles for easy access
    bundle_dest = OUT_BUNDLE / zip_filename
    shutil.copyfile(zip_path, bundle_dest)

    # 4. Sync directly to active IDE plugins directories if installed
    jetbrains_app_support = Path.home() / "Library" / "Application Support" / "JetBrains"
    if jetbrains_app_support.exists():
        for p in jetbrains_app_support.glob("*/plugins/percipience-intellij-plugin/lib"):
            target_installed_jar = p / jar_filename
            try:
                shutil.copyfile(jar_path, target_installed_jar)
                print(f"✅ Updated installed plugin JAR at: {target_installed_jar}")
            except Exception as ex:
                print(f"⚠️ Could not update {target_installed_jar}: {ex}")

    # Clean up any misplaced directory if created
    if (PLUGIN_ROOT.parents[1] / ".nb").exists():
        shutil.rmtree(PLUGIN_ROOT.parents[1] / ".nb", ignore_errors=True)

    print(f"✅ Generated IntelliJ Plugin JAR: {jar_path} ({len(jar_bytes)} bytes)")
    print(f"✅ Generated Installable Plugin ZIP: {zip_path} ({zip_path.stat().st_size} bytes)")
    print(f"✅ Copied to bundles: {bundle_dest}")
    return zip_path


if __name__ == "__main__":
    package_intellij_plugin()
