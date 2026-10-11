# 📐 6-Vector Semantic Parity Audit Checklist & Gatekeeper Specification

## Overview

The Percipience Semantic Parity Gate enforces that any plan marked with `maturity.stage = COMPLETED` or `production_ready = true` must satisfy a composite 6-vector score $S_{SP} \ge 0.950$.

---

## 1. Mathematical Parity Formula

$$S_{SP} = \sum_{i=1}^{6} w_i \cdot V_i$$

Where:
- $\sum_{i=1}^{6} w_i = 1.0$
- $V_i \in [0.0, 1.0]$

| Vector Index | Dimension | Symbol | Weight ($w_i$) | Description |
| :---: | :--- | :---: | :---: | :--- |
| $V_1$ | **AST Parity** | $V_{AST}$ | 0.20 | Preserves syntax trees, symbol references, and language AST constructs without semantic loss. |
| $V_2$ | **Contract Parity** | $V_{CTR}$ | 0.20 | Strict adherence to JSON-Schema / Pydantic stage input/output payload contracts. |
| $V_3$ | **Behavior Parity** | $V_{BEH}$ | 0.20 | Runtime state transitions, idempotency assertions, and unit/integration test assertions pass 100%. |
| $V_4$ | **Handover Parity** | $V_{HND}$ | 0.15 | Multi-agent task handoff idempotency, DAG context preservation, and state ledger checkpointing. |
| $V_5$ | **Documentation Parity** | $V_{DOC}$ | 0.15 | Synchronized consistency between `concise.md`, `detailed.md`, and code implementation comments/docstrings. |
| $V_6$ | **Supply Chain Parity** | $V_{SUP}$ | 0.10 | Cryptographic SHA-256 hashes, license boundaries, and packaging dependency security integrity. |

---

## 2. Gatekeeper Thresholds

- **$S_{SP} \ge 0.950$**: `PASSED` - Certified for production runtime deployment and automated merging.
- **$0.900 \le S_{SP} < 0.950$**: `WARNING` - Non-blocking dev branch execution; remediation required before release.
- **$S_{SP} < 0.900$**: `BLOCKED` - Strict gate failure; PR gatekeeper rejects autonomous deployment.

---

## 3. Audit Scoring Protocol

Before marking any plan as `COMPLETED`:
1. Execute `bash .nb/plan/scripts/validate.sh` to ensure DAG acyclicity and hash integrity.
2. Verify that `pytest workplace/tests/` passes with 100% success rate.
3. Verify that `file_versions` in `MANIFEST.yaml` matches the SHA-256 hashes of `concise.md`, `detailed.md`, and `README.md`.
4. Run `python3 .nb/plan/scripts/generate_capability_index.py` to regenerate the matrix.
