---
description: Run Percipience audit, gatekeeper, test coverage, and configuration diagnostics
---
Please perform the following actions:
1. Run `./.nb/bin/percipience config show` to inspect active platform configuration values.
2. Run `./.nb/bin/percipience audit --enforce-merkle-chain` to inspect Merkle DAG integrity and maturity scorecard.
3. Run `./.nb/bin/percipience tokens summary` to inspect token savings ledger and FinOps ROI.
4. Run `./.nb/bin/percipience test --coverage` to verify the test pyramid across all 54 platform core engines.
5. Report the platform status and any active policy invariant warnings.
