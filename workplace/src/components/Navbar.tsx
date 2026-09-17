import React, { useState } from "react";

export interface NavItem {
  label: string;
  href: string;
  badge?: string;
}

const NAV_ITEMS: NavItem[] = [
  { label: "Architecture", href: "/#architecture" },
  { label: "Capabilities", href: "/#capabilities" },
  { label: "AST Pruning Demo", href: "/#demo", badge: "Live" },
  { label: "ROI Calculator", href: "/#roi" },
  { label: "Case Studies", href: "/case-studies" },
  { label: "Docs", href: "/docs" },
];

export const Navbar: React.FC = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [theme, setTheme] = useState<"dark" | "system">("dark");

  return (
    <nav
      className="sticky top-0 z-50 w-full glass-panel border-b border-percipience-dark-600/50"
      role="navigation"
      aria-label="Main Navigation"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Brand Logo */}
          <div className="flex items-center space-x-3">
            <a
              href="/"
              className="flex items-center space-x-2 focus-visible:ring-2 focus-visible:ring-cyan-glow rounded-md"
              aria-label="Percipience Home"
            >
              <div className="w-9 h-9 rounded-lg bg-cyan-glow/10 border border-cyan-glow/30 flex items-center justify-center">
                <span className="text-cyan-glow font-mono font-bold text-lg">⚡</span>
              </div>
              <div className="flex flex-col">
                <span className="font-bold text-lg tracking-tight gradient-text-cyan">
                  Percipience
                </span>
                <span className="text-[10px] text-muted-foreground uppercase tracking-widest font-mono">
                  Context OS
                </span>
              </div>
            </a>

            {/* Live Merkle Status Badge */}
            <div className="hidden md:flex items-center px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping mr-1.5" />
              <span>Merkle Chain Active</span>
            </div>
          </div>

          {/* Desktop Nav Links */}
          <div className="hidden md:flex items-center space-x-6">
            {NAV_ITEMS.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="text-sm font-medium text-slate-300 hover:text-cyan-glow transition-colors duration-150 flex items-center space-x-1.5"
              >
                <span>{item.label}</span>
                {item.badge && (
                  <span className="text-[10px] uppercase font-mono px-1.5 py-0.2 rounded bg-cyan-glow/20 text-cyan-glow font-semibold">
                    {item.badge}
                  </span>
                )}
              </a>
            ))}
          </div>

          {/* Action CTAs */}
          <div className="hidden md:flex items-center space-x-3">
            <button
              onClick={() => setTheme(theme === "dark" ? "system" : "dark")}
              className="p-2 text-slate-400 hover:text-slate-200 rounded-lg hover:bg-slate-800/60 focus-visible:ring-2"
              aria-label="Toggle theme"
            >
              <span className="text-sm">🌓</span>
            </button>
            <a
              href="/login"
              className="text-sm font-medium text-slate-300 hover:text-white px-3 py-1.5 rounded-lg hover:bg-slate-800/60 transition"
            >
              Sign In
            </a>
            <a
              href="/onboarding"
              className="text-sm font-medium bg-cyan-glow text-slate-950 px-4 py-1.5 rounded-lg font-semibold hover:bg-cyan-glow/90 shadow-cyan-glow transition"
            >
              Start Free Trial
            </a>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center space-x-2">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 focus-visible:ring-2 focus-visible:ring-cyan-glow"
              aria-expanded={mobileMenuOpen}
              aria-label="Toggle main menu"
            >
              <span className="text-xl">{mobileMenuOpen ? "✕" : "☰"}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden glass-panel border-b border-slate-700 px-4 pt-2 pb-4 space-y-2">
          {NAV_ITEMS.map((item) => (
            <a
              key={item.href}
              href={item.href}
              onClick={() => setMobileMenuOpen(false)}
              className="block px-3 py-2 rounded-md text-base font-medium text-slate-300 hover:text-cyan-glow hover:bg-slate-800/80"
            >
              {item.label}
            </a>
          ))}
          <div className="pt-3 border-t border-slate-700 flex flex-col space-y-2">
            <a
              href="/login"
              className="text-center py-2 text-sm font-medium text-slate-300 rounded-md bg-slate-800"
            >
              Sign In
            </a>
            <a
              href="/onboarding"
              className="text-center py-2 text-sm font-semibold text-slate-950 bg-cyan-glow rounded-md shadow-cyan-glow"
            >
              Start Free Trial
            </a>
          </div>
        </div>
      )}
    </nav>
  );
};
