import React from "react";

export interface CapabilityCard {
  id: string;
  icon: string;
  title: string;
  tagline: string;
  description: string;
  metric: string;
  metricLabel: string;
  highlightColor: string;
}

const CAPABILITIES: CapabilityCard[] = [
  {
    id: "ast-pruning",
    icon: "🌳",
    title: "Structural AST Token Pruning",
    tagline: "40–60% context reduction before model ingestion",
    description:
      "Performs AST diff extraction, comments/docstrings stripping, and dead-branch elimination across TypeScript, Python, and Go codebases.",
    metric: "47.4%",
    metricLabel: "Measured Token Savings",
    highlightColor: "text-cyan-glow border-cyan-glow/30",
  },
  {
    id: "merkle-ledger",
    icon: "⛓️",
    title: "Cryptographic Merkle State Ledger",
    tagline: "Tamper-proof audit trails for autonomous agents",
    description:
      "Every prompt turn, code change, and schema migration is atomically hashed and sealed into an immutable SHA-256 Merkle chain.",
    metric: "487+",
    metricLabel: "Verified Merkle Blocks",
    highlightColor: "text-emerald-400 border-emerald-400/30",
  },
  {
    id: "poisoning-sentinel",
    icon: "🛡️",
    title: "Context Poisoning Interception",
    tagline: "Sub-1.2s surgical rollback to clean state",
    description:
      "Detects hallucinated packages, invalid API signatures, and prompt contamination before merge, rolling back only contaminated modules.",
    metric: "1.14s",
    metricLabel: "Rollback Latency",
    highlightColor: "text-rose-400 border-rose-400/30",
  },
  {
    id: "nbpack-enclave",
    icon: "🔒",
    title: "Sealed Binary Enclaves (.nbpack)",
    tagline: "0.0% plaintext exposure of proprietary logic",
    description:
      "Compiles proprietary plans, custom prompt chains, and architecture rules into AES-256-GCM / Ed25519 sealed binary envelopes.",
    metric: "0.0%",
    metricLabel: "Plaintext Exposure",
    highlightColor: "text-indigo-400 border-indigo-400/30",
  },
  {
    id: "worktree-concurrency",
    icon: "🔀",
    title: "Ephemeral Git Worktrees",
    tagline: "Zero-contention concurrent agent collaboration",
    description:
      "Mounts isolated ephemeral worktrees for parallel agent execution with automated TTL enforcement and atomic verification merges.",
    metric: "100%",
    metricLabel: "Merge Conflict Immunity",
    highlightColor: "text-cyan-glow border-cyan-glow/30",
  },
  {
    id: "byor-adapter",
    icon: "🔌",
    title: "BYOR Multi-VCS Bridge",
    tagline: "Bring-Your-Own-Repository integration",
    description:
      "Connects GitHub, GitLab, and Bitbucket repositories with unified webhook ingestion and enterprise PR gatekeeper status checks.",
    metric: "3-Way",
    metricLabel: "VCS Platform Support",
    highlightColor: "text-emerald-400 border-emerald-400/30",
  },
  {
    id: "living-docs",
    icon: "📊",
    title: "Autonomous Living Documentation",
    tagline: "100% synchronized architecture & diagrams",
    description:
      "Automatically extracts AST topologies and generates live Mermaid C4 diagrams, sequence flows, and module catalogs on every PR.",
    metric: "7 Docs",
    metricLabel: "Self-Synchronizing Blueprints",
    highlightColor: "text-indigo-400 border-indigo-400/30",
  },
  {
    id: "rev-share-finops",
    icon: "💰",
    title: "Token Savings Rev-Share Metering",
    tagline: "15% performance fee tied to cryptographic proof",
    description:
      "Automated Stripe billing and telemetry engine that calculates gross cash saved across agent prompts and auto-invoices performance share.",
    metric: "$3.92+",
    metricLabel: "Net Savings per Session",
    highlightColor: "text-amber-400 border-amber-400/30",
  },
];

export const FeatureGrid: React.FC = () => {
  return (
    <section id="capabilities" className="py-20 bg-slate-950/40 relative" aria-label="Core Capabilities">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-xs uppercase font-mono tracking-widest text-cyan-glow font-semibold">
            Enterprise Architecture Pillars
          </h2>
          <p className="mt-2 text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Built for Autonomous AI Development at Scale
          </p>
          <p className="mt-4 text-base text-slate-400">
            A comprehensive suite of AST compression engines, tamper-proof state machines, and autonomous CI/CD verification gates.
          </p>
        </div>

        {/* 8-Card Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {CAPABILITIES.map((card) => (
            <div
              key={card.id}
              className="glass-panel rounded-2xl p-6 border border-slate-800 hover:border-slate-700 transition-all duration-200 flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-3xl p-2.5 rounded-xl bg-slate-800/80 border border-slate-700">
                    {card.icon}
                  </span>
                  <div className={`px-2.5 py-1 rounded-full border text-xs font-mono font-bold ${card.highlightColor}`}>
                    {card.metric}
                  </div>
                </div>
                <h3 className="text-lg font-bold text-white group-hover:text-cyan-glow transition-colors">
                  {card.title}
                </h3>
                <p className="text-xs font-medium text-slate-400 mt-1 mb-3">
                  {card.tagline}
                </p>
                <p className="text-xs text-slate-400 leading-relaxed">
                  {card.description}
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between text-[11px] text-slate-400">
                <span>{card.metricLabel}</span>
                <span className="text-cyan-glow font-semibold group-hover:translate-x-1 transition-transform">
                  Explore →
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
