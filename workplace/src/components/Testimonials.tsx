import React from "react";

export interface Testimonial {
  quote: string;
  author: string;
  role: string;
  company: string;
  metric: string;
  metricLabel: string;
  avatar: string;
}

const TESTIMONIALS: Testimonial[] = [
  {
    quote:
      "Percipience shaved 48% off our monthly Anthropic token bill within 48 hours of enabling the PR gatekeeper. The AST diff optimizer is sheer engineering brilliance.",
    author: "Elena Rostova",
    role: "VP of Engineering",
    company: "FinScale Dynamics",
    metric: "$42,800 / mo",
    metricLabel: "Direct Token Savings",
    avatar: "ER",
  },
  {
    quote:
      "Context poisoning used to stall our autonomous coding agent fleet for hours. With Percipience's surgical rollback, isolated modules recover in 1.14s without halting sibling tasks.",
    author: "Marcus Vance",
    role: "Head of AI Platform",
    company: "AetherOps Enterprise",
    metric: "99.8%",
    metricLabel: "Agent Uptime",
    avatar: "MV",
  },
  {
    quote:
      "The sealed .nbpack enclave let us distribute proprietary context engineering rules to enterprise clients with 0.0% plaintext risk. It solved our IP compliance barrier.",
    author: "Devon Chen",
    role: "Chief Architect",
    company: "NeuralNexus Labs",
    metric: "0.0%",
    metricLabel: "Plaintext Exposure",
    avatar: "DC",
  },
];

export const Testimonials: React.FC = () => {
  return (
    <section className="py-20 bg-slate-950/20 relative" aria-label="Customer Testimonials">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-xs uppercase font-mono tracking-widest text-cyan-glow font-semibold">
            Proven Enterprise ROI
          </h2>
          <p className="mt-2 text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Trusted by Autonomous AI Engineering Teams
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {TESTIMONIALS.map((t, idx) => (
            <div
              key={idx}
              className="glass-panel rounded-2xl p-8 border border-slate-800 flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center space-x-1 text-cyan-glow mb-4">
                  {[...Array(5)].map((_, i) => (
                    <span key={i} className="text-sm">★</span>
                  ))}
                </div>
                <p className="text-sm text-slate-300 italic leading-relaxed">
                  "{t.quote}"
                </p>
              </div>

              <div className="mt-8 pt-6 border-t border-slate-800 flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-full bg-cyan-glow/10 border border-cyan-glow/30 flex items-center justify-center font-bold text-cyan-glow text-xs">
                    {t.avatar}
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-white">{t.author}</div>
                    <div className="text-xs text-slate-400">
                      {t.role}, {t.company}
                    </div>
                  </div>
                </div>

                <div className="text-right">
                  <div className="text-sm font-bold font-mono text-emerald-400">
                    {t.metric}
                  </div>
                  <div className="text-[10px] text-slate-400 font-mono">
                    {t.metricLabel}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
