# Append-Only Flaky Test Registry

Individual, immutable flaky test incident files are recorded here as:
`<test_id>.yaml`

This prevents concurrent subagent worktrees from contending on a single file lock. The legacy `user/hitl/flaky_quarantine.yaml` serves as a read-only rolled-up view.
