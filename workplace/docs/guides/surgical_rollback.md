# Surgical Module Rollback Protocol

How to cleanly recover from context poisoning without breaking sibling micro-modules.

## The Problem with Naive Git Rollback
Standard `git reset --hard` clobbers all simultaneous work across the repository. In a multi-module system, this destroys valid commits in unaffected modules.

## Percipience Surgical Rollback
Percipience isolates and restores only the contaminated module subtree:
```bash
percipience rollback --module mod_observability_usage --target-point RP_PLAY3_BOOTSTRAP_001
```

Sibling modules (`mod_portal_marketing`, `mod_tenant_onboarding`, `mod_billing_metering`) remain completely unaffected.
Offending prompt turns and diff snippets are recorded in `user/hitl/poisoning_quarantine.md`.
