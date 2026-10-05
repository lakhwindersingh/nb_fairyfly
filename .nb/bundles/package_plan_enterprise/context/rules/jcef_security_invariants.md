# JCEF Security Invariants

1. **Restricted Scheme & Host Access**:
   - JCEF browser instances must restrict custom scheme handlers to local assets (`percipience://app/...`) and forbid loading arbitrary external URLs.

2. **Nonce-Based RPC Validation**:
   - Queries sent via `CefMessageRouter` must carry an ephemeral session nonce validated by the Kotlin project service before dispatching commands to the Percipience daemon.
