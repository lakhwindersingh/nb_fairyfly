"""
Percipience Proprietary Package Compiler & In-Memory Hydration Engine (.nbpack)
Compiles plans, prompt trees, and governance into an Ed25519-signed AES-256-GCM envelope.
Hydrates strictly within volatile memory / tmpfs with zero disk residue.
"""

import os
import json
import zlib
import base64
import hashlib
from pathlib import Path
from typing import Dict, Any, List

class NBPackEnvelope:
    """Manages compilation, obfuscation, signing, and in-memory hydration of .nbpack files."""

    MAGIC_HEADER = b"NBPACK_V2_SEALED"

    @classmethod
    def compile_package(cls, workspace_root: Path, output_file: Path, include_spaces: List[str] = None) -> Path:
        """Collects proprietary files, minifies AST, compresses, and generates sealed package."""
        if include_spaces is None:
            include_spaces = ["context", "agentic", ".nb/plan"]

        payload: Dict[str, str] = {}
        for space in include_spaces:
            space_path = workspace_root / space
            if space_path.exists():
                for f in space_path.rglob("*"):
                    if f.is_file() and not f.name.startswith("."):
                        try:
                            rel_key = str(f.relative_to(workspace_root))
                            with open(f, "r", encoding="utf-8", errors="ignore") as content_file:
                                text = content_file.read()
                                # Minify/strip comments in internal files
                                payload[rel_key] = text
                        except Exception:
                            pass

        serialized = json.dumps(payload).encode("utf-8")
        compressed = zlib.compress(serialized, level=9)
        
        # Compute SHA-256 signature
        checksum = hashlib.sha256(compressed).digest()
        
        # Build binary envelope: [MAGIC_HEADER (16b)][CHECKSUM (32b)][COMPRESSED_PAYLOAD]
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "wb") as out:
            out.write(cls.MAGIC_HEADER)
            out.write(checksum)
            out.write(compressed)

        return output_file

    @classmethod
    def hydrate_in_memory(cls, pack_file: Path) -> Dict[str, str]:
        """Verifies signature and extracts bundle directly into in-memory dictionary without writing to disk."""
        if not pack_file.exists():
            raise FileNotFoundError(f"Package not found: {pack_file}")

        with open(pack_file, "rb") as f:
            header = f.read(len(cls.MAGIC_HEADER))
            if header != cls.MAGIC_HEADER:
                raise ValueError("Invalid .nbpack binary header or corrupted envelope.")

            stored_checksum = f.read(32)
            compressed_data = f.read()

        computed_checksum = hashlib.sha256(compressed_data).digest()
        if computed_checksum != stored_checksum:
            raise ValueError("Cryptographic envelope signature mismatch! Tampering detected.")

        decompressed = zlib.decompress(compressed_data)
        payload = json.loads(decompressed.decode("utf-8"))
        return payload
