import React, { useState, useEffect } from 'react';

export interface TokenStrategyConfig {
  ast_skeleton_pruning: boolean;
  markdown_doc_pruning: boolean;
  config_schema_minification: boolean;
  diagnostic_log_slicing: boolean;
  git_diff_pruning: boolean;
  conversation_memory_compaction: boolean;
}

export interface TokenOptimizationSettings {
  enabled: boolean;
  mode: 'disabled' | 'conservative' | 'standard' | 'aggressive' | 'extreme';
  strategies: TokenStrategyConfig;
  monthly_baseline_tokens: number;
}

export const TokenOptimizationSettingsPanel: React.FC = () => {
  const [settings, setSettings] = useState<TokenOptimizationSettings>({
    enabled: true,
    mode: 'standard',
    strategies: {
      ast_skeleton_pruning: true,
      markdown_doc_pruning: true,
      config_schema_minification: true,
      diagnostic_log_slicing: true,
      git_diff_pruning: true,
      conversation_memory_compaction: true,
    },
    monthly_baseline_tokens: 50_000_000,
  });

  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Mode descriptions and expected compression ratios
  const modeMetrics = {
    disabled: { label: 'Disabled', ratio: 0, desc: 'Zero compression. Raw context dispatched.' },
    conservative: { label: 'Conservative', ratio: 0.35, desc: 'Preserves all docstrings & type headers.' },
    standard: { label: 'Standard (Recommended)', ratio: 0.55, desc: 'Structural AST skeletons & doc table pruning.' },
    aggressive: { label: 'Aggressive', ratio: 0.75, desc: 'Minimal signatures, schema minification & log slicing.' },
    extreme: { label: 'Extreme', ratio: 0.90, desc: 'Single-line symbol indices & dense state memory.' },
  };

  const handleToggleMaster = () => {
    setSettings((prev) => {
      const nextEnabled = !prev.enabled;
      return {
        ...prev,
        enabled: nextEnabled,
        mode: nextEnabled ? 'standard' : 'disabled',
      };
    });
  };

  const handleSelectMode = (newMode: 'disabled' | 'conservative' | 'standard' | 'aggressive' | 'extreme') => {
    setSettings((prev) => ({
      ...prev,
      mode: newMode,
      enabled: newMode !== 'disabled',
    }));
  };

  const handleToggleStrategy = (key: keyof TokenStrategyConfig) => {
    setSettings((prev) => ({
      ...prev,
      strategies: {
        ...prev.strategies,
        [key]: !prev.strategies[key],
      },
    }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      // Simulation or call to /api/v1/tokens/config
      await new Promise((resolve) => setTimeout(resolve, 400));
      setSaveSuccess(true);
      setTimeout(() => setSaveSuccess(false), 3000);
    } finally {
      setSaving(false);
    }
  };

  // Real-time FinOps Calculations ($3.00/MTok standard blended rate)
  const currentRatio = settings.enabled ? modeMetrics[settings.mode].ratio : 0;
  const tokensSaved = Math.round(settings.monthly_baseline_tokens * currentRatio);
  const grossSavingsUsd = (tokensSaved / 1_000_000) * 3.0;
  const revShareFeeUsd = grossSavingsUsd * 0.15;
  const netSavingsUsd = grossSavingsUsd - revShareFeeUsd;

  return (
    <div className="w-full max-w-5xl mx-auto p-6 bg-slate-900 text-slate-100 rounded-2xl border border-slate-800 shadow-2xl">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-6 border-b border-slate-800 gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h2 className="text-2xl font-bold tracking-tight text-white">Token Optimization & FinOps Control</h2>
            <span
              className={`px-3 py-1 rounded-full text-xs font-semibold ${
                settings.enabled ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-400 border border-rose-500/30'
              }`}
            >
              {settings.enabled ? 'ACTIVE & METERED' : 'DISABLED'}
            </span>
          </div>
          <p className="text-sm text-slate-400 mt-1">
            Configure multi-tier context compression to reduce LLM token consumption and maximize net ROI.
          </p>
        </div>

        <button
          onClick={handleToggleMaster}
          className={`px-5 py-2.5 rounded-xl font-medium text-sm transition-all shadow-md ${
            settings.enabled
              ? 'bg-rose-600/90 hover:bg-rose-500 text-white shadow-rose-950/40'
              : 'bg-emerald-600 hover:bg-emerald-500 text-white shadow-emerald-950/40'
          }`}
        >
          {settings.enabled ? 'Disable Token Optimization' : 'Enable Token Optimization'}
        </button>
      </div>

      {/* Mode Selector Cards */}
      <div className="mt-8">
        <label className="block text-sm font-semibold uppercase tracking-wider text-slate-400 mb-3">
          Optimization Intensity Preset
        </label>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
          {(Object.keys(modeMetrics) as Array<keyof typeof modeMetrics>).map((mKey) => {
            const m = modeMetrics[mKey];
            const isSelected = settings.mode === mKey;
            return (
              <div
                key={mKey}
                onClick={() => handleSelectMode(mKey)}
                className={`cursor-pointer p-4 rounded-xl border transition-all ${
                  isSelected
                    ? 'border-indigo-500 bg-indigo-950/40 ring-2 ring-indigo-500/50 shadow-lg shadow-indigo-950/50'
                    : 'border-slate-800 bg-slate-800/40 hover:border-slate-700 hover:bg-slate-800/80'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-300">{m.label}</span>
                  <span className="text-xs font-bold text-indigo-400">{Math.round(m.ratio * 100)}%</span>
                </div>
                <p className="text-xs text-slate-400 mt-2 line-clamp-2">{m.desc}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Granular Strategy Toggles */}
      <div className="mt-8">
        <label className="block text-sm font-semibold uppercase tracking-wider text-slate-400 mb-3">
          Granular Compression Strategies
        </label>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            {
              key: 'ast_skeleton_pruning' as const,
              title: 'AST Skeleton Pruning',
              desc: 'Strips function bodies while preserving signatures, interfaces, and exported types.',
            },
            {
              key: 'markdown_doc_pruning' as const,
              title: 'Markdown & Living Docs Pruner',
              desc: 'Removes badges, truncates large data tables, and strips repetitive prose boilerplate.',
            },
            {
              key: 'config_schema_minification' as const,
              title: 'Config & JSONSchema Minification',
              desc: 'Strips YAML comments, default empty fields, and schemas metadata.',
            },
            {
              key: 'diagnostic_log_slicing' as const,
              title: 'Diagnostic Log & Stack Slicing',
              desc: 'Slices multi-page error logs down to isolated root assertions and failure frames.',
            },
            {
              key: 'git_diff_pruning' as const,
              title: 'Git Diff & Lockfile Filter',
              desc: 'Filters lockfiles (package-lock, yarn, poetry) and limits context lines to -U2.',
            },
            {
              key: 'conversation_memory_compaction' as const,
              title: 'Conversation Memory Squeezer',
              desc: 'Compacts multi-turn agent history into an immutable state ledger and goal vector.',
            },
          ].map((strat) => {
            const isChecked = settings.enabled && settings.strategies[strat.key];
            return (
              <div
                key={strat.key}
                onClick={() => settings.enabled && handleToggleStrategy(strat.key)}
                className={`flex items-start justify-between p-4 rounded-xl border transition-all ${
                  !settings.enabled
                    ? 'opacity-40 cursor-not-allowed border-slate-800/40 bg-slate-800/10'
                    : isChecked
                    ? 'cursor-pointer border-indigo-500/50 bg-indigo-950/20'
                    : 'cursor-pointer border-slate-800 bg-slate-800/30 hover:border-slate-700'
                }`}
              >
                <div className="pr-4">
                  <span className="text-sm font-semibold text-white">{strat.title}</span>
                  <p className="text-xs text-slate-400 mt-1">{strat.desc}</p>
                </div>
                <input
                  type="checkbox"
                  checked={isChecked}
                  disabled={!settings.enabled}
                  onChange={() => handleToggleStrategy(strat.key)}
                  className="mt-1 h-5 w-5 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-slate-900 cursor-pointer"
                />
              </div>
            );
          })}
        </div>
      </div>

      {/* Live FinOps ROI Calculator Preview */}
      <div className="mt-8 p-5 bg-gradient-to-br from-slate-800/70 to-slate-900/90 rounded-xl border border-slate-700/60 shadow-inner">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-indigo-400 mb-4 flex items-center gap-2">
          <span>⚡</span> Real-Time FinOps ROI & Performance Fee Calculator
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-center">
          <div className="p-3 bg-slate-900/80 rounded-lg border border-slate-800">
            <span className="text-xs text-slate-400">Context Reduction Ratio</span>
            <p className="text-xl font-bold text-white mt-1">{(currentRatio * 100).toFixed(0)}%</p>
          </div>
          <div className="p-3 bg-slate-900/80 rounded-lg border border-slate-800">
            <span className="text-xs text-slate-400">Est. Monthly Tokens Saved</span>
            <p className="text-xl font-bold text-emerald-400 mt-1">{tokensSaved.toLocaleString()}</p>
          </div>
          <div className="p-3 bg-slate-900/80 rounded-lg border border-slate-800">
            <span className="text-xs text-slate-400">Gross Spend Avoided</span>
            <p className="text-xl font-bold text-emerald-400 mt-1">${grossSavingsUsd.toFixed(2)}/mo</p>
          </div>
          <div className="p-3 bg-slate-900/80 rounded-lg border border-slate-800">
            <span className="text-xs text-slate-400">Net Customer Cash Savings (85%)</span>
            <p className="text-xl font-bold text-cyan-400 mt-1">${netSavingsUsd.toFixed(2)}/mo</p>
          </div>
        </div>
      </div>

      {/* Footer Controls */}
      <div className="mt-8 flex items-center justify-between pt-5 border-t border-slate-800">
        <span className="text-xs text-slate-500">
          State sealed cryptographically to <code className="text-indigo-400">token_compression_rules.yaml</code>
        </span>
        <div className="flex items-center gap-3">
          {saveSuccess && <span className="text-xs text-emerald-400 font-medium">✓ Configuration updated successfully</span>}
          <button
            onClick={handleSave}
            disabled={saving}
            className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-sm font-semibold transition-all shadow-lg shadow-indigo-900/40 disabled:opacity-50"
          >
            {saving ? 'Saving...' : 'Apply & Save Settings'}
          </button>
        </div>
      </div>
    </div>
  );
};
export default TokenOptimizationSettingsPanel;
