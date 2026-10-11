#!/usr/bin/env python3
import sys
import yaml
from pathlib import Path

def inject_security_mesh(workspace_root: Path, target_plan_dir: Path):
    print(f"🛡️ Injecting Security Mesh into target plan: {target_plan_dir.name}")
    
    assert target_plan_dir.exists(), f"Target plan not found: {target_plan_dir}"
    manifest_file = target_plan_dir / "MANIFEST.yaml"
    assert manifest_file.exists(), f"Missing MANIFEST.yaml in target plan: {manifest_file}"

    # 1. Update Target Manifest Dependencies
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)
    
    deps = manifest.get("dependencies", [])
    if "security-mesh" not in deps:
        deps.append("security-mesh")
        manifest["dependencies"] = deps
        print("   ✅ Added 'security-mesh' dependency to target plan manifest.")

    # 2. Inject Security Capabilities
    caps = manifest.get("modular_breakdown", {}).get("capabilities", [])
    security_caps = [
        "Multi-Tenant Row-Level Security (RLS) Isolation",
        "FIDO2 / WebAuthn Hardware Passkeys & Adaptive MFA",
        "Continuous Zero-Trust Authorization & SPIFFE/SPIRE mTLS",
        "NIST SP 800-38G Format-Preserving Encryption (FPE) & PII Scrubber",
        "Cloud Security Posture Management & SEC 17a-4 WORM Egress"
    ]
    for sc in security_caps:
        if sc not in caps:
            caps.append(sc)
            print(f"   ✅ Injected capability: {sc}")
    
    with open(manifest_file, "w", encoding="utf-8") as f:
        yaml.safe_dump(manifest, f, sort_keys=False)
    
    print(f"🎉 Successfully injected Security Mesh into {target_plan_dir.name}!")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inject_security_mesh.py <target_plan_dir>")
        sys.exit(1)
    root = Path(__file__).resolve().parents[3]
    target = Path(sys.argv[1])
    if not target.is_absolute():
        target = root / target
    inject_security_mesh(root, target)
