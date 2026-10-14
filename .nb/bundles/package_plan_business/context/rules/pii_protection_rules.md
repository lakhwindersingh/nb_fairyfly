# PII Protection, NIST SP 800-38G FPE Encryption & Dynamic Masking Rules

## 1. Zero-Plaintext Level 4 PII Invariant
1. Raw Level 4 PII (Taxpayer ID / SSN, IBAN, bank account numbers, plaintext user email addresses) MUST NEVER be stored in plaintext.
2. Structured fields requiring format retention and indexing MUST utilize NIST SP 800-38G Format-Preserving Encryption (FF1).
3. Complex or unstructured PII payloads MUST utilize KMS envelope-encrypted token pointers (`pii_token_vault`).

## 2. Dynamic Role-Based Data Masking
1. Requester RBAC/ReBAC roles dictate field representation:
   - Public / Standard Users: Full redaction (`[REDACTED_PII]`) or partial trailing four (`***-**-1234`).
   - Email fields: Obfuscated user handle (`j***@bank.com`).
   - Compliance / Legal Auditor: Plaintext authorized only upon presenting audited business justification.
2. Decryption events MUST be recorded with Merkle leaf hashes in `pii_access_audit_log`.

## 3. Streaming Log & LLM Prompt Scrubbing
1. Real-time regex and AST filters intercept all outbound telemetry, log lines, and LLM prompt turns.
2. Any detected unmasked Level 4 PII is sanitized before network transmission.
