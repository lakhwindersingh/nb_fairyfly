# Continuous Zero-Trust Authorization & Revocation Rules

## 1. Continuous Identity Attestation
1. "Never Trust, Always Verify": No network perimeter (intra-cluster VPC, VPN, or localhost) confers automatic trust.
2. Every request MUST provide valid, cryptographically signed credentials (Ed25519 Bearer token or SPIFFE X.509 SVID).
3. Access tokens MUST have short lifespans (<= 15 minutes) and are backed by stateful refresh token families with reuse detection.

## 2. Sub-Millisecond Distributed Revocation
1. Immediate token revocation MUST evaluate against an in-memory Redis Bloom Filter / distributed fast-path cache.
2. Target revocation evaluation latency MUST be <= 200 microseconds.
3. Upon detecting a revoked `jti` (JWT ID), the request gateway immediately terminates the session with HTTP 401/403 and records an anomaly event.

## 3. Four-Eyes Multi-Signature Dual Control
1. Critical administrative and financial actions (surgical rollbacks, key rotations, WORM policy amendments) require two distinct authorized actors:
   $$\text{Actor}_{\text{initiator}} \ne \text{Actor}_{\text{approver}}$$
2. Both actors MUST sign the payload with independent cryptographic private keys.
3. All four-eyes approved transactions MUST be sealed into the Merkle DAG ledger.
