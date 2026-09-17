import React, { useState } from "react";

export const HeroBanner: React.FC = () => {
  const [copied, setCopied] = useState(false);
  const installCmd = "npx @percipience/bootstrap --init";

  const handleCopy = () => {
    navigator.clipboard?.writeText(installCmd);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section className="relative pt-12 pb-20 overflow-hidden" aria-label="Hero Section">
      {/* Background Decorative Radial Gradients */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[300px] bg-cyan-glow/10 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute top-1/3 left-1/3 w-[400px] h-[250px] bg-indigo-500/10 blur-[100px] rounded-full pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        {/* Release / Innovation Pill */}
        <div className="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full bg-slate-800/80 border border-slate-700/80 text-xs text-slate-300 mb-6 shadow-sm">
          <span className="flex h-2 w-2 rounded-full bg-cyan-glow animate-pulse" />
          <span className="font-semibold text-cyan-glow">Play 3 Released</span>
          <span className="text-slate-500">|</span>
          <span>47.4% Structural Token Compression & CI Gatekeeper</span>
        </div>

        {/* Main Headline */}
        <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white max-w-5xl mx-auto leading-[1.1]">
          The Enterprise <span className="gradient-text-cyan">Context Engineering</span> Operating System
        </h1>

        {/* Subtitle */}
        <p className="mt-6 text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto font-normal leading-relaxed">
          Stop burning LLM tokens on comments, imports, and bloated context windows. Percipience prunes AST diffs in real time, enforces cryptographic Merkle state ledgers, intercepts context poisoning in sub-1.2s, and meters 15% revenue-share savings.
        </p>

        {/* Conversion Action Buttons */}
        <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
          <a
            href="/onboarding"
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl font-semibold text-slate-950 bg-cyan-glow hover:bg-cyan-glow/90 shadow-cyan-glow transition-all duration-200 transform hover:-translate-y-0.5"
          >
            Deploy Enterprise Gatekeeper
          </a>
          <a
            href="#demo"
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl font-semibold text-slate-200 glass-panel hover:bg-slate-800/80 border border-slate-700 transition-all duration-200 flex items-center justify-center space-x-2"
          >
            <span>Live Interactive Demo</span>
            <span className="text-cyan-glow font-mono">→</span>
          </a>
        </div>

        {/* Interactive Quickstart CLI Terminal Snippet */}
        <div className="mt-10 max-w-xl mx-auto">
          <div className="glass-panel rounded-xl p-3 border border-slate-700 flex items-center justify-between text-left font-mono text-xs sm:text-sm text-slate-300">
            <div className="flex items-center space-x-2 truncate">
              <span className="text-cyan-glow font-bold">$</span>
              <span className="text-slate-200 truncate">{installCmd}</span>
            </div>
            <button
              onClick={handleCopy}
              className="ml-3 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 font-sans border border-slate-600 transition"
              aria-label="Copy install command"
            >
              {copied ? "✓ Copied" : "Copy"}
            </button>
          </div>
        </div>

        {/* Real-Time Telemetry Stats Strip */}
        <div className="mt-14 grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto border-t border-slate-800 pt-8 text-left">
          <div className="p-3">
            <div className="text-2xl sm:text-3xl font-bold font-mono text-cyan-glow">47.4%</div>
            <div className="text-xs text-slate-400 mt-1">Average Token Reduction</div>
          </div>
          <div className="p-3">
            <div className="text-2xl sm:text-3xl font-bold font-mono text-emerald-400">&lt; 1.14s</div>
            <div className="text-xs text-slate-400 mt-1">Surgical Rollback Speed</div>
          </div>
          <div className="p-3">
            <div className="text-2xl sm:text-3xl font-bold font-mono text-indigo-400">100%</div>
            <div className="text-xs text-slate-400 mt-1">Cryptographic Merkle Continuity</div>
          </div>
          <div className="p-3">
            <div className="text-2xl sm:text-3xl font-bold font-mono text-white">0.0%</div>
            <div className="text-xs text-slate-400 mt-1">Client Plaintext IP Exposure</div>
          </div>
        </div>
      </div>
    </section>
  );
};
