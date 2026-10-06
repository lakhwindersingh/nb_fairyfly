/**
 * Detailed Percipience Capabilities Catalog Data Model
 */

export interface SystemCapability {
  id: string;
  title: string;
  tagline: string;
  badge: string;
  description: string;
  technicalDetails: string[];
  slaMetric: string;
  codeSnippet: string;
}

export const CAPABILITIES_CATALOG: SystemCapability[] = [
  {
    id: "cap_worktree",
    title: "Ephemeral Git Worktree Subagent Isolation",
    tagline: "Concurrent Multi-Agent Software Development Without Workspace Collisions",
    badge: "Concurrency Engine",
    description: "Assigns each active coding subagent (Claude Code, Cursor, custom agents) a dedicated ephemeral git worktree linked to a pre-warmed gVisor microVM sandbox. Prevents file overwrites, uncommitted dirty states, and branch locking.",
    technicalDetails: [
      "Dynamic worktree allocation under .nb/workspaces/wt_{tenant}_{agent_id}",
      "Time-bound Redis lease TTLs with automatic teardown and branch pruning",
      "Automated canary merge verification before syncing into target branch"
    ],
    slaMetric: "p50 allocation < 180ms | 0% file race conditions",
    codeSnippet: "percipience worktree acquire --agent agent_dev_04 --ttl 3600"
  },
  {
    id: "cap_ast_compression",
    title: "Structural AST Token Optimization & Compression",
    tagline: "50%–70% Context Token Reduction via Tree-Sitter Body Stripping",
    badge: "Cost Reduction",
    description: "Parses Python, TypeScript, Go, and Rust source code into Abstract Syntax Trees. Strips dense internal function bodies while preserving exported signatures, interfaces, type contracts, and semantic docstrings before routing to inference models.",
    technicalDetails: [
      "Rust-compiled Tree-Sitter daemon with sub-120ms parsing throughput",
      "Prompt cache alignment guaranteeing identical prefixes for 90% Anthropic/OpenAI discounts",
      "Enforces unified diff patches saving 80%+ output tokens on 500-line files"
    ],
    slaMetric: "p50 pruning < 85ms | 58.4% average context token reduction",
    codeSnippet: "def calculate_risk(...) -> float:\n    \"\"\"Calculates portfolio value-at-risk.\"\"\"\n    ..."
  },
  {
    id: "cap_merkle_state",
    title: "Cryptographic Merkle State Machine (ledger_chain)",
    tagline: "Tamper-Evident SHA-256 State DAG for Non-Repudiable Audit Trails",
    badge: "Governance & Audit",
    description: "Every state transition, test verification, and PR gate calculates a cryptographic SHA-256 Merkle block. Chains MVS inputs, cross-module contracts, diffs, and execution logs into an immutable ledger in context/ledger/context_ledger.yaml and cloud WORM storage.",
    technicalDetails: [
      "Formula: Block Hash = SHA256(Block ID + Prev Hash + Merkle Root + Git SHA + Timestamp)",
      "Emits automated verifiable audit proof bundles for SOC 2 Type II, HIPAA, and EU AI Act",
      "Dual-ledger architecture: private master ledger + sanitized public projection"
    ],
    slaMetric: "p50 sealing < 35ms | 100% cryptographic continuity",
    codeSnippet: "percipience audit --enforce-merkle-chain --min-maturity 0.85"
  },
  {
    id: "cap_poisoning_rollback",
    title: "Context Poisoning Defense & Surgical Rollback",
    tagline: "Pinpoint Module Rollback Without Destructive Global Git Resets",
    badge: "Resilience",
    description: "An independent verifier subagent monitors AST diffs for hallucinated dependencies, API contract drift, and security leaks. If poisoning is detected, Percipience halts the turn, logs the culprit to poisoning_quarantine.md, and rolls back only the contaminated micro-module to recovery point RP_k.",
    technicalDetails: [
      "Automated quarantine ledger isolation at user/hitl/poisoning_quarantine.md",
      "Poly-module subtree rewind: resets mod_payment while sparing mod_marketing and mod_billing",
      "Diagnostic re-prompting with isolated failure contexts for self-healing"
    ],
    slaMetric: "Surgical rollback < 1.2s | Zero sibling module disruption",
    codeSnippet: "percipience rollback --module mod_observability_usage --target-point RP_PLAY3_BOOTSTRAP_001"
  },
  {
    id: "cap_nbpack",
    title: "Proprietary IP Packaging & RAM Enclave Sealing (.nbpack)",
    tagline: "Zero Plaintext Leakage of Context Engineering Plans and Metaprompts",
    badge: "IP Protection",
    description: "Compiles proprietary plans, prompt suites, and governance schemas into an Ed25519-signed AES-256-GCM binary envelope. Hydrates strictly within volatile memory (/dev/shm or tmpfs) inside client environments, leaving zero plaintext on physical disk.",
    technicalDetails: [
      "AST minification and identifier mangling of internal agent metaprompts",
      "Envelope key derivation using HKDF bound to tenant KMS and machine fingerprints",
      "In-memory stream hydration verifying Ed25519 digital signature before mounting"
    ],
    slaMetric: "Zero physical disk residue | 100% anti-exfiltration defense",
    codeSnippet: "percipience pack --include-spaces context,agentic --output parent.nbpack --obfuscate --sign"
  },
  {
    id: "cap_hybrid_coexistence",
    title: "Extensible Hybrid Context & Custom Agent Coexistence",
    tagline: "Enterprise Extensibility Layered on Immutable Platform Invariants",
    badge: "Extensibility",
    description: "Allows enterprise teams to define proprietary business logic, custom agents, and organization-specific API schemas in unencrypted workspace directories without modifying or compromising sealed core platform IP.",
    technicalDetails: [
      "3-tier context cascade: Platform Invariants (Tier 1) -> Global Rules (Tier 2) -> Domain Schemas (Tier 3)",
      "Declarative YAML agent authoring with custom system prompts and tool bindings",
      "Hybrid Merkle state hashing covering both sealed enclave and customer extensions"
    ],
    slaMetric: "100% schema validation pass | Deterministic precedence hierarchy",
    codeSnippet: "percipience validate --layered"
  },
  {
    id: "cap_byor",
    title: "Bring Your Own Repository (BYOR) Multi-VCS Integration",
    tagline: "Native Connectivity for Self-Hosted GitLab, GHES & Bitbucket Data Center",
    badge: "Enterprise VCS",
    description: "Integrates directly with on-premise and self-hosted Git appliances located behind corporate firewalls, VPNs, or private cloud VPCs. Supports SSH deploy keys, corporate CA root certificates, and universal bidirectional webhook status checks.",
    technicalDetails: [
      "Zero-Trust credential vault with dynamic runtime injection and memory wiping",
      "Custom corporate CA bundle support for secure internal TLS verification",
      "Universal status check egress for GitLab MRs, Bitbucket PRs, and GitHub Checks"
    ],
    slaMetric: "Universal VCS support | Zero public exposure required",
    codeSnippet: "percipience repo connect --url git@gitlab.internal.bank.com:core.git --auth-type ssh_key"
  },
  {
    id: "cap_infra_bridge",
    title: "Shared Infrastructure Bridge & Zero-Downtime Decoupling",
    tagline: "Smooth Transition from $255/mo Shared Co-Location to Dedicated Enterprise VPCs",
    badge: "Cloud Architecture",
    description: "Abstracts databases, distributed caches, and object vaults behind IInfraBridge. Enables low-cost launch on shared Aurora PostgreSQL RLS ($255/mo OpEx) and instant zero-code-change decoupling to dedicated customer VPC endpoints at enterprise scale.",
    technicalDetails: [
      "Phase 1: PostgreSQL Row-Level Security tenant_id pooling + Redis namespace partitioning",
      "Phase 2: Seamless migration to dedicated client RDS, isolated Redis clusters, and WORM vaults",
      "Uniform API contracts guarantee caller modules require zero code refactoring during decoupling"
    ],
    slaMetric: "Zero downtime infrastructure switching | 95%+ gross margins",
    codeSnippet: "const db = await infraBridge.getDatabaseConnection(tenantId);"
  }
,
  {
    id: "cap_reliability_pid_atomic",
    title: "Enterprise Reliability: Atomic Disk Serialization & POSIX PID Probing",
    tagline: "Zero Ledger Corruption & Automated Stale Worktree Lease Pruning",
    badge: "Reliability Hardening",
    description: "Replaces non-atomic file writes with tempfile fsync and atomic os.replace across Merkle and FinOps ledgers. Probes owning process IDs via os.kill(pid, 0) to automatically evict dead agent leases and prune orphaned directories via git worktree remove --force.",
    technicalDetails: [
      "Atomic disk swaps prevent 0-byte truncated files during unexpected process termination",
      "Active POSIX PID probing reclaims orphaned subagent leases without operator intervention",
      "Deep JSON Schema Draft-07 runtime wire contract validation on all inter-module RPC payloads"
    ],
    slaMetric: "Zero corrupted ledgers | 100% dead lease eviction in < 15ms",
    codeSnippet: "is_pid_alive(pid) -> False -> WorktreeEngine.release_lease(agent_id, force=True)"
  },
  {
    id: "cap_scalability_ast_caching_epochs",
    title: "Scalability Architecture: Content-Addressable AST Caching & Epoch Archiving",
    tagline: "Sub-Millisecond Syntax Retrieval & O(1) Constant-Time Merkle Sealing",
    badge: "Scalability Engine",
    description: "Computes SHA-256 content hashes of source code to cache stripped AST skeletons across in-memory and disk caches (.scratch/ast_cache/). Automatically checkpoints historical Merkle blocks into immutable JSON epoch archives (.nb/context/ledger/archive/), bounding active ledger height.",
    technicalDetails: [
      "Content-addressable caching eliminates >85% of redundant AST parsing overhead (<0.1ms hits)",
      "Rolling Merkle epoch checkpointing preserves constant O(1) read/write ledger speed",
      "Full cryptographic chain verification seamlessly traverses both active window and archives"
    ],
    slaMetric: "< 0.1ms AST cache retrieval | O(1) ledger memory footprint across 10,000+ blocks",
    codeSnippet: "MerkleEngine.checkpoint_epoch(workspace_root, epoch_size=50)"
  },
  {
    id: "cap_cognitive_router",
    title: "Model-Agnostic Cognitive Tiering Router",
    tagline: "Dynamic Tier A vs. Tier B Dispatch Delivering 90% Subagent Cost Arbitrage",
    badge: "Cognitive FinOps",
    description: "Analyzes incoming task prompt complexity, file paths, and AST diffs to route routine tasks to Tier B (Claude 3.5 Haiku / Gemini Flash / GPT-4o-mini) and high-complexity reasoning to Tier A (Claude 3.7 Sonnet / Gemini Pro / GPT-4o).",
    technicalDetails: [
      "Automated heuristic scoring of task requirements, contract mutations, and security risks",
      "Captures a 90% per-token cost discount on 78% of autonomous subagent CI/CD turns",
      "Model-agnostic configuration adhering to model_tiering_policy in workspace configuration"
    ],
    slaMetric: "Sub-5ms cognitive routing latency | 90% cost drop on routine turns",
    codeSnippet: "CognitiveRouter.dispatch(prompt, module_scope, complexity_hint) -> 'tier_b'"
  },
  {
    id: "cap_autonomous_cicd_specialists",
    title: "Autonomous CI/CD Specialist Agent Fleet & 6-Stage Gatekeeper",
    tagline: "Plug-and-Play Specialist Agents for Flaky Tests, Wire Contracts, CVEs & Doc Drift",
    badge: "Autonomous CI/CD",
    description: "Extensible fleet of specialized autonomous agent plugins with declarative YAML manifests, dedicated sandboxes, and recovery policies. Integrated into a 6-stage PR verification gatekeeper protecting master branches from regression.",
    technicalDetails: [
      "agent_flaky_test_detector: Multi-run stability analysis & non-blocking flaky quarantine",
      "agent_contract_compatibility_checker: Semantic wire contract diffing & SemVer enforcement",
      "agent_dependency_cve_sentinel: Supply-chain AST import auditing & restrictive license detection",
      "agent_doc_drift_synchronizer: Synchronizes architectural blueprints with live AST symbol exports"
    ],
    slaMetric: "17/17 automated tests passing in ~6s | Zero false-positive PR blocks",
    codeSnippet: "./bin/percipience gate  # Executes complete 6-stage verification gate"
  }
,
  {
    id: "cap_context_gateway_inflight",
    title: "Option 1: Context Gateway & In-Flight Prompt Injection",
    tagline: "Zero-Client-Exposure Execution of Proprietary .nbpack Blueprints",
    badge: "IP Isolation & Enclave",
    description: "Proprietary architecture plans, .nbpack bundles, and KMS decryption keys reside strictly inside the server-side Context Gateway RAM. Untrusted local client agents query POST /v1/chat/completions; the gateway injects plan invariants in-flight into the LLM system prompt and returns only sanitized code patches, ensuring 0% plan text leakage on client machines.",
    technicalDetails: [
      "Drop-in OpenAI/Claude compatible completions endpoint (POST /v1/chat/completions)",
      "Zero client-side plan or key residue: decrypted plans never touch client RAM or storage",
      "Dynamic in-flight prompt injection of hidden plan invariants, wire contracts, and rules",
      "Automated sanitization filters strip internal plan markers, returning pure code diffs"
    ],
    slaMetric: "0.0% Client Plan Exposure | +22.4ms p50 gateway latency overhead",
    codeSnippet: "curl -X POST http://localhost:3000/v1/chat/completions -d '{\"plan_id\": \"plan_iot_mobile\"}'"
  },
  {
    id: "cap_dynamic_dag",
    title: "Dynamic Task DAGs & Runtime Sub-Goal Expansion",
    tagline: "Plan-and-Solve Runtime Step Graph Mutation, Blast-Radius Branching & Backtracking",
    badge: "Cognitive Topology",
    description: "Enables autonomous agents to synthesize runtime sub-goals, adapt execution paths based on AST blast radius, backtrack upon branch failures, and prevent graph deadlocks via strict O(V+E) Kahn acyclicity checks.",
    technicalDetails: [
      "Runtime step expansion bounded by recursion depth D <= 3 and total steps N <= 20",
      "Automated blast-radius branching: validate_syntax -> run_focused_tests -> check_contract_parity",
      "Backtracking rollbacks restore ephemeral worktree state and activate alternate candidate branches"
    ],
    slaMetric: "< 15ms topological re-sort | 0% cyclic execution loops",
    codeSnippet: "DynamicDAGOrchestrator.expand_subgoals(parent_id, subgoals)"
  },
  {
    id: "cap_reflexion_critic",
    title: "3-Phase Reflexion & Invariant Critic Verification Loops",
    tagline: "Zero-Disk-Write Guarantee Until 5 Invariant Pillars Pass with S >= 0.90",
    badge: "Verification Gate",
    description: "Enforces GENERATE -> CRITIQUE -> REFINE state transitions prior to filesystem mutation. The Critic evaluates Wire Contracts, Edge-Case Coverage, Type Signature Purity, Guardrail Compliance, and Token Budgets before authorizing disk writes.",
    technicalDetails: [
      "Zero-disk-write guarantee: blocks file mutation until Critic convergence score S >= 0.90",
      "Structured CritiqueEnvelope detailing defects, severity, and remediation directives",
      "Bounded iterations (N_reflect <= 2) with automated escalation to HITL on persistent divergence"
    ],
    slaMetric: "Zero unverified disk writes | 94.2% first-pass convergence",
    codeSnippet: "SelfReflectionEngine.safe_apply_filesystem_write(path, code, reflexion_result)"
  },
  {
    id: "cap_3tier_memory",
    title: "3-Tier Persistent Agent Memory Architecture",
    tagline: "Working Scratchpad, Episodic Event Stream & Long-Term Semantic Rules",
    badge: "Cognitive Memory",
    description: "Provides ephemeral session scratchpads (Working Memory), persistent historical event streams with >0.85 error-signature recall (Episodic Memory), and project architectural conventions (Semantic Memory) with cryptographic Merkle block anchoring.",
    technicalDetails: [
      "Tier 1 Working: Ephemeral session scratchpad tracking in-flight hypotheses and symbol diffs",
      "Tier 2 Episodic: Persistent JSONL event stream indexing past resolutions and verified patches",
      "Tier 3 Semantic: Conceptual architectural patterns and Quad-Space invariant catalog",
      "Memory Consolidation: Anchors working resolutions into episodic memory with Merkle block hashes"
    ],
    slaMetric: "> 0.85 episodic recall on matching error signatures | Sub-5ms concept lookup",
    codeSnippet: "AgentMemoryEngine.query_episodic_memory(query, error_signature)"
  },
  {
    id: "cap_tool_contracts",
    title: "Declarative Tool Contracts & JSON Schema Draft-07 Validation",
    tagline: "Strict Input/Output Schema Enforcement, Idempotency Caching & Timeout Deadlines",
    badge: "Agent Tooling",
    description: "Standardizes agent tools with complete JSON Schema Draft-07 contracts. Intercepts calls for pre-call argument validation and post-call return conformance, while caching idempotent tool outputs and terminating runaway executions.",
    technicalDetails: [
      "Pre-call parameter validation rejecting malformed arguments (INVALID_TOOL_ARGUMENTS)",
      "Post-call return validation ensuring conformant payloads (INVALID_TOOL_OUTPUT)",
      "Idempotency caching engine eliminating redundant compute via sha256(inputs) keys",
      "Thread pool execution deadline enforcer terminating breached calls with TOOL_TIMEOUT_EXCEEDED"
    ],
    slaMetric: "< 0.1ms cache hit latency | 100% schema conformance enforcement",
    codeSnippet: "ToolContractValidator.execute_tool(tool_name, args, handler_fn)"
  },
  {
    id: "cap_cbac_sandbox",
    title: "Capability-Based Access Control (CBAC) Sandbox Tokens",
    tagline: "HMAC-SHA256 Cryptographic Tokens, Path Boundaries & Subprocess Whitelisting",
    badge: "Zero-Trust Sandbox",
    description: "Issues cryptographically bound capability tokens specifying granular rights (CAP_FS_READ, CAP_FS_WRITE_MODULE_ONLY, CAP_EXEC_SUBPROCESS, CAP_NETWORK_EGRESS). Restricts filesystem writes to assigned worktrees and blocks dangerous shell commands.",
    technicalDetails: [
      "HMAC-SHA256 tokens bound to (agent_id, worktree_path, allowed_operations, expiry_utc)",
      "Path-bound filesystem enforcer blocking writes to .nb/core, .nb/context/rules, and directory breakout",
      "Subprocess command whitelist allowing pytest/git/python3 while blocking curl/wget/rm -rf/bash",
      "Network egress firewall permitting virtual loopback sockets while blocking unauthorized external IPs"
    ],
    slaMetric: "Sub-1ms token verification | 100% path traversal & unauthorized command interception",
    codeSnippet: "AgentCapabilityGuard.check_fs_access(token, path, operation='write')"
  }
];
