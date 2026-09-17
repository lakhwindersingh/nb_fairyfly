import React, { useState } from "react";

export interface ContactFormData {
  name: string;
  email: string;
  company: string;
  monthlyTokens: string;
  message: string;
}

export const ContactForm: React.FC = () => {
  const [formData, setFormData] = useState<ContactFormData>({
    name: "",
    email: "",
    company: "",
    monthlyTokens: "10M - 50M",
    message: "",
  });

  const [status, setStatus] = useState<"idle" | "submitting" | "success" | "error">("idle");
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = (): boolean => {
    const errs: Record<string, string> = {};
    if (!formData.name.trim()) errs.name = "Name is required.";
    if (!formData.email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errs.email = "Valid corporate email is required.";
    }
    if (!formData.company.trim()) errs.company = "Company name is required.";
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    setStatus("submitting");
    setTimeout(() => {
      setStatus("success");
    }, 800);
  };

  return (
    <section id="contact" className="py-20 relative" aria-label="Contact Sales">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="glass-panel-glow rounded-3xl p-8 sm:p-12 border border-slate-800">
          <div className="text-center mb-8">
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white">
              Schedule an Enterprise Architecture Review
            </h2>
            <p className="mt-2 text-sm text-slate-400">
              Calculate your exact token savings and deploy a dedicated PR gatekeeper sandbox.
            </p>
          </div>

          {status === "success" ? (
            <div className="text-center py-10">
              <div className="w-14 h-14 bg-emerald-500/10 border border-emerald-500/30 rounded-full flex items-center justify-center mx-auto text-emerald-400 text-2xl mb-4">
                ✓
              </div>
              <h3 className="text-xl font-bold text-white">Review Request Received</h3>
              <p className="mt-2 text-sm text-slate-400 max-w-md mx-auto">
                A Percipience Solutions Architect will reach out to{" "}
                <span className="text-cyan-glow font-medium">{formData.email}</span> within 4 business hours.
              </p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-5" noValidate>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="name" className="block text-xs font-medium text-slate-300 mb-1.5">
                    Full Name *
                  </label>
                  <input
                    id="name"
                    type="text"
                    required
                    value={formData.name}
                    onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700 text-white text-sm focus:border-cyan-glow focus:ring-1 focus:ring-cyan-glow outline-none transition"
                    placeholder="Jane Doe"
                  />
                  {errors.name && <p className="text-xs text-rose-400 mt-1">{errors.name}</p>}
                </div>

                <div>
                  <label htmlFor="email" className="block text-xs font-medium text-slate-300 mb-1.5">
                    Work Email *
                  </label>
                  <input
                    id="email"
                    type="email"
                    required
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700 text-white text-sm focus:border-cyan-glow focus:ring-1 focus:ring-cyan-glow outline-none transition"
                    placeholder="jane@enterprise.com"
                  />
                  {errors.email && <p className="text-xs text-rose-400 mt-1">{errors.email}</p>}
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="company" className="block text-xs font-medium text-slate-300 mb-1.5">
                    Company / Organization *
                  </label>
                  <input
                    id="company"
                    type="text"
                    required
                    value={formData.company}
                    onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700 text-white text-sm focus:border-cyan-glow focus:ring-1 focus:ring-cyan-glow outline-none transition"
                    placeholder="Acme Corp"
                  />
                  {errors.company && <p className="text-xs text-rose-400 mt-1">{errors.company}</p>}
                </div>

                <div>
                  <label htmlFor="tokens" className="block text-xs font-medium text-slate-300 mb-1.5">
                    Estimated Monthly Tokens
                  </label>
                  <select
                    id="tokens"
                    value={formData.monthlyTokens}
                    onChange={(e) => setFormData({ ...formData, monthlyTokens: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700 text-white text-sm focus:border-cyan-glow focus:ring-1 focus:ring-cyan-glow outline-none transition"
                  >
                    <option value="1M - 10M">1M – 10M tokens / mo</option>
                    <option value="10M - 50M">10M – 50M tokens / mo</option>
                    <option value="50M - 250M">50M – 250M tokens / mo</option>
                    <option value="250M+">250M+ tokens / mo (Enterprise Scale)</option>
                  </select>
                </div>
              </div>

              <div>
                <label htmlFor="message" className="block text-xs font-medium text-slate-300 mb-1.5">
                  Specific Requirements or Infrastructure Stack
                </label>
                <textarea
                  id="message"
                  rows={3}
                  value={formData.message}
                  onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                  className="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700 text-white text-sm focus:border-cyan-glow focus:ring-1 focus:ring-cyan-glow outline-none transition"
                  placeholder="e.g., GitHub Enterprise, Claude 3.7 Sonnet, multi-agent worktrees..."
                />
              </div>

              <button
                type="submit"
                disabled={status === "submitting"}
                className="w-full py-3 rounded-xl font-semibold text-slate-950 bg-cyan-glow hover:bg-cyan-glow/90 shadow-cyan-glow transition duration-150 disabled:opacity-50"
              >
                {status === "submitting" ? "Submitting..." : "Request Architecture Review"}
              </button>
            </form>
          )}
        </div>
      </div>
    </section>
  );
};
