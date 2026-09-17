/**
 * Percipience Competitive Differentiation Matrix Component Data & Logic
 * Comprehensive breakdown comparing Percipience vs generic coding assistants,
 * trace libraries, legacy observability tools, and traditional CI/CD frameworks.
 */

export interface CompetitorComparisonRow {
  dimension: string;
  category: "autonomous_cicd" | "context_finops" | "governance" | "security" | "concurrency";
  rawCursorClaudeCode: string;
  langChainLangSmith: string;
  arizePhoenixArmor: string;
  legacyCICD: string; // Jenkins / GitHub Actions / GitLab CI
  percipience: string;
  impactVerdict: string;
}

export const COMPETITIVE_MATRIX_DATA: CompetitorComparisonRow[] = [
  // -------------------------------------------------------------
  // AUTONOMOUS CI/CD DOMAIN (Exclusive to Neutron Binary Percipience)
  // -------------------------------------------------------------
  {
    dimension: "Autonomous CI/CD Triad (Sustain, Heal, Improve)",
    category: "autonomous_cicd",
    rawCursorClaudeCode: "❌ Single-turn command runner; no self-healing loops",
    langChainLangSmith: "❌ Trace visualization only; no CI/CD remediation",
    arizePhoenixArmor: "❌ Passive evaluation metrics; no execution loop",
    legacyCICD: "❌ Passive failure reporting (red build); zero automated repair",
    percipience: "✅ Full Triad: SelfSustainingEngine (GC/TTL) + AutonomousHealer + SelfImprovingEngine",
    impactVerdict: "Eliminates 90%+ of human DevOps triage by automatically repairing broken agent PRs"
  },
  {
    dimension: "Diagnostic Re-Prompting Loop (CAP-02)",
    category: "autonomous_cicd",
    rawCursorClaudeCode: "❌ Unbounded brute-force retries with bloated error logs",
    langChainLangSmith: "❌ None",
    arizePhoenixArmor: "❌ None",
    legacyCICD: "❌ None (requires developer commit push to re-test)",
    percipience: "✅ Slices raw failure trace to minimal isolated prompt envelope; bounded 3-attempt SLA",
    impactVerdict: "70%+ token drop on diagnostic loops; falls back safely to surgical rollback if unhealed"
  },
  {
    dimension: "Surgical Micro-Module Rollback (RP_k)",
    category: "autonomous_cicd",
    rawCursorClaudeCode: "❌ Destructive full git reset (destroys concurrent team work)",
    langChainLangSmith: "❌ No filesystem or git rollback capabilities",
    arizePhoenixArmor: "❌ None (observability and logging only)",
    legacyCICD: "❌ Revert commit reverses entire PR branch / merge",
    percipience: "✅ Restores culprit module to recovery point RP_k, sparing 100% of sibling micro-modules",
    impactVerdict: "Zero blast radius or data loss during agent hallucinations in multi-module codebases"
  },
  {
    dimension: "Deterministic Flaky Test Statistical Quarantine",
    category: "autonomous_cicd",
    rawCursorClaudeCode: "❌ Flaky tests fail builds unpredictably or force manual skips",
    langChainLangSmith: "❌ None",
    arizePhoenixArmor: "❌ None",
    legacyCICD: "⚠️ Manual @flaky annotations or rerun plugins (masks real bugs)",
    percipience: "✅ Automated multi-run detection & non-blocking quarantine in flaky_quarantine.yaml",
    impactVerdict: "Prevents false-alarm PR gate rejections while maintaining a rigorous remediation backlog"
  },
  {
    dimension: "Cross-Module Wire Contract & SemVer Gate",
    category: "autonomous_cicd",
    rawCursorClaudeCode: "❌ Unchecked code generation leading to subtle API drift",
    langChainLangSmith: "❌ None",
    arizePhoenixArmor: "❌ None",
    legacyCICD: "⚠️ Runtime integration test failures after deployment",
    percipience: "✅ Pre-merge JSON Schema / Protobuf contract audit; catches breaking changes & missing SemVer",
    impactVerdict: "Guarantees 100% backward compatibility across microservices before code enters staging"
  },
  {
    dimension: "Living Architecture & Mermaid Documentation Engine",
    category: "autonomous_cicd",
    rawCursorClaudeCode: "❌ Outdated markdown docs that drift immediately",
    langChainLangSmith: "❌ None",
    arizePhoenixArmor: "❌ None",
    legacyCICD: "❌ Static doc build tools without syntax linting",
    percipience: "✅ Continuous AST-to-Mermaid generator with strict bracket/syntax linting & Merkle hash validation",
    impactVerdict: "Living documentation is always 100% synchronized with codebase state without human authoring"
  },

  // -------------------------------------------------------------
  // CONTEXT ENGINEERING & MULTI-STRATEGY FINOPS DOMAIN
  // -------------------------------------------------------------
  {
    dimension: "6-Dimensional Token Compression Suite",
    category: "context_finops",
    rawCursorClaudeCode: "⚠️ Rudimentary naive file grep and line truncation",
    langChainLangSmith: "❌ Passes full prompt text or unparsed chunk strings",
    arizePhoenixArmor: "❌ None",
    legacyCICD: "❌ None",
    percipience: "✅ AST pruning + Doc condensing + Config minification + Traceback slicing + Git Diff clamping + Memory compaction",
    impactVerdict: "50% to 75% context token reduction (<120ms execution) saving $12,000+/mo for enterprise swarms"
  },
  {
    dimension: "Selective Token Optimization Toggles & Portal Control",
    category: "context_finops",
    rawCursorClaudeCode: "❌ Hardcoded black-box heuristics",
    langChainLangSmith: "❌ None",
    arizePhoenixArmor: "❌ None",
    legacyCICD: "❌ None",
    percipience: "✅ 5 intensity presets (conservative -> extreme), granular strategy checkboxes, live ROI calculator",
    impactVerdict: "Engineering teams customize optimization per microservice with real-time FinOps visibility"
  },
  {
    dimension: "Token Savings Performance Rev-Share Model",
    category: "context_finops",
    rawCursorClaudeCode: "❌ Flat seat licenses ($20/user/mo) regardless of efficiency",
    langChainLangSmith: "❌ Per-trace event billing ($0.005/trace) increasing with usage",
    arizePhoenixArmor: "❌ Ingestion volume pricing",
    legacyCICD: "❌ Per-minute runner billing (GitHub Actions minutes)",
    percipience: "✅ 15% of verified token savings; 100% aligned with customer cloud cost reduction",
    impactVerdict: "Percipience pays for itself: 80%+ net cash-positive ROI for engineering organizations"
  },
  {
    dimension: "Model-Agnostic Cognitive Tiering Router",
    category: "context_finops",
    rawCursorClaudeCode: "❌ Single expensive flagship model for all turns ($3-$15/MTok)",
    langChainLangSmith: "⚠️ Manual route chains; no dynamic AST complexity analysis",
    arizePhoenixArmor: "❌ None",
    legacyCICD: "❌ None",
    percipience: "✅ Dynamic Tier A (Claude 3.7 / Pro) vs Tier B (Haiku / Flash), dropping 90% cost on 78% of turns",
    impactVerdict: "Massively reduces agent swarm operating costs without degrading reasoning depth"
  },

  // -------------------------------------------------------------
  // CRYPTOGRAPHIC GOVERNANCE & AUDITABILITY DOMAIN
  // -------------------------------------------------------------
  {
    dimension: "Cryptographic Merkle State Machine & Epoch Archiving",
    category: "governance",
    rawCursorClaudeCode: "❌ None (standard git commit log only)",
    langChainLangSmith: "⚠️ Centralized proprietary SaaS trace logs (vendor lock-in)",
    arizePhoenixArmor: "❌ None",
    legacyCICD: "⚠️ Ephemeral CI job logs wiped after 30-90 days",
    percipience: "✅ Tamper-evident SHA-256 DAG in context_ledger.yaml with rolling JSON epoch archiving (O(1) I/O)",
    impactVerdict: "Non-repudiable audit trails for SOC 2 Type II, HIPAA, ISO 27001, and EU AI Act compliance"
  },
  {
    dimension: "SEC Rule 17a-4 / FINRA Compliant WORM Cloud Egress",
    category: "governance",
    rawCursorClaudeCode: "❌ None",
    langChainLangSmith: "❌ None",
    arizePhoenixArmor: "❌ None",
    legacyCICD: "❌ None",
    percipience: "✅ Automated egress to AWS S3 Object Lock (Compliance Mode) & GCP GCS Bucket Retention",
    impactVerdict: "Guarantees regulatory immutability against malicious tampering or insider deletion"
  },

  // -------------------------------------------------------------
  // ENTERPRISE SECURITY & IP ENCLAVE DOMAIN
  // -------------------------------------------------------------
  {
    dimension: "Option 1 Context Gateway (0.0% Client IP Exposure)",
    category: "security",
    rawCursorClaudeCode: "❌ Plaintext markdown prompts exposed to client disk & memory",
    langChainLangSmith: "⚠️ Prompts logged in centralized SaaS without KMS enclaves",
    arizePhoenixArmor: "❌ None (client holds entire system prompt)",
    legacyCICD: "❌ Plaintext repository secrets injected into runner memory",
    percipience: "✅ Server-side In-Flight Prompt Injection in KMS RAM enclave; 0.0% plan disk exposure",
    impactVerdict: "Complete zero-trust protection of proprietary architectural blueprints and prompt IP"
  },
  {
    dimension: "Supply-Chain Security & AST Dependency CVE Sentinel",
    category: "security",
    rawCursorClaudeCode: "❌ No AST-level import CVE interception during agent generation",
    langChainLangSmith: "❌ None",
    arizePhoenixArmor: "⚠️ Prompt injection filters only; zero AST package gate",
    legacyCICD: "⚠️ Post-merge vulnerability scans (Snyk/Dependabot)",
    percipience: "✅ Real-time AST import interception of malicious/typosquatted packages before file write",
    impactVerdict: "Stops supply-chain attacks and hallucinated package execution at the exact point of synthesis"
  },

  // -------------------------------------------------------------
  // CONCURRENCY & ISOLATED WORKSPACE DOMAIN
  // -------------------------------------------------------------
  {
    dimension: "Distributed Redis Redlock Worktree Leases & PID Probing",
    category: "concurrency",
    rawCursorClaudeCode: "❌ Dirty working tree collisions during simultaneous agent runs",
    langChainLangSmith: "❌ None (relies on single environment or container)",
    arizePhoenixArmor: "❌ None",
    legacyCICD: "⚠️ Heavy Docker container per job (slow startup: 30s-2m)",
    percipience: "✅ Ephemeral Git worktrees (<180ms startup) with Redis Redlock leases and dead-PID auto-eviction",
    impactVerdict: "Enables 50+ autonomous subagents to write and test code concurrently without collisions"
  },
  {
    dimension: "Bring Your Own Repository (BYOR) Behind Firewalls",
    category: "concurrency",
    rawCursorClaudeCode: "⚠️ Cloud GitHub.com or local desktop app required",
    langChainLangSmith: "⚠️ Hosted public SaaS cloud only",
    arizePhoenixArmor: "⚠️ Hosted public SaaS cloud only",
    legacyCICD: "⚠️ Self-hosted runners require heavy agent maintenance",
    percipience: "✅ Native integration for self-hosted GitLab, GHES, Bitbucket DC with custom corporate CA certs",
    impactVerdict: "Full compliance with strict corporate air-gapped VPCs and enterprise security boundaries"
  }
];

export function getMatrixByCategory(category: CompetitorComparisonRow["category"]): CompetitorComparisonRow[] {
  return COMPETITIVE_MATRIX_DATA.filter(row => row.category === category);
}
