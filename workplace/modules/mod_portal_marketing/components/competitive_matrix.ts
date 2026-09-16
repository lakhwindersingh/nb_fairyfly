/**
 * Percipience Competitive Differentiation Matrix Component Data & Logic
 */

export interface CompetitorComparisonRow {
  dimension: string;
  category: "execution" | "governance" | "cost" | "security";
  rawCursorClaudeCode: string;
  langChainLangSmith: string;
  arizePhoenixArmor: string;
  percipience: string;
  impactVerdict: string;
}

export const COMPETITIVE_MATRIX_DATA: CompetitorComparisonRow[] = [
  {
    dimension: "Surgical Module Rollback",
    category: "execution",
    rawCursorClaudeCode: "❌ Full git reset required (destroys concurrent work)",
    langChainLangSmith: "❌ No filesystem or git rollback capabilities",
    arizePhoenixArmor: "❌ None (observability and logging only)",
    percipience: "✅ Rewinds culprit micro-module to RP_k, sparing 100% of siblings",
    impactVerdict: "Zero data loss during agent hallucinations in multi-module codebases"
  },
  {
    dimension: "Git Worktree Agent Isolation",
    category: "execution",
    rawCursorClaudeCode: "❌ Dirty working tree collisions during simultaneous runs",
    langChainLangSmith: "❌ None (relies on single environment or container)",
    arizePhoenixArmor: "❌ None",
    percipience: "✅ Dedicated ephemeral worktree per subagent with TTL auto-cleanup",
    impactVerdict: "Enables 20+ autonomous agents to write code concurrently without git locks"
  },
  {
    dimension: "Cryptographic Merkle State Machine",
    category: "governance",
    rawCursorClaudeCode: "❌ None (standard commit logs only)",
    langChainLangSmith: "⚠️ Proprietary centralized SaaS trace logs",
    arizePhoenixArmor: "❌ None",
    percipience: "✅ Tamper-evident SHA-256 state DAG in context_ledger.yaml & WORM storage",
    impactVerdict: "Non-repudiable audit trails for SOC 2 Type II, HIPAA, and EU AI Act compliance"
  },
  {
    dimension: "Structural AST Context Pruning",
    category: "cost",
    rawCursorClaudeCode: "⚠️ Rudimentary file grep and basic truncation",
    langChainLangSmith: "❌ None (passes full text or naive chunks)",
    arizePhoenixArmor: "❌ None",
    percipience: "✅ Rust/Tree-Sitter strips function bodies; preserves interfaces & docstrings",
    impactVerdict: "50% to 70% reduction in Claude/OpenAI context tokens (<120ms parsing)"
  },
  {
    dimension: "Cross-Module Contract Gatekeeper",
    category: "governance",
    rawCursorClaudeCode: "❌ Unchecked code generation leading to API schema drift",
    langChainLangSmith: "❌ None",
    arizePhoenixArmor: "❌ None",
    percipience: "✅ Pre-commit verification against formal YAML/Protobuf contracts",
    impactVerdict: "Prevents breaking API alterations before code enters staging or main"
  },
  {
    dimension: "Proprietary IP Obfuscation (.nbpack)",
    category: "security",
    rawCursorClaudeCode: "❌ Exposes raw system prompts & architecture in plaintext",
    langChainLangSmith: "❌ Plaintext YAML and JSON configuration files",
    arizePhoenixArmor: "❌ None",
    percipience: "✅ AES-256-GCM encrypted, Ed25519-signed envelope with RAM tmpfs hydration",
    impactVerdict: "Zero proprietary prompt or context leakage on client disk or public repos"
  },
  {
    dimension: "Bring Your Own Repository (BYOR)",
    category: "execution",
    rawCursorClaudeCode: "⚠️ Requires GitHub.com or local desktop app",
    langChainLangSmith: "⚠️ Hosted SaaS cloud only",
    arizePhoenixArmor: "⚠️ Hosted SaaS cloud only",
    percipience: "✅ Native support for self-hosted GitLab, GHES, Bitbucket DC with custom CA certs",
    impactVerdict: "Complies with strict internal corporate firewall & private VPC policies"
  },
  {
    dimension: "Token Savings Rev-Share Performance Model",
    category: "cost",
    rawCursorClaudeCode: "❌ Flat seat licenses ($20/user/mo)",
    langChainLangSmith: "❌ Per-trace event billing ($0.005/trace)",
    arizePhoenixArmor: "❌ Per-event log ingestion pricing",
    percipience: "✅ 15% of verified token savings; aligned directly with customer cost reduction",
    impactVerdict: "Percipience pays for itself: 80%+ net cash-positive ROI for engineering teams"
  }
,
  {
    dimension: "Model-Agnostic Cognitive Tiering Router",
    category: "cost",
    rawCursorClaudeCode: "❌ Single expensive model for all turns ($3 to $15/MTok)",
    langChainLangSmith: "⚠️ Manual route chains; no dynamic AST complexity detection",
    arizePhoenixArmor: "❌ None",
    percipience: "✅ Dynamic Tier A vs Tier B (Claude 3.5 Haiku / Flash) yielding 90% cost drop",
    impactVerdict: "Cuts subagent operational costs by 78% without degradation of reasoning"
  },
  {
    dimension: "Supply-Chain CVE & Wire Contract Gate",
    category: "security",
    rawCursorClaudeCode: "❌ No contract validation or AST import CVE interception",
    langChainLangSmith: "❌ None",
    arizePhoenixArmor: "⚠️ Prompt injection checks only; zero AST wire contract gate",
    percipience: "✅ Deep JSON Schema Draft-07 validation & AST package import vulnerability sentinel",
    impactVerdict: "Guarantees 100% backward compatibility & zero malicious package hallucinations"
  },
  {
    dimension: "Flaky Test Quarantine & Auto-Eviction",
    category: "execution",
    rawCursorClaudeCode: "❌ Flaky tests block developer PRs or force manual skips",
    langChainLangSmith: "❌ None",
    arizePhoenixArmor: "❌ None",
    percipience: "✅ Multi-run statistical detection & non-blocking quarantine in flaky_quarantine.yaml",
    impactVerdict: "Eliminates false-positive CI failures while tracking flaky test resolution"
  },
  {
    dimension: "Rolling Merkle Epoch Archiving",
    category: "governance",
    rawCursorClaudeCode: "❌ None",
    langChainLangSmith: "❌ Centralized database queries degrade at scale",
    arizePhoenixArmor: "❌ None",
    percipience: "✅ O(1) rolling active window with historical JSON archives in context/ledger/archive/",
    impactVerdict: "Constant-time cryptographic ledger verification even across 10,000+ blocks"
  }
];
