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
      "Dynamic worktree allocation under .workspaces/wt_{tenant}_{agent_id}",
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
];

export class CapabilitiesCatalogService {
  static getCatalog(): SystemCapability[] {
    return CAPABILITIES_CATALOG;
  }
}
