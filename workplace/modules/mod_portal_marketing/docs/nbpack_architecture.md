# Proprietary Plan Obfuscation & Enclave Architecture (`.nbpack`)

Protect enterprise intellectual property and proprietary prompt suites when distributing agentic systems.

## The 5 Layers of Defense
1. **AST Minification**: Strips whitespace, human comments, and obfuscates identifier tokens.
2. **Bytecode Serialization**: Encodes prompt templates and workflows into serialized binary protocol buffers.
3. **AES-256-GCM Envelope Encryption**: Sealed binary container using HKDF keys derived from tenant API keys.
4. **Ed25519 Cryptographic Signatures**: Prevents tampering and unauthenticated binary modifications.
5. **Zero-Knowledge Runtime RAM Hydration**: Decrypts directly into `/dev/shm` / tmpfs memory with zero plaintext written to disk.
