# Append-Only Poisoning Incident Store

Individual, immutable poisoning incident files are recorded here as:
`<incident_id>.md`

This prevents concurrent subagent worktrees from contending on a single file lock. The legacy `user/hitl/poisoning_quarantine.md` serves as a read-only rolled-up view.
