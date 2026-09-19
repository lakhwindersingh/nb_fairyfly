# Percipience Developer Guide: Custom Agents, Layered Context & Workflows

This workspace operates under a **Hybrid Coexistence Architecture**:
- **Sealed Platform Engine**: Core prompt suites and state machines are loaded directly into RAM from `.nb/percipience_parent.nbpack`.
- **Your Custom Workspace**: You can add your own agents in `agentic/custom/` and domain context in `context/custom/`.

---

## 1. How to Create a Custom Agent
Create a YAML file in `agentic/custom/agents/<agent_name>.yaml`:

```yaml
agent_id: "agent_security_auditor"
name: "Enterprise Infosec & Compliance Auditor"
description: "Audits AST diffs for OWASP Top 10, hardcoded credentials, and banking compliance rules."
model: "claude-3-5-sonnet-20241022"
temperature: 0.1
role: "Infosec Auditor"

system_prompt: |
  You are the Enterprise Infosec Auditor for this repository.
  Analyze the AST symbol diffs and source modifications in workplace/ against:
  1. No unencrypted secrets or hardcoded API tokens.
  2. Strict adherence to context/custom/rules/banking_security.md.
  3. Emit structured issues with line numbers and CVE/CWE classifications.

tools:
  - name: "read_ast_diff"
    description: "Inspects pruned AST delta between base commit and PR branch"
  - name: "flag_quarantine_issue"
    description: "Appends security violation to user/hitl/poisoning_quarantine.md"

execution_constraints:
  max_token_budget_per_run: 8000
  timeout_seconds: 60
  tier: "Tier_A_Frontier"
```

---

## 2. How to Layer Your Own Context
Add your proprietary rules and schemas without modifying platform core files:

1. **Domain & Architectural Rules** (`context/custom/rules/banking_security.md`):
   ```markdown
   # Banking Domain Security Rules
   - Rule-01: All monetary amounts must use 64-bit integer cents (avoid IEEE 754 floats).
   - Rule-02: PII (SSN, credit card, account numbers) must be masked before logging.
   - Rule-03: API calls must require authenticated mTLS context headers.
   ```

2. **Custom API Contracts** (`context/custom/schemas/payment_event.yaml`):
   ```yaml
   $schema: "http://json-schema.org/draft-07/schema#"
   title: "PaymentEvent"
   type: "object"
   properties:
     transaction_id: { type: "string", format: "uuid" }
     amount_cents: { type: "integer", minimum: 1 }
     currency: { type: "string", enum: ["USD", "EUR", "GBP"] }
   required: ["transaction_id", "amount_cents", "currency"]
   ```

---

## 3. How to Wire Custom Agents into Workflow DAGs
Declare a custom workflow in `agentic/custom/workflows/enterprise_sdlc.yaml`:

```yaml
workflow_id: "wf_enterprise_pr_gate"
name: "Enterprise PR Gate with Custom Infosec Review"

steps:
  - step_id: "ast_prune"
    executor: "platform.ast_pruner"
    inputs: ["workplace/"]

  - step_id: "custom_security_audit"
    executor: "agent_security_auditor"
    depends_on: ["ast_prune"]
    inputs: ["workplace/", "context/custom/rules/banking_security.md"]
    failure_action: "quarantine_and_pause"

  - step_id: "contract_verification"
    executor: "platform.contract_verifier"
    depends_on: ["custom_security_audit"]
    inputs: ["context/custom/schemas/"]

  - step_id: "merkle_seal"
    executor: "platform.merkle_ledger"
    depends_on: ["contract_verification"]
```

---

## 4. How to Validate and Execute
```bash
# 1. Validate custom schemas and agents comply with platform invariants
percipience validate --layered

# 2. Run a dry-run execution of your custom workflow
percipience run --workflow wf_enterprise_pr_gate --dry-run
```
