import React from "react";

export const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-950 border-t border-slate-800/80 text-slate-400 text-xs" role="contentinfo">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-8 mb-12">
          {/* Col 1: Brand & Identity */}
          <div className="col-span-2">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 rounded-lg bg-cyan-glow/10 border border-cyan-glow/30 flex items-center justify-center">
                <span className="text-cyan-glow font-mono font-bold">⚡</span>
              </div>
              <span className="text-base font-bold text-white tracking-tight">
                Neutron Binary Percipience
              </span>
            </div>
            <p className="mt-3 text-xs text-slate-400 max-w-sm leading-relaxed">
              The foundational Context Engineering Operating System & Autonomous CI/CD Gatekeeper. Reducing token overhead, enforcing Merkle state ledgers, and securing enterprise agent workflows.
            </p>
            <div className="mt-4 flex items-center space-x-3">
              <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-[10px] text-slate-300 font-mono">
                SOC2 Type II Ready
              </span>
              <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-[10px] text-slate-300 font-mono">
                ISO 27001
              </span>
              <span className="px-2 py-0.5 rounded bg-slate-800 border border-slate-700 text-[10px] text-slate-300 font-mono">
                WCAG 2.1 AA
              </span>
            </div>
          </div>

          {/* Col 2: Platform */}
          <div>
            <h4 className="text-white font-semibold mb-3">Platform</h4>
            <ul className="space-y-2">
              <li><a href="/#capabilities" className="hover:text-cyan-glow transition">AST Token Pruner</a></li>
              <li><a href="/#architecture" className="hover:text-cyan-glow transition">Merkle State Ledger</a></li>
              <li><a href="/#capabilities" className="hover:text-cyan-glow transition">Surgical Rollback</a></li>
              <li><a href="/#capabilities" className="hover:text-cyan-glow transition">Sealed Enclaves (.nbpack)</a></li>
              <li><a href="/#capabilities" className="hover:text-cyan-glow transition">Git Worktrees Engine</a></li>
            </ul>
          </div>

          {/* Col 3: Resources & Docs */}
          <div>
            <h4 className="text-white font-semibold mb-3">Resources</h4>
            <ul className="space-y-2">
              <li><a href="/docs/guides/quickstart" className="hover:text-cyan-glow transition">Quickstart Guide</a></li>
              <li><a href="/docs/architecture" className="hover:text-cyan-glow transition">Living Architecture</a></li>
              <li><a href="/case-studies" className="hover:text-cyan-glow transition">Enterprise Case Studies</a></li>
              <li><a href="/docs/benchmarks/workflow_durability_analysis" className="hover:text-cyan-glow transition">Durability Benchmarks</a></li>
              <li><a href="/docs/reports/token_savings_whitepaper" className="hover:text-cyan-glow transition">FinOps Whitepaper</a></li>
            </ul>
          </div>

          {/* Col 4: Company & Trust */}
          <div>
            <h4 className="text-white font-semibold mb-3">Company</h4>
            <ul className="space-y-2">
              <li><a href="/about" className="hover:text-cyan-glow transition">About Neutron Binary</a></li>
              <li><a href="/security" className="hover:text-cyan-glow transition">Trust & Security</a></li>
              <li><a href="/privacy" className="hover:text-cyan-glow transition">Privacy Policy</a></li>
              <li><a href="/terms" className="hover:text-cyan-glow transition">Terms of Service</a></li>
              <li><a href="/contact" className="hover:text-cyan-glow transition">Contact & Support</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar: Copyright & Hash Status */}
        <div className="pt-8 border-t border-slate-800/60 flex flex-col sm:flex-row items-center justify-between text-slate-400 gap-4">
          <div>
            © {new Date().getFullYear()} Neutron Binary Inc. All rights reserved. Percipience™ is an enterprise trademark.
          </div>
          <div className="flex items-center space-x-4 font-mono text-[11px]">
            <span className="flex items-center space-x-1.5 text-emerald-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
              <span>Genesis Block 0 Sealed</span>
            </span>
            <span className="text-slate-400">|</span>
            <span>Ed25519 Signed</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
