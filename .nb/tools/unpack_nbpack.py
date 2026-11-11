#!/usr/bin/env python3
"""
Percipience Cryptographic Plan Pack Unpacker / Inspector
Verifies Ed25519 signature and decrypts AES-256-GCM .nbpack envelopes.
"""

import os
import sys
import json
import zlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

MAGIC_HEADER = b"NBPACK1"
ASSOCIATED_DATA = b"PERCIPIENCE_NBPACK_V1"

def unpack(bundle_path, output_path=None, key_dir=".nb/keys"):
    aes_key_path = os.path.join(key_dir, "enclave.key")
    pub_key_path = os.path.join(key_dir, "signing_ed25519.pub")

    if not os.path.exists(aes_key_path) or not os.path.exists(pub_key_path):
        print(f"Error: Missing keys in {key_dir}")
        sys.exit(1)

    with open(aes_key_path, "rb") as f:
        aes_key = f.read()
    with open(pub_key_path, "rb") as f:
        pub_key = serialization.load_pem_public_key(f.read())

    with open(bundle_path, "rb") as f:
        envelope = f.read()

    if not envelope.startswith(MAGIC_HEADER):
        raise ValueError("Invalid magic header: not a valid .nbpack file")

    nonce = envelope[7:19]
    signature = envelope[19:83]
    ciphertext = envelope[83:]

    # Verify Ed25519 signature
    pub_key.verify(signature, ciphertext)

    # Decrypt AES-256-GCM
    aesgcm = AESGCM(aes_key)
    decompressed = aesgcm.decrypt(nonce, ciphertext, ASSOCIATED_DATA)
    raw_json = zlib.decompress(decompressed).decode("utf-8")
    payload = json.loads(raw_json)

    print(f"[*] Verified & Decrypted: {bundle_path}")
    print(f"    Format: {payload.get('format')}")
    print(f"    Plan ID: {payload.get('plan_id')}")
    print(f"    Plan Name: {payload.get('plan_name')}")

    if output_path:
        content = payload.get("content", "")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[✔] Extracted Markdown to: {output_path}")
    else:
        print("[✔] Payload is valid and intact.")

    return payload

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path_to_nbpack> [output_markdown_path]")
        sys.exit(1)

    bundle = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    unpack(bundle, out)
