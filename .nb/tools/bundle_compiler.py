#!/usr/bin/env python3
"""
Percipience Cryptographic Plan Pack Compiler
Compiles all active tiered plans in .nb/plan into encrypted, Ed25519-signed .nbpack bundles in .nb/plan/bundle.
Uses AES-256-GCM authenticated encryption and Ed25519 digital signatures.
"""

import os
import json
import zlib
import shutil
import hashlib
from pathlib import Path
import yaml
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

MAGIC_HEADER = b"NBPACK1"
ASSOCIATED_DATA = b"PERCIPIENCE_NBPACK_V1"

TEXT_EXTENSIONS = {
    ".md", ".yaml", ".yml", ".json", ".py", ".css", ".html", ".toml", ".rs"
}


def ensure_keys(key_dir=".nb/keys"):
    os.makedirs(key_dir, exist_ok=True)

    aes_key_path = os.path.join(key_dir, "enclave.key")
    priv_key_path = os.path.join(key_dir, "signing_ed25519.pem")
    pub_key_path = os.path.join(key_dir, "signing_ed25519.pub")

    if os.path.exists(aes_key_path):
        with open(aes_key_path, "rb") as f:
            aes_key = f.read()
    else:
        aes_key = AESGCM.generate_key(bit_length=256)
        with open(aes_key_path, "wb") as f:
            f.write(aes_key)
        print(f"[KeyManager] Generated new AES-256 Enclave Key at {aes_key_path}")

    if os.path.exists(priv_key_path) and os.path.exists(pub_key_path):
        with open(priv_key_path, "rb") as f:
            priv_key = serialization.load_pem_private_key(f.read(), password=None)
        with open(pub_key_path, "rb") as f:
            pub_key = serialization.load_pem_public_key(f.read())
    else:
        priv_key = ed25519.Ed25519PrivateKey.generate()
        pub_key = priv_key.public_key()

        priv_bytes = priv_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        pub_bytes = pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        with open(priv_key_path, "wb") as f:
            f.write(priv_bytes)
        with open(pub_key_path, "wb") as f:
            f.write(pub_bytes)
        print(f"[KeyManager] Generated new Ed25519 Keypair at {key_dir}")

    return aes_key, priv_key, pub_key


def build_envelope(payload_dict, aes_key, priv_key):
    raw_json = json.dumps(payload_dict, indent=2, sort_keys=True).encode("utf-8")
    uncompressed_len = len(raw_json)
    compressed_bytes = zlib.compress(raw_json, level=9)

    nonce = os.urandom(12)
    aesgcm = AESGCM(aes_key)
    ciphertext = aesgcm.encrypt(nonce, compressed_bytes, ASSOCIATED_DATA)

    signature = priv_key.sign(ciphertext)

    envelope = MAGIC_HEADER + nonce + signature + ciphertext
    envelope_hash = hashlib.sha256(envelope).hexdigest()

    return envelope, envelope_hash, uncompressed_len, len(ciphertext), signature.hex()


def verify_envelope(envelope_bytes, aes_key, pub_key):
    if not envelope_bytes.startswith(MAGIC_HEADER):
        raise ValueError("Invalid magic header")
    nonce = envelope_bytes[7:19]
    signature = envelope_bytes[19:83]
    ciphertext = envelope_bytes[83:]

    pub_key.verify(signature, ciphertext)

    aesgcm = AESGCM(aes_key)
    decompressed = aesgcm.decrypt(nonce, ciphertext, ASSOCIATED_DATA)
    raw_json = zlib.decompress(decompressed).decode("utf-8")
    return json.loads(raw_json)


def _collect_plan_dir_files(plan_dir: Path, base_dir: Path) -> dict:
    collected = {}
    for p in sorted(plan_dir.rglob("*")):
        if not p.is_file() or p.name.startswith("."):
            continue
        rel_parts = p.relative_to(plan_dir).parts
        if "archive" in rel_parts or "__pycache__" in rel_parts:
            continue
        if p.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        rel_key = p.relative_to(base_dir).as_posix()
        collected[rel_key] = p.read_text(encoding="utf-8", errors="replace")
    return collected


def compile_all():
    base_dir = Path(".").resolve()
    plan_dir = base_dir / ".nb" / "plan"
    output_bundle_dir = plan_dir / "bundle"
    output_bundle_dir.mkdir(parents=True, exist_ok=True)

    print("[*] Compiling encrypted nbpack bundles...")
    print(f"    Source: {plan_dir}")
    print(f"    Destination: {output_bundle_dir}")

    aes_key, priv_key, pub_key = ensure_keys()

    # Remove stale .nbpack files before fresh compilation
    for existing in output_bundle_dir.glob("*.nbpack"):
        existing.unlink()

    manifest_records = []
    consolidated_files = {}

    # 1. Process all active tiered MANIFEST.yaml plans
    manifests = sorted(plan_dir.rglob("MANIFEST.yaml"))
    for mpath in manifests:
        rel_parts = mpath.relative_to(plan_dir).parts
        if "archive" in rel_parts or "bundle" in rel_parts:
            continue

        raw_manifest = yaml.safe_load(mpath.read_text(encoding="utf-8")) or {}
        plan_meta = raw_manifest.get("plan") if isinstance(raw_manifest.get("plan"), dict) else {}
        rel_dir = mpath.parent.relative_to(plan_dir).as_posix()
        inferred_id = rel_dir.replace("/", "_").replace("-", "_")
        plan_id = str(plan_meta.get("id") or raw_manifest.get("plan_id") or inferred_id).strip()
        plan_name = str(plan_meta.get("name") or raw_manifest.get("plan_name") or mpath.parent.name).strip()
        plan_type = str(plan_meta.get("category") or raw_manifest.get("plan_type") or mpath.parent.parent.name)

        plan_files = _collect_plan_dir_files(mpath.parent, base_dir)
        consolidated_files.update(plan_files)

        primary_md = mpath.parent / "detailed.md"
        if not primary_md.is_file():
            primary_md = mpath.parent / "concise.md"
        primary_content = primary_md.read_text(encoding="utf-8") if primary_md.is_file() else ""
        source_rel = mpath.relative_to(base_dir).as_posix()

        payload = {
            "format": "PERCIPIENCE_NBPACK_V1",
            "plan_id": plan_id,
            "plan_name": plan_name,
            "plan_type": plan_type,
            "plan_directory": f".nb/plan/{rel_dir}",
            "source_file": source_rel,
            "manifest": raw_manifest,
            "content": primary_content,
            "files": plan_files,
        }

        envelope, env_hash, uncompressed_len, cipher_len, sig_hex = build_envelope(payload, aes_key, priv_key)
        bundle_filename = f"{plan_id}.nbpack"
        bundle_path = output_bundle_dir / bundle_filename
        bundle_path.write_bytes(envelope)

        manifest_records.append(
            {
                "bundle_file": bundle_filename,
                "plan_id": plan_id,
                "plan_name": plan_name,
                "source_file": source_rel,
                "sha256": env_hash,
                "raw_bytes": uncompressed_len,
                "encrypted_bytes": cipher_len,
                "envelope_bytes": len(envelope),
                "signature_ed25519": sig_hex,
            }
        )
        print(f"  [✔] Encrypted: {bundle_filename} (SHA-256: {env_hash[:12]}... | {len(envelope)} bytes)")

    # 2. Include root index/rating/free_plan and l3/mini/*.md in consolidated set
    for extra in sorted(plan_dir.glob("*.md")) + sorted((plan_dir / "l3" / "mini").glob("*.md")):
        if extra.is_file():
            consolidated_files[extra.relative_to(base_dir).as_posix()] = extra.read_text(encoding="utf-8")

    # 3. Process Consolidated Master Bundle of ALL Plans (+ alias parent_master_all_plans.nbpack)
    all_payload = {
        "format": "PERCIPIENCE_NBPACK_MASTER_V1",
        "plan_id": "all_plans_master",
        "plan_name": "Consolidated All Plans Master Pack",
        "bundle_type": "all_plans_consolidated",
        "description": "Complete sealed repository of all active master, architecture, and L1-L5 plans and specifications",
        "total_files": len(consolidated_files),
        "content": (plan_dir / "README.md").read_text(encoding="utf-8"),
        "files": consolidated_files,
    }

    all_envelope, all_hash, all_uncompressed, all_cipher, all_sig = build_envelope(all_payload, aes_key, priv_key)
    for bname, pid, pname in (
        ("all_plans.nbpack", "all_plans_master", "Consolidated All Plans Master Pack"),
        ("parent_master_all_plans.nbpack", "parent_master_all_plans", "Consolidated Parent Master All Plans Alias"),
    ):
        bpath = output_bundle_dir / bname
        bpath.write_bytes(all_envelope)
        manifest_records.append(
            {
                "bundle_file": bname,
                "plan_id": pid,
                "plan_name": pname,
                "source_file": ".nb/plan/README.md",
                "sha256": all_hash,
                "raw_bytes": all_uncompressed,
                "encrypted_bytes": all_cipher,
                "envelope_bytes": len(all_envelope),
                "signature_ed25519": all_sig,
            }
        )

    print(
        f"  [★] Consolidated Master Bundle: all_plans.nbpack "
        f"({len(consolidated_files)} files | SHA-256: {all_hash[:12]}... | {len(all_envelope)} bytes)"
    )

    # 4. Write Manifest, Checksums & README
    manifest_path = output_bundle_dir / "bundle_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "generator": "Percipience Plan Pack Compiler v2.1",
                "cipher": "AES-256-GCM (96-bit nonce, 128-bit auth tag)",
                "signature": "Ed25519 (RFC 8032)",
                "total_bundles": len(manifest_records),
                "bundles": manifest_records,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    checksums_path = output_bundle_dir / "checksums.sha256"
    checksums_path.write_text(
        "".join(f"{r['sha256']}  {r['bundle_file']}\n" for r in manifest_records),
        encoding="utf-8",
    )

    readme_path = output_bundle_dir / "README.md"
    readme_path.write_text(
        f"""# Percipience Encrypted Plan Bundles (`.nbpack`)

This directory contains cryptographically sealed and authenticated `.nbpack` bundles for all active plans in `.nb/plan/`.

## Cryptographic Guarantees
- **Authenticated Encryption**: AES-256-GCM (128-bit authentication tag, 96-bit unique IV).
- **Asymmetric Non-Repudiation**: Ed25519 digital signature over the ciphertext envelope.
- **Compression**: zlib level 9 compression before encryption.
- **Volatile Enclave Hydration**: Bundles are designed to hydrate directly into in-memory RAM/tmpfs without persisting unencrypted source markdown files to disk.

## Verification & Manifest
- **Manifest**: [`bundle_manifest.json`](./bundle_manifest.json)
- **Checksums**: [`checksums.sha256`](./checksums.sha256)
- **Total Bundles**: {len(manifest_records)}

## Keys
- Public Key: `.nb/keys/signing_ed25519.pub`
- Master Enclave Key: `.nb/keys/enclave.key`
""",
        encoding="utf-8",
    )

    print(f"[✔] Successfully generated {len(manifest_records)} encrypted .nbpack bundles in {output_bundle_dir}")

    # 5. Verify all generated bundles
    print("[*] Running cryptographic verification audit on all generated bundles...")
    for rec in manifest_records:
        bfile = rec["bundle_file"]
        bpath = output_bundle_dir / bfile
        data = bpath.read_bytes()
        payload = verify_envelope(data, aes_key, pub_key)
        assert payload is not None
        assert (base_dir / rec["source_file"]).exists(), f"Missing source_file: {rec['source_file']}"
    print(f"  [✔ Verified] All {len(manifest_records)} bundles passed Ed25519 + AES-256-GCM + source existence checks.")


if __name__ == "__main__":
    compile_all()
