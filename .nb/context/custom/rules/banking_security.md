# Banking Domain Security Rules & Governance Guardrails

- **Rule-01 (Monetary Representation)**: All monetary amounts across services and databases must use 64-bit integer cents (avoid IEEE 754 floating point arithmetic).
- **Rule-02 (PII Masking)**: Personally Identifiable Information (SSN, credit card numbers, account numbers, tax identifiers) must be masked before entering stdout, stderr, or telemetry logs.
- **Rule-03 (mTLS Context)**: All inter-service API calls must propagate verified mTLS context headers (`X-Client-Cert-SHA256`) and Ed25519 tenant tokens.
- **Rule-04 (Zero Plaintext Secrets)**: API keys, database connection passwords, and private certificates must never be hardcoded into workplace source files.
