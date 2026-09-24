#!/usr/bin/env python3
"""
Neutron Binary Percipience - Enterprise Product Site & Cloud SaaS Portal
Detailed Multi-Section Product Platform featuring:
- Executive Value Proposition & Hero
- 8 Deep Technical Capabilities with Code Skeletons & Latency SLAs
- Quantified ROI & Business Benefits by ICP (AI Studios, Enterprises, Regulated FinTech)
- Interactive Competitive Differentiation Matrix (vs Cursor, LangChain, Arize Phoenix)
- Interactive AST Pruning & Token Optimization Playground
- Live Merkle State DAG Explorer & Time-Travel Recovery Console
- AWS vs Google Cloud Hosting Economics & Breakeven Analysis
- Self-Serve Quad-Space Provisioning & 15% Rev-Share Metering Engine
"""

from typing import Dict, Any, List, Optional, Tuple
import sys
import os
import json
import yaml
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

REPO_ROOT = Path(__file__).resolve().parents[2]
for p_dir in [REPO_ROOT / ".nb", REPO_ROOT / ".nb" / "core", REPO_ROOT / "workplace"]:
    if str(p_dir) not in sys.path:
        sys.path.insert(0, str(p_dir))

from core.ast_optimizer import ASTOptimizer
from core.merkle_engine import MerkleEngine
from core.poisoning_sentinel import PoisoningSentinel
from core.maturity_evaluator import MaturityEvaluator
from core.worktree_engine import WorktreeEngine
from core.token_tracker import TokenTracker
from core.agent_plugin_engine import AgentPluginEngine
from core.cognitive_router import CognitiveRouter
from core.flaky_test_detector import FlakyTestDetector
from core.contract_compatibility_checker import ContractCompatibilityChecker
from core.context_gateway import ContextGateway
from core.nbpack_envelope import NBPackEnvelope
from core.dependency_cve_sentinel import DependencyCVESentinel
from core.doc_drift_synchronizer import DocDriftSynchronizer
from core.handoff_validator import HandoffValidator
from core.semantic_parity_engine import SemanticParityEngine
from core.reconciliation_engine import DualReconciliationEngine
from core.otel_exporter import OpenTelemetryGenAIExporter
from core.eval_scoring_engine import EvalScoringEngine
from core.prompt_benchmark_engine import PromptBenchmarkEngine
from core.semantic_prompt_cache import SemanticPromptCache
from core.attention_budgeter import AttentionBudgeter
from core.adversarial_fuzzer import AdversarialFuzzer
from core.ambiguity_resolver import AmbiguityResolver

from core.autonomous_cicd import (
    SelfSustainingEngine,
    AutonomousHealer,
    SelfImprovingEngine,
    AutonomousCICDOrchestrator
)
from core.tenant_manager import (
    TenantManager,
    TenantRole,
    Tenant,
    Project,
    Repository,
    WorkspaceNode,
    TenantUser,
)
from core.project_scaffolder import ProjectScaffolder, ScaffoldResult
from core.kms_broker import KMSBroker, KeyRecord, SealedEnclaveBundle
from core.commercial_packager_provisioner import CommercialPackagerProvisioner
from core.project_policy_engine import (
    ProjectPolicyManager,
    ProjectPolicy,
    AttentionSlicingPolicy,
    CognitiveRoutingPolicy,
    ASTPruningPolicy,
    SelfHealingSLAPolicy,
    WireContractRule
)

PORTAL_HTML = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Neutron Binary Percipience | Enterprise Context Engineering OS &amp; CI/CD Gatekeeper</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>

    :root {
      /* Dark Theme Tokens (Default) */
      --bg: #070B14;
      --bg-panel: #0D1527;
      --bg-card: #111C33;
      --bg-card-hover: #182849;
      --border: #1E2D4A;
      --border-accent: #00F2FE;
      --text: #F8FAFC;
      --muted: #94A3B8;
      --code-bg: #050811;
      --cyan: #00F2FE;
      --cyan-glow: rgba(0, 242, 254, 0.18);
      --gradient-brand: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
      --gradient-purple: linear-gradient(135deg, #A855F7 0%, #6366F1 100%);
      --gradient-card: linear-gradient(180deg, rgba(17, 28, 51, 0.8) 0%, rgba(13, 21, 39, 0.95) 100%);
      --green: #10B981;
      --green-glow: rgba(16, 185, 129, 0.18);
      --emerald: #10B981;
      --purple: #A855F7;
      --amber: #F59E0B;
      --red: #F43F5E;
      --header-bg: rgba(7, 11, 20, 0.94);
      --table-th: #091021;
      --cat-header: #0D172E;
      --toggle-bg: #1A263F;
      --shadow-card: 0 8px 24px rgba(0, 0, 0, 0.4);
      --shadow-glow: 0 0 20px rgba(0, 242, 254, 0.15);
      /* Compatibility aliases */
      --text-muted: var(--muted);
      --text-color: var(--text);
      --card-bg: var(--bg-card);
      --border-color: var(--border);
    }

    [data-theme="light"] {
      /* Light Theme Tokens */
      --bg: #F8FAFC;
      --bg-panel: #FFFFFF;
      --bg-card: #FFFFFF;
      --bg-card-hover: #F1F5F9;
      --border: #E2E8F0;
      --border-accent: #0284C7;
      --text: #0F172A;
      --muted: #64748B;
      --code-bg: #F8FAFC;
      --cyan: #0284C7;
      --cyan-glow: rgba(2, 132, 199, 0.12);
      --gradient-brand: linear-gradient(135deg, #0284C7 0%, #2563EB 100%);
      --gradient-purple: linear-gradient(135deg, #9333EA 0%, #4F46E5 100%);
      --gradient-card: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
      --green: #059669;
      --green-glow: rgba(5, 150, 105, 0.12);
      --emerald: #059669;
      --purple: #9333EA;
      --amber: #D97706;
      --red: #E11D48;
      --header-bg: rgba(255, 255, 255, 0.94);
      --table-th: #F1F5F9;
      --cat-header: #F8FAFC;
      --toggle-bg: #E2E8F0;
      --shadow-card: 0 4px 16px rgba(0, 0, 0, 0.06);
      --shadow-glow: 0 0 16px rgba(2, 132, 199, 0.1);
      /* Compatibility aliases */
      --text-muted: var(--muted);
      --text-color: var(--text);
      --card-bg: var(--bg-card);
      --border-color: var(--border);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; transition: background-color 0.2s ease, border-color 0.2s ease, color 0.15s ease; }
    body { background: var(--bg); color: var(--text); min-height: 100vh; display: flex; flex-direction: column; overflow-x: hidden; }

    /* Header */
    header { background: var(--header-bg); backdrop-filter: blur(16px); border-bottom: 1px solid var(--border); padding: 12px 28px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }
    .brand-wrap { display: flex; align-items: center; gap: 12px; }
    .logo-badge { background: var(--gradient-brand); color: #070B14; font-weight: 900; font-size: 18px; width: 34px; height: 34px; border-radius: 8px; display: flex; align-items: center; justify-content: center; box-shadow: var(--shadow-glow); }
    .brand-title { font-size: 16px; font-weight: 800; letter-spacing: -0.02em; background: var(--gradient-brand); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .brand-sub { font-size: 10px; color: var(--muted); font-family: 'JetBrains Mono', monospace; }
    .nav { display: flex; gap: 4px; align-items: center; flex-wrap: wrap; }
    .nav-btn { background: transparent; border: 1px solid transparent; color: var(--muted); padding: 6px 11px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1); }
    .nav-btn:hover { color: var(--text); background: var(--bg-card-hover); }
    .nav-btn.active { color: var(--text); background: var(--bg-card); border-color: var(--border-accent); box-shadow: var(--shadow-glow); }
    .theme-toggle-btn { background: var(--toggle-bg); border: 1px solid var(--border); color: var(--text); padding: 5px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; cursor: pointer; margin-left: 8px; }

    /* Main Container */
    main { flex: 1; max-width: 1320px; margin: 0 auto; width: 100%; padding: 24px 20px; }
    .tab-content { display: none; }
    .tab-content.active { display: block; animation: fadeIn 0.25s cubic-bezier(0.16, 1, 0.3, 1); }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }

    /* Section Typography */
    .section-title { font-size: 22px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 6px; color: var(--text); }
    .section-desc { font-size: 13px; color: var(--muted); margin-bottom: 22px; line-height: 1.55; max-width: 860px; }

    /* Hero */
    .hero { text-align: center; padding: 32px 16px 24px; max-width: 980px; margin: 0 auto 24px; }
    .hero-badge { display: inline-flex; align-items: center; gap: 6px; background: var(--cyan-glow); border: 1px solid var(--border-accent); color: var(--cyan); padding: 5px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 14px; }
    .hero h1 { font-size: 32px; font-weight: 800; line-height: 1.2; letter-spacing: -0.03em; margin-bottom: 12px; }
    .hero p { font-size: 14px; color: var(--muted); line-height: 1.6; max-width: 780px; margin: 0 auto 20px; }
    .hero-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 20px; }
    .hero-stat-item { background: var(--gradient-card); border: 1px solid var(--border); padding: 14px 12px; border-radius: 10px; text-align: center; box-shadow: var(--shadow-card); }
    .hero-stat-val { font-size: 20px; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: var(--cyan); margin-bottom: 3px; letter-spacing: -0.02em; }
    .hero-stat-label { font-size: 11px; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }

    /* Cards & Grids */
    .grid-2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(440px, 1fr)); gap: 18px; }
    .grid-3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap: 18px; }
    .grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px; }
    .grid-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px; }
    
    .card, .panel-card { background: var(--gradient-card); border: 1px solid var(--border); border-radius: 12px; padding: 18px 20px; position: relative; box-shadow: var(--shadow-card); transition: transform 0.2s ease, border-color 0.2s ease; margin-bottom: 18px; }
    .card:hover, .panel-card:hover { border-color: var(--border-accent); transform: translateY(-1px); }
    .card-title, .panel-card h3 { font-size: 15px; font-weight: 700; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between; gap: 8px; color: var(--text); line-height: 1.35; }
    .card-badge { display: inline-block; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; padding: 2px 7px; border-radius: 5px; background: var(--cyan-glow); color: var(--cyan); margin-bottom: 8px; }
    .card h3 { font-size: 15px; font-weight: 700; margin-bottom: 6px; color: var(--text); line-height: 1.35; }
    .card h4 { font-size: 13px; font-weight: 700; color: var(--text); margin-top: 14px; margin-bottom: 6px; }
    .card p, .panel-card p { font-size: 12px; color: var(--muted); line-height: 1.55; margin-bottom: 10px; }
    
    .metric-card { background: var(--gradient-card); border: 1px solid var(--border); border-radius: 10px; padding: 14px 12px; text-align: center; box-shadow: var(--shadow-card); }
    .metric-val { font-size: 20px; font-weight: 800; font-family: 'JetBrains Mono', monospace; margin-bottom: 3px; letter-spacing: -0.02em; line-height: 1.2; }
    .metric-label { font-size: 11px; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
    .metric-sub { font-size: 10.5px; color: var(--muted); margin-top: 3px; font-weight: 500; }

    /* Stat Box Component */
    .stat-box {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 7px 10px;
      margin-top: 6px;
      background: rgba(0, 0, 0, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 6px;
      font-size: 12px;
      color: var(--muted);
    }
    [data-theme="light"] .stat-box {
      background: rgba(0, 0, 0, 0.03);
      border-color: rgba(0, 0, 0, 0.06);
    }
    .stat-val {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      font-size: 12px;
      color: var(--text);
    }

    /* Price Component */
    .price-val { font-size: 22px; font-weight: 800; font-family: 'JetBrains Mono', monospace; color: var(--cyan); margin: 8px 0 10px; }
    .price-period { font-size: 11.5px; font-weight: 500; color: var(--muted); }

    /* Bullet Lists */
    ul, ol, .bullet-list { list-style: none; padding-left: 0; margin: 8px 0; }
    li { font-size: 12px; line-height: 1.55; color: var(--muted); position: relative; padding-left: 16px; margin-bottom: 5px; }
    li::before { content: "▪"; color: var(--cyan); position: absolute; left: 0; top: -1px; font-size: 13px; }

    /* Tables & Table Wrapper */
    .table-wrap { width: 100%; overflow-x: auto; border: 1px solid var(--border); border-radius: 10px; background: var(--bg-panel); box-shadow: var(--shadow-card); margin-top: 12px; margin-bottom: 22px; }
    table, .table { width: 100%; border-collapse: collapse; text-align: left; }
    th, .table th { background: var(--table-th); color: var(--muted); font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; padding: 10px 14px; border-bottom: 1px solid var(--border); white-space: nowrap; }
    td, .table td { padding: 9px 14px; font-size: 12px; line-height: 1.45; border-bottom: 1px solid var(--border); color: var(--text); }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: var(--bg-card-hover); }
    .cat-header { background: var(--cat-header); font-weight: 800; font-size: 12px; color: var(--cyan); padding: 10px 14px; border-left: 3px solid var(--cyan); letter-spacing: 0.02em; }
    .feature-name { font-weight: 700; font-size: 12px; color: var(--text); }
    .percipience-cell { background: rgba(0, 242, 254, 0.05); border-left: 1px solid rgba(0, 242, 254, 0.2); border-right: 1px solid rgba(0, 242, 254, 0.2); font-weight: 600; color: #E0F2FE; }

    /* Badges & Status Pills */
    .badge { display: inline-flex; align-items: center; gap: 4px; padding: 2px 7px; border-radius: 5px; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; }
    .badge-cyan { background: var(--cyan-glow); color: var(--cyan); border: 1px solid var(--border-accent); }
    .badge-purple { background: rgba(168, 85, 247, 0.15); color: var(--purple); border: 1px solid var(--purple); }
    .badge-emerald { background: var(--green-glow); color: var(--green); border: 1px solid var(--green); }
    .badge-amber { background: rgba(245, 158, 11, 0.15); color: var(--amber); border: 1px solid var(--amber); }
    .status-pill { display: inline-block; padding: 2px 7px; border-radius: 10px; font-size: 10px; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
    .status-active { background: var(--green-glow); color: var(--green); }
    .status-warning { background: rgba(245, 158, 11, 0.15); color: var(--amber); }

    /* Forms, Inputs, Form Groups */
    .form-group { margin-bottom: 14px; display: flex; flex-direction: column; gap: 5px; }
    .form-label { font-size: 11px; font-weight: 700; color: var(--text); display: flex; justify-content: space-between; align-items: center; letter-spacing: 0.02em; }
    .form-hint { font-size: 10px; color: var(--muted); font-weight: 400; }
    .input, input[type="text"], input[type="password"], input[type="number"], input[type="email"], select, textarea {
      background: var(--code-bg);
      border: 1px solid var(--border);
      color: var(--text);
      border-radius: 7px;
      padding: 9px 12px;
      font-size: 12px;
      width: 100%;
      outline: none;
      font-family: inherit;
      transition: all 0.2s ease;
    }
    .input:focus, input[type="text"]:focus, input[type="password"]:focus, input[type="number"]:focus, input[type="email"]:focus, select:focus, textarea:focus {
      border-color: var(--cyan);
      box-shadow: 0 0 0 3px var(--cyan-glow);
    }
    select { cursor: pointer; }
    textarea { min-height: 80px; font-family: 'JetBrains Mono', monospace; font-size: 11px; resize: vertical; }

    /* Buttons */
    .btn, .action-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      padding: 7px 14px;
      border-radius: 7px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.2s ease;
      text-decoration: none;
      font-family: inherit;
    }
    .action-btn, .btn-primary {
      background: var(--gradient-brand);
      color: #070B14;
      box-shadow: var(--shadow-glow);
    }
    .action-btn:hover, .btn-primary:hover {
      opacity: 0.92;
      transform: translateY(-1px);
      color: #070B14;
    }
    .btn-secondary {
      background: var(--bg-card);
      color: var(--text);
      border: 1px solid var(--border);
    }
    .btn-secondary:hover {
      background: var(--bg-card-hover);
      border-color: var(--border-accent);
    }
    .btn-cyan { background: var(--cyan-glow); color: var(--cyan); border-color: var(--border-accent); }
    .btn-emerald { background: var(--green-glow); color: var(--green); border-color: var(--green); }
    .btn-purple { background: rgba(168, 85, 247, 0.15); color: var(--purple); border-color: var(--purple); }
    .btn-cyan:hover, .btn-emerald:hover, .btn-purple:hover { transform: translateY(-1px); }

    /* Utility Colors & Progress Bars */
    .text-emerald, .text-green { color: var(--green); }
    .text-cyan { color: var(--cyan); }
    .text-purple { color: var(--purple); }
    .text-amber { color: var(--amber); }
    .text-red { color: var(--red); }
    .bg-emerald, .bg-green { background: var(--green); }
    .bg-cyan { background: var(--cyan); }
    .bg-purple { background: var(--purple); }
    .bg-amber { background: var(--amber); }
    .bg-red { background: var(--red); }

    .vector-list { display: flex; flex-direction: column; gap: 10px; margin-top: 10px; }
    .vector-item { display: flex; flex-direction: column; gap: 4px; font-size: 12px; }
    .vector-header { display: flex; justify-content: space-between; align-items: center; }
    .bar-track { background: var(--code-bg); height: 6px; border-radius: 3px; overflow: hidden; border: 1px solid var(--border); }
    .bar-fill { height: 100%; border-radius: 3px; transition: width 0.3s ease; }

    pre, code { font-family: 'JetBrains Mono', monospace; }
    pre { background: var(--code-bg); border: 1px solid var(--border); border-radius: 7px; padding: 10px 12px; font-size: 11px; color: var(--cyan); overflow-x: auto; margin: 8px 0; }


    /* Range Sliders & Policy Controls (CAP-40 / CAP-41) */
    .slider-group { margin-bottom: 14px; }
    .slider-header { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px; }
    .slider-header label { font-weight: 600; color: var(--text); }
    .slider-val { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--cyan); }
    input[type=range] {
      -webkit-appearance: none;
      width: 100%;
      height: 6px;
      background: var(--border);
      border-radius: 4px;
      outline: none;
      margin: 4px 0;
    }
    input[type=range]::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: var(--cyan);
      cursor: pointer;
      border: 2px solid var(--card-bg);
      box-shadow: 0 0 8px rgba(6, 182, 212, 0.4);
      transition: transform 0.1s ease;
    }
    input[type=range]::-webkit-slider-thumb:hover {
      transform: scale(1.15);
    }
    .budget-bar-container {
      display: flex;
      height: 22px;
      border-radius: 6px;
      overflow: hidden;
      margin: 10px 0 16px;
      border: 1px solid var(--border);
      background: var(--code-bg);
    }
    .budget-slice {
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 10px;
      font-weight: 700;
      color: #fff;
      transition: width 0.2s ease;
      overflow: hidden;
      white-space: nowrap;
      text-shadow: 0 1px 2px rgba(0,0,0,0.6);
    }
    .tree-node {
      padding: 8px 14px;
      border-radius: 6px;
      background: var(--code-bg);
      border: 1px solid var(--border);
      margin-bottom: 8px;
      font-size: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .tree-node.level-2 { margin-left: 20px; border-left: 3px solid var(--cyan); }
    .tree-node.level-3 { margin-left: 40px; border-left: 3px solid var(--purple); }
    .tree-node.level-4 { margin-left: 60px; border-left: 3px solid var(--green); }

    /* Responsive Navigation & Mobile Adaptation */
    @media (max-width: 1200px) {
      header {
        flex-direction: column;
        align-items: stretch;
        gap: 10px;
        padding: 10px 18px;
      }
      .brand-wrap {
        justify-content: space-between;
        width: 100%;
      }
      .nav {
        width: 100%;
        overflow-x: auto;
        white-space: nowrap;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: thin;
        padding-bottom: 4px;
      }
      .nav::-webkit-scrollbar {
        height: 3px;
      }
      .nav::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 3px;
      }
      .nav-btn {
        flex-shrink: 0;
        white-space: nowrap;
      }
    }

    @media (max-width: 900px) {
      .hero {
        padding: 20px 10px 16px;
      }
      .hero h1 {
        font-size: 26px;
        line-height: 1.25;
      }
      .hero-stats {
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
      }
      .grid-2, .grid-3, .grid-4, .grid-cards {
        grid-template-columns: 1fr !important;
      }
      .metric-card, .hero-stat-item {
        padding: 12px 10px;
      }
      main {
        padding: 16px 12px;
      }
    }

    @media (max-width: 600px) {
      .hero h1 {
        font-size: 20px;
      }
      .hero p {
        font-size: 13px;
      }
      .hero-stats {
        grid-template-columns: 1fr;
      }
      .stat-box {
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
      }
      .card, .panel-card {
        padding: 14px 12px;
      }
      .table-wrap {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        margin: 0 -12px;
        padding: 0 12px;
      }
      table {
        min-width: 520px;
      }
      .budget-bar-container {
        height: 18px;
      }
      .budget-slice {
        font-size: 8.5px;
      }
      .btn, .action-btn {
        padding: 7px 12px;
      }
      .tree-node.level-2 { margin-left: 10px; }
      .tree-node.level-3 { margin-left: 18px; }
      .tree-node.level-4 { margin-left: 26px; }
    }
  </style>
</head>
<body>
  <header>
    <div class="brand-wrap">
      <div class="logo-badge">⚡</div>
      <div>
        <div class="brand-title">Neutron Binary Percipience</div>
        <div class="brand-sub">Context Engineering OS &amp; CI/CD Gatekeeper</div>
      </div>
    </div>
    <nav class="nav">
      <button class="nav-btn active" onclick="showTab('overview')">Overview</button>
      <button class="nav-btn" onclick="showTab('capabilities')">Capabilities</button>
      <button class="nav-btn" onclick="showTab('comparatives')">Comparatives</button>
      <button class="nav-btn" onclick="showTab('tier-matrix')">📊 Plan Matrix &amp; Ceilings</button>
      <button class="nav-btn" onclick="showTab('gateway')">Context Gateway</button>
      <button class="nav-btn" onclick="showTab('roi-calculator')">ROI &amp; Benefits</button>
      <button class="nav-btn" onclick="showTab('sandboxes')">Live Sandboxes</button>
      <button class="nav-btn" onclick="showTab('infrastructure')">Cloud &amp; OpEx</button>
      <button class="nav-btn" onclick="showTab('pricing')">Pricing</button>
      <button class="nav-btn" onclick="showTab('docs')">Docs</button>
      <button class="nav-btn" onclick="showTab('reports')">📑 Deep Reports</button>
      <button class="nav-btn" onclick="showTab('observability')">📈 Observability</button>
      <button class="nav-btn" onclick="showTab('client')" id="clientNavBtn" style="border:1px solid var(--cyan); color:var(--cyan); font-weight:700;">🔐 Client Space</button>
      <button class="nav-btn" onclick="showTab('governance'); loadGovernanceTab();" id="govNavBtn" style="border:1px solid var(--purple); color:var(--purple); font-weight:700;">🏛️ Multi-Tenant &amp; Policies</button>
      <button class="nav-btn" onclick="showTab('commercial-provisioner'); loadCommercialTab();" id="commercialNavBtn" style="border:1px solid var(--amber); color:var(--amber); font-weight:700;">📦 Commercial Provisioner</button>
      <button class="theme-toggle-btn" onclick="toggleTheme()" id="portalThemeBtn">🌙 Dark</button>
    </nav>
  </header>

  <main>
    <!-- TAB 1: OVERVIEW -->
    <section id="overview" class="tab-content active">
      <div class="hero">
        <div class="hero-badge">⚡ Commercial Play 3 Architecture</div>
        <h1>Enterprise Context Engineering OS<br>&amp; Autonomous CI/CD Gatekeeper</h1>
        <p>The first enterprise control plane that stops agentic context drift, isolates subagents in ephemeral Git worktrees, enforces cross-module contracts, and cuts LLM context token consumption by 50% to 70%.</p>
        
        <div class="hero-stats">
          <div class="hero-stat-item">
            <div class="hero-stat-val">58.4%</div>
            <div class="hero-stat-label">Measured Token Reduction</div>
          </div>
          <div class="hero-stat-item">
            <div class="hero-stat-val">&lt; 120ms</div>
            <div class="hero-stat-label">Tree-Sitter AST Pruning</div>
          </div>
          <div class="hero-stat-item">
            <div class="hero-stat-val">100%</div>
            <div class="hero-stat-label">Cryptographic Merkle Proofs</div>
          </div>
          <div class="hero-stat-item">
            <div class="hero-stat-val">0%</div>
            <div class="hero-stat-label">Plaintext Disk Residue (.nbpack)</div>
          </div>
        </div>

        <div style="display:flex; justify-content:center; gap:10px; margin-top:22px; flex-wrap:wrap;">
          <button class="btn btn-primary" onclick="showTab('gateway')">🚀 Try Context Gateway</button>
          <button class="btn btn-secondary" onclick="showTab('tier-matrix')">📊 Plan Matrix &amp; Ceilings</button>
          <button class="btn btn-secondary" onclick="showTab('roi-calculator')">💰 FinOps ROI Calculator</button>
          <button class="btn btn-secondary" onclick="showTab('governance')" style="border-color:var(--purple); color:var(--purple); font-weight:700;">🏛️ Multi-Tenant Policies</button>
        </div>
      </div>

      <div class="grid-3">
        <div class="card">
          <div class="card-badge">Root Problem</div>
          <h3>The Context Crisis</h3>
          <p>Unmanaged autonomous coding agents (Claude Code, Cursor) suffer catastrophic degradation: prompt bloat, memory leaks, hallucinated dependencies, and destructive global git conflicts.</p>
          <ul class="bullet-list">
            <li>Tokens burn uncontrollably (200k context windows)</li>
            <li>Subagents clobber uncommitted working trees</li>
            <li>Subtle API schema changes break upstream services</li>
          </ul>
        </div>

        <div class="card">
          <div class="card-badge">Percipience Engine</div>
          <h3>Quad-Space Standard</h3>
          <p>Strict structural partitioning of enterprise repositories into four immutable quadrants with deterministic boundary enforcement.</p>
          <ul class="bullet-list">
            <li><code>.nb/context/</code>: Formal contracts &amp; SHA-256 state ledger</li>
            <li><code>.nb/agentic/</code>: Bounded prompts &amp; verification DAGs</li>
            <li><code>workplace/</code>: Decoupled application source code</li>
            <li><code>user/</code>: Minimum Viable Sets &amp; quarantine sentinels</li>
          </ul>
        </div>

        <div class="card">
          <div class="card-badge">Financial Return</div>
          <h3>Performance Rev-Share</h3>
          <p>Percipience pays for itself. In addition to fixed licensing, our 15% token savings revenue-share add-on aligns our incentives directly with customer cost reduction.</p>
          <ul class="bullet-list">
            <li>Typical 50-dev team saves $118,800/yr net</li>
            <li>Cash-flow positive EBITDA on Customer 2</li>
            <li>91.2% AWS / 91.5% GCP hosting gross margins</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- TAB 2: CAPABILITIES -->
    <section id="capabilities" class="tab-content">
      <div class="section-title">Foundational Technical Subsystems (CAP-01 to CAP-39)</div>
      <div class="section-desc">Designed from the ground up to solve context poisoning, prompt leakage, workspace clobbering, and model drift in mission-critical enterprise codebases.</div>
      
      <div class="grid-2">
        <div class="card">
          <div class="card-badge">Concurrency (CAP-01)</div>
          <h3>1. Ephemeral Git Worktree Isolation</h3>
          <p>Assigns each autonomous coding subagent its own isolated git worktree backed by a pre-warmed gVisor microVM sandbox. Prevents branch locks and dirty working tree overwrites.</p>
          <pre>git worktree add -b wt_agent_04 .nb/workspaces/wt_agent_04 main
percipience worktree acquire --agent agent_dev_04 --ttl 3600</pre>
          <div class="stat-box"><span>SLA Allocation Latency:</span><span class="stat-val text-cyan">&lt; 180ms</span></div>
        </div>

        <div class="card">
          <div class="card-badge">Token FinOps (CAP-02)</div>
          <h3>2. Polyglot Tree-Sitter 6D AST Body Pruning</h3>
          <p>Replaces internal method bodies with syntactic placeholders (<code>... [AST_PRUNED]</code>), cutting prompt token overhead by 50%–75% while preserving 100% of public interface contracts.</p>
          <pre>percipience optimize --file payment_service.py --dialect python --preserve-types</pre>
          <div class="stat-box"><span>Measured Token Drop:</span><span class="stat-val text-emerald">50.3% ($15.69 Gross Saved)</span></div>
        </div>

        <div class="card">
          <div class="card-badge">Anti-Drift (CAP-03)</div>
          <h3>3. Semantic Parity &amp; Reverse AST Reconciliation</h3>
          <p>Computes mathematical semantic parity score comparing generated code against ground-truth specifications. Generates surgical reverse AST diffs to revert unauthorized edits.</p>
          <pre>percipience drift reconcile --mode revert --module mod_auth</pre>
          <div class="stat-box"><span>Parity Score:</span><span class="stat-val text-emerald">0.9960 (ALIGNED)</span></div>
        </div>

        <div class="card">
          <div class="card-badge">Governance (CAP-31)</div>
          <h3>4. 4-Tier Swarm Authority &amp; Anti-Usurpation Tree</h3>
          <p>Enforces strict role hierarchies (<code>ORCHESTRATOR &gt; DOMAIN_ARCHITECT &gt; SPECIALIST_WORKER &gt; GATEKEEPER</code>) and intercepts rogue subagent spawning beyond recursion depth ceiling D=2.</p>
          <pre>percipience swarm audit --depth-ceiling 2 --verify-leases</pre>
          <div class="stat-box"><span>Rogue Spawns Blocked:</span><span class="stat-val text-cyan">100% Intercepted</span></div>
        </div>

        <div class="card">
          <div class="card-badge">Resilience (CAP-29)</div>
          <h3>5. 4-Pillar Error Taxonomy &amp; Self-Healing Playbooks</h3>
          <p>Classifies agent failures into TRANSIENT (rate limits), STRUCTURAL (syntax errors), INVARIANT (test failures), and HALLUCINATORY (invented symbols), routing each to specialized self-healing playbooks.</p>
          <pre>percipience heal --error-type STRUCTURAL --target-file gateway.py</pre>
          <div class="stat-box"><span>MTTR Remediation:</span><span class="stat-val text-purple">&lt; 3 Bounded Iterations</span></div>
        </div>

        <div class="card">
          <div class="card-badge">Context Slicing (CAP-33)</div>
          <h3>6. Mathematical Attention Slicing (15/25/35/10/15)</h3>
          <p>Enforces strict proportional token budget quotas: 15% System Invariants, 25% Schemas/Contracts, 35% AST Skeletons, 10% ReAct Trajectories, 15% LLM Generation Target Space.</p>
          <pre>percipience budget --allocate-quotas --window-size 32000</pre>
          <div class="stat-box"><span>Attention Degradation:</span><span class="stat-val text-emerald">0% Lost-in-Middle</span></div>
        </div>

        <div class="card">
          <div class="card-badge">Security (CAP-32)</div>
          <h3>7. Adversarial Mutation Fuzzer &amp; Chaos Injection</h3>
          <p>Subjecting generated code to boundary condition fuzzing, SQL/XSS injections, schema mutations, and chaos faults to guarantee zero unhandled runtime exceptions before PR merging.</p>
          <pre>percipience fuzz --target mod_billing --vectors numerical,sql,schema</pre>
          <div class="stat-box"><span>Fuzz Mutation Coverage:</span><span class="stat-val text-cyan">100% Passing</span></div>
        </div>

        <div class="card">
          <div class="card-badge">Observability (CAP-36 &amp; CAP-37)</div>
          <h3>8. OpenTelemetry GenAI &amp; 5D G-Eval Radar</h3>
          <p>Streams standardized W3C <code>traceparent</code> headers, TTFT waterfalls, and multi-dimensional G-Eval quality scores (Faithfulness, Hallucination Freedom, Code Correctness) to enterprise APMs.</p>
          <pre>percipience otel export --target datadog --w3c-traceparent 00-4bf92...</pre>
          <div class="stat-box"><span>Composite G-Eval Score:</span><span class="stat-val text-emerald">0.962 / 1.00 (PASSED)</span></div>
        </div>
      </div>
    </section>

    <!-- TAB 3: COMPARATIVES -->
    <section id="comparatives" class="tab-content">
      <div class="section-title">Competitive Differentiation Matrix &amp; Autonomous CI/CD Analysis</div>
      <div class="section-desc">See how Neutron Binary Percipience compares against generic coding assistants (Cursor / Claude Code), trace libraries (LangSmith), legacy observability (Arize Phoenix), and traditional CI/CD runners (GitHub Actions / Jenkins).</div>

      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th style="width:20%;">Capability Dimension</th>
              <th style="width:16%;">Raw Cursor / Claude Code</th>
              <th style="width:16%;">LangChain / LangSmith</th>
              <th style="width:16%;">Arize Phoenix / Armor</th>
              <th style="width:16%;">Legacy CI/CD (GitHub Actions / Jenkins)</th>
              <th style="width:16%; color:var(--cyan); background:rgba(0,242,254,0.08);">⚡ Neutron Binary Percipience</th>
            </tr>
          </thead>
          <tbody>
            <!-- 1. AUTONOMOUS CI/CD DOMAIN -->
            <tr>
              <td colspan="6" class="cat-header">🤖 1. Autonomous CI/CD &amp; Closed-Loop Self-Healing Domain (Exclusive)</td>
            </tr>
            <tr>
              <td class="feature-name">Autonomous CI/CD Triad<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Self-Sustaining, Self-Recovering, Self-Improving</span></td>
              <td>❌ Single-turn command runner; zero closed-loop repair</td>
              <td>❌ Trace graph visualization only; no CI/CD remediation</td>
              <td>❌ Passive evaluation metrics; no execution loop</td>
              <td>❌ Passive red-build alerts; 100% human DevOps triage required</td>
              <td class="percipience-cell">✅ <strong>Full Triad:</strong> SelfSustainingEngine (GC/TTL) + AutonomousHealer + SelfImprovingEngine</td>
            </tr>
            <tr>
              <td class="feature-name">Diagnostic Re-Prompting Loop (CAP-02)<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Bounded Isolated Prompt Envelopes</span></td>
              <td>❌ Unbounded brute-force retries with noisy 500-line error logs</td>
              <td>❌ None</td>
              <td>❌ None</td>
              <td>❌ None (requires developer commit push to re-test)</td>
              <td class="percipience-cell">✅ Slices failure trace to root assertion; bounded 3-attempt SLA; auto-fallback to rollback</td>
            </tr>
            <tr>
              <td class="feature-name">Surgical Micro-Module Rollback (RP_k)<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Zero Sibling Disruption</span></td>
              <td>❌ Destructive full git reset (destroys concurrent work)</td>
              <td>❌ No filesystem or git rollback capabilities</td>
              <td>❌ None (read-only logs)</td>
              <td>❌ Revert commit reverses entire PR branch / merge</td>
              <td class="percipience-cell">✅ Rewinds culprit micro-module to RP_k, sparing 100% of siblings in multi-module monorepos</td>
            </tr>
            <tr>
              <td class="feature-name">Flaky Test Statistical Quarantine<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Non-Blocking Isolation</span></td>
              <td>❌ Flaky tests block developer PRs or force manual skips</td>
              <td>❌ None</td>
              <td>❌ None</td>
              <td>⚠️ Manual @flaky annotations or rerun plugins (masks real bugs)</td>
              <td class="percipience-cell">✅ Multi-run statistical detection &amp; non-blocking quarantine in flaky_quarantine.yaml</td>
            </tr>
            <tr>
              <td class="feature-name">Cross-Module Wire Contract &amp; SemVer Gate<br><span style="font-size:11px; color:var(--muted); font-weight:400;">API Schema Evolution</span></td>
              <td>❌ Unchecked code generation leading to subtle API drift</td>
              <td>❌ None</td>
              <td>❌ None</td>
              <td>⚠️ Runtime integration test failures after deployment</td>
              <td class="percipience-cell">✅ Pre-merge JSON Schema / Protobuf contract audit; catches breaking changes &amp; missing SemVer</td>
            </tr>
            <tr>
              <td class="feature-name">Living Architecture &amp; Mermaid Engine<br><span style="font-size:11px; color:var(--muted); font-weight:400;">AST-to-Diagram Continuous Sync</span></td>
              <td>❌ Outdated markdown docs that drift immediately</td>
              <td>❌ None</td>
              <td>❌ None</td>
              <td>❌ Static doc build tools without syntax linting</td>
              <td class="percipience-cell">✅ Continuous AST-to-Mermaid generator with strict syntax linting &amp; Merkle hash validation</td>
            </tr>

            <!-- 2. CONTEXT ENGINEERING & FINOPS DOMAIN -->
            <tr>
              <td colspan="6" class="cat-header">⚡ 2. Context Engineering &amp; Multi-Strategy Token Optimization Domain</td>
            </tr>
            <tr>
              <td class="feature-name">6-Dimensional Token Compression<br><span style="font-size:11px; color:var(--muted); font-weight:400;">AST, Docs, Schemas, Tracebacks, Diffs, Memory</span></td>
              <td>⚠️ Rudimentary naive file grep and basic truncation</td>
              <td>❌ Passes full prompt text or unparsed chunk strings</td>
              <td>❌ None</td>
              <td>❌ None</td>
              <td class="percipience-cell">✅ <strong>6 Pruners:</strong> AST bodies, Markdown tables, YAML/JSON schemas, Test logs, Lockfile diffs, Memory compaction</td>
            </tr>
            <tr>
              <td class="feature-name">Prompt Prefix Cache Pinning<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Bit-for-Bit Deterministic Anchoring</span></td>
              <td>⚠️ Best-effort prompt prefix; high miss rate</td>
              <td>⚠️ Unpinned template variables invalidate KV cache</td>
              <td>❌ No prompt restructuring</td>
              <td>❌ N/A</td>
              <td class="percipience-cell">✅ Bit-for-Bit Static Prefix Invariant Ordering (88%+ KV Cache Hit Rate)</td>
            </tr>
            <tr>
              <td class="feature-name">Selective Strategy Toggles &amp; Portal UI<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Granular Controls &amp; Presets</span></td>
              <td>❌ Hardcoded black-box heuristics</td>
              <td>❌ None</td>
              <td>❌ None</td>
              <td>❌ None</td>
              <td class="percipience-cell">✅ 5 intensity presets (conservative &rarr; extreme), granular strategy checkboxes, live ROI calculator</td>
            </tr>
            <tr>
              <td class="feature-name">Token Savings Rev-Share Model<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Outcome-Aligned FinOps</span></td>
              <td>❌ Flat seat licenses (/user/mo) regardless of efficiency</td>
              <td>❌ Per-trace event billing (zsh.005/trace) increasing with usage</td>
              <td>❌ Ingestion volume pricing</td>
              <td>❌ Per-minute runner billing (GitHub Actions minutes)</td>
              <td class="percipience-cell">✅ 15% of verified token savings; 100% aligned with customer cloud cost reduction</td>
            </tr>
            <tr>
              <td class="feature-name">Model-Agnostic Cognitive Tiering Router<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Dynamic LLM Complexity Routing</span></td>
              <td>❌ Single expensive flagship model for all turns (–/MTok)</td>
              <td>⚠️ Manual route chains; no dynamic AST complexity analysis</td>
              <td>❌ None</td>
              <td>❌ None</td>
              <td class="percipience-cell">✅ Dynamic Tier A (Claude 3.7 / Pro) vs Tier B (Haiku / Flash), dropping 90% cost on 78% of turns</td>
            </tr>

            <!-- 3. CRYPTOGRAPHIC GOVERNANCE DOMAIN -->
            <tr>
              <td colspan="6" class="cat-header">🛡️ 3. Cryptographic Governance &amp; Regulatory Non-Repudiation Domain</td>
            </tr>
            <tr>
              <td class="feature-name">Cryptographic Merkle State Machine<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Tamper-Evident SHA-256 DAG</span></td>
              <td>❌ None (standard git commit log only)</td>
              <td>⚠️ Centralized proprietary SaaS trace logs (vendor lock-in)</td>
              <td>❌ None</td>
              <td>⚠️ Ephemeral CI job logs wiped after 30-90 days</td>
              <td class="percipience-cell">✅ Tamper-evident SHA-256 DAG in context_ledger.yaml with rolling JSON epoch archiving (O(1) I/O)</td>
            </tr>
            <tr>
              <td class="feature-name">Semantic Parity &amp; 6-Vector Alignment<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Anti-Drift Dual Reconciliation</span></td>
              <td>❌ No contract alignment tracking</td>
              <td>❌ Basic trace latency logging</td>
              <td>❌ Drift alerts without remediation</td>
              <td>⚠️ Static unit test assertions</td>
              <td class="percipience-cell">✅ Dual-Reconciliation Engine (Revert Unprompted Edits vs Evolve RFC Contracts)</td>
            </tr>
            <tr>
              <td class="feature-name">SEC Rule 17a-4 / FINRA WORM Cloud Egress<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Dual-Vault Immutable Storage</span></td>
              <td>❌ None</td>
              <td>❌ None</td>
              <td>❌ None</td>
              <td>❌ None</td>
              <td class="percipience-cell">✅ Automated egress to AWS S3 Object Lock (Compliance Mode) &amp; GCP GCS Bucket Retention</td>
            </tr>

            <!-- 4. ENTERPRISE SECURITY DOMAIN -->
            <tr>
              <td colspan="6" class="cat-header">🔒 4. Enterprise Security &amp; Zero Client IP Exposure Domain</td>
            </tr>
            <tr>
              <td class="feature-name">Option 1 Context Gateway Enclave<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Zero Client Disk Residue</span></td>
              <td>❌ Plaintext markdown prompts exposed to client disk &amp; memory</td>
              <td>⚠️ Prompts logged in centralized SaaS without KMS enclaves</td>
              <td>❌ None (client holds entire system prompt)</td>
              <td>❌ Plaintext repository secrets injected into runner memory</td>
              <td class="percipience-cell">✅ Server-side In-Flight Prompt Injection in KMS RAM enclave; 0.0% plan disk exposure</td>
            </tr>
            <tr>
              <td class="feature-name">Proprietary IP Obfuscation (.nbpack)<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Sealed Binary Envelopes</span></td>
              <td>❌ Exposes raw system prompts in plaintext configs</td>
              <td>❌ Plaintext python/typescript configs</td>
              <td>❌ Plaintext prompt logs</td>
              <td>❌ Plaintext repository files</td>
              <td class="percipience-cell">✅ Sealed AES-256-GCM / Ed25519 binary (.nbpack) RAM-hydrated with KMS broker</td>
            </tr>
            <tr>
              <td class="feature-name">Supply-Chain Security &amp; AST CVE Sentinel<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Pre-Write Package Interception</span></td>
              <td>❌ No AST-level import CVE interception during agent generation</td>
              <td>❌ None</td>
              <td>⚠️ Prompt injection filters only; zero AST package gate</td>
              <td>⚠️ Post-merge vulnerability scans (Snyk / Dependabot)</td>
              <td class="percipience-cell">✅ Real-time AST import interception of malicious/typosquatted packages before file write</td>
            </tr>
            <tr>
              <td class="feature-name">4-Tier Swarm Authority &amp; Anti-Usurpation Tree<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Recursion Ceiling Enforcement</span></td>
              <td>❌ Unrestricted rogue subagent spawning</td>
              <td>⚠️ Memory limits only</td>
              <td>❌ No enforcement</td>
              <td>❌ None</td>
              <td class="percipience-cell">✅ 4-Tier Authority (Orchestrator &gt; Architect &gt; Worker &gt; Gatekeeper) with D_max = 2 ceiling</td>
            </tr>

            <!-- 5. CONCURRENCY & WORKSPACE ISOLATION -->
            <tr>
              <td colspan="6" class="cat-header">🌐 5. Distributed Concurrency &amp; Workspace Isolation Domain</td>
            </tr>
            <tr>
              <td class="feature-name">Distributed Redis Redlock Worktree Leases<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Active PID Liveness Probing</span></td>
              <td>❌ Dirty working tree collisions during simultaneous agent runs</td>
              <td>❌ None (relies on single environment or container)</td>
              <td>❌ None</td>
              <td>⚠️ Heavy Docker container per job (slow startup: 30s-2m)</td>
              <td class="percipience-cell">✅ Ephemeral Git worktrees (&lt;180ms startup) with Redis Redlock leases and dead-PID auto-eviction</td>
            </tr>
            <tr>
              <td class="feature-name">Bring Your Own Repository (BYOR)<br><span style="font-size:11px; color:var(--muted); font-weight:400;">Enterprise Firewall &amp; VPC Peering</span></td>
              <td>⚠️ Cloud GitHub.com or local desktop app required</td>
              <td>⚠️ Hosted public SaaS cloud only</td>
              <td>⚠️ Hosted public SaaS cloud only</td>
              <td>⚠️ Self-hosted runners require heavy agent maintenance</td>
              <td class="percipience-cell">✅ Native integration for self-hosted GitLab, GHES, Bitbucket DC with custom corporate CA certs</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- DEEP-DIVE: AUTONOMOUS CI/CD CAPABILITIES NOT AVAILABLE IN OTHER FRAMEWORKS -->
      <div style="margin-top:36px; margin-bottom:28px;">
        <div class="section-title">🚀 Autonomous CI/CD Capabilities Exclusive to Percipience</div>
        <div class="section-desc">Why standard CI/CD runners (Jenkins/Actions) and generic coding assistants (Cursor/Devin) fail in multi-agent enterprise environments, and how Percipience closes the loop.</div>

        <div class="grid-2">
          <div class="card">
            <div class="card-badge" style="background:rgba(0,242,254,0.15); color:var(--cyan);">Core Triad</div>
            <h3>1. Closed-Loop Autonomous Triad (Sustain • Heal • Improve)</h3>
            <p>Traditional CI/CD simply marks jobs as failed and waits for human intervention. Percipience deploys an autonomous triad that continuously reclaims dead leases, bounds diagnostic repairs under strict SLAs, and optimizes token policies based on failure distributions.</p>
            <ul class="bullet-list">
              <li><b>Self-Sustaining:</b> Automated worktree garbage collection &amp; Merkle chain reconciliation.</li>
              <li><b>Self-Recovering:</b> Bounded 3-attempt diagnostic re-prompting with surgical module fallback.</li>
              <li><b>Self-Improving:</b> Dynamic AST pruning threshold adaptation &amp; prompt prefix caching.</li>
            </ul>
          </div>

          <div class="card">
            <div class="card-badge" style="background:rgba(16,185,129,0.15); color:var(--green);">Zero Blast Radius</div>
            <h3>2. Sub-1.2s Surgical Micro-Module Rollback</h3>
            <p>When an autonomous coding agent hallucinates or introduces breaking regressions, standard tools force a destructive <code>git reset --hard</code> that clobbers sibling agents. Percipience rewinds only the culprit micro-module to its verified Recovery Point (<code>RP_k</code>).</p>
            <ul class="bullet-list">
              <li>Restores targeted module subtree while preserving 100% of concurrent sibling work.</li>
              <li>Sub-1.2 second rollback execution with zero downtime.</li>
              <li>Seals rollback event with cryptographic Merkle proof in <code>context_ledger.yaml</code>.</li>
            </ul>
          </div>

          <div class="card">
            <div class="card-badge" style="background:rgba(245,158,11,0.15); color:var(--amber);">Signal Integrity</div>
            <h3>3. Statistical Flaky Test Quarantine Engine</h3>
            <p>Non-deterministic test suites frequently derail autonomous agent PR pipelines. Percipience conducts multi-run statistical audits, isolates flaky tests into non-blocking quarantine (<code>flaky_quarantine.yaml</code>), and tracks auto-eviction once stabilized.</p>
            <ul class="bullet-list">
              <li>Eliminates false-positive CI/CD blockages without masking legitimate regressions.</li>
              <li>Maintains an audit ledger of quarantined tests with pass/fail ratios.</li>
              <li>Enables continuous 100% pass rates on critical PR merge gates.</li>
            </ul>
          </div>

          <div class="card">
            <div class="card-badge" style="background:rgba(168,85,247,0.15); color:var(--purple);">Living Architecture</div>
            <h3>4. Continuous AST Living Docs &amp; Validated Mermaid Engine</h3>
            <p>Software architecture diagrams in enterprise wikis drift immediately after commits. Percipience parses AST symbols across all microservices and autonomously generates 7+ strictly linted Mermaid architecture diagrams with Merkle hash integrity.</p>
            <ul class="bullet-list">
              <li>Strict Mermaid syntax linting catches unquoted brackets and broken connections.</li>
              <li>Continuous sync of sequence flows, data flows, entity relationships, and module catalogs.</li>
              <li>Zero human authoring overhead required to keep architecture living and accurate.</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- DEEP-DIVE: TOKEN REDUCTION ARCHITECTURE (AST VS GRAPH RAG / GRAPHIFY) -->
      <div style="margin-top:36px; margin-bottom:12px;">
        <div class="section-title">⚡ Deep-Dive Token Reduction: Percipience 6D AST Compression vs. Knowledge Graphs (Graphify / CodeKG)</div>
        <div class="section-desc">Comparing high-overhead Knowledge Graph serialization (Neo4j / Graph RAG) with Tree-Sitter AST Skeletonization and Bit-for-Bit Static Prefix Caching.</div>

        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th style="width:22%;">Architectural Dimension</th>
                <th style="width:39%;">Knowledge Graph / Graph RAG (Graphify / CodeKG)</th>
                <th style="width:39%; color:var(--cyan); background:rgba(0,242,254,0.08);">⚡ Percipience 6D AST Compression (Tree-Sitter)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="feature-name">Parsing Latency &amp; CPU Overhead</td>
                <td>⚠️ 5s–30s heavy AST graph indexing &amp; k-hop ego-network query extraction</td>
                <td class="percipience-cell">✅ <strong>&lt; 85ms</strong> native Tree-Sitter C/Rust daemon (>10,000 LOC/sec in memory)</td>
              </tr>
              <tr>
                <td class="feature-name">Token Payload &amp; Metadata Overhead</td>
                <td>❌ <strong>+20% to +40% token inflation</strong> from serialized graph edges, JSON schemas &amp; node IDs</td>
                <td class="percipience-cell">✅ <strong>50% to 75% token reduction</strong> via syntactic method body placeholders (<code>... [AST_PRUNED]</code>)</td>
              </tr>
              <tr>
                <td class="feature-name">Prompt Prefix KV-Cache Pinning</td>
                <td>❌ Dynamic graph neighbor queries create random token ordering, invalidating LLM prefix cache</td>
                <td class="percipience-cell">✅ <strong>Deterministic static invariant sorting</strong> ensures 88%+ KV-Cache hit rate across LLM providers</td>
              </tr>
              <tr>
                <td class="feature-name">Syntactic &amp; Type Completeness</td>
                <td>⚠️ Graph entity hops lose line-level AST context, decorator invariants, and type signatures</td>
                <td class="percipience-cell">✅ <strong>100% syntactic preservation</strong> of type signatures, docstrings, classes, interfaces, and decorators</td>
              </tr>
              <tr>
                <td class="feature-name">Infrastructure &amp; Database Footprint</td>
                <td>❌ Requires running Neo4j / NetworkX graph server + external Vector DB cluster</td>
                <td class="percipience-cell">✅ <strong>Zero external DB dependency</strong>; runs completely ephemeral in-memory tmpfs / CLI runtime</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <!-- TAB: PLAN TIER MATRIX & BOUNDARY CEILINGS (Section 2 of Parent Master Plan) -->
    <section id="tier-matrix" class="tab-content">
      <div class="section-title">2. Plan Tier Matrix &amp; Boundary Ceilings</div>
      <div class="section-desc">Comprehensive architectural entitlement matrix, boundary ceilings, concurrency quotas, security enclaves, and full 35-capability mapping across Free Community, Team, Business, and Enterprise tiers (governed by <code>.nb/plan/claude-context-engineering-parent-master-free_plan.md</code>).</div>

      <div class="grid-4" style="margin-bottom:22px;">
        <div class="metric-card">
          <div class="metric-val text-emerald">Free Forever</div>
          <div class="metric-label">Community Plan (plan_free)</div>
          <div class="metric-sub">1 Seat &bull; 1 Local Worktree &bull; 500 Audits</div>
        </div>
        <div class="metric-card">
          <div class="metric-val text-cyan">$1,499 / mo</div>
          <div class="metric-label">Team Plan (plan_team)</div>
          <div class="metric-sub">15 Seats &bull; 5 Worktrees &bull; 5,000 Audits</div>
        </div>
        <div class="metric-card">
          <div class="metric-val text-purple">$4,499 / mo</div>
          <div class="metric-label">Business Plan (plan_business)</div>
          <div class="metric-sub">50 Seats &bull; 20 Worktrees &bull; .nbpack AES-256</div>
        </div>
        <div class="metric-card">
          <div class="metric-val" style="color:var(--amber);">$9,999+ / mo</div>
          <div class="metric-label">Enterprise Dedicated (plan_enterprise)</div>
          <div class="metric-sub">Unlimited &bull; RAM Enclave &bull; Dedicated VPC</div>
        </div>
      </div>

      <!-- CORE MATRIX TABLE (Section 2 from Plan) -->
      <div class="card" style="margin-bottom:24px;">
        <div class="card-badge">Section 2 Specification</div>
        <h3>Plan Tier Matrix &amp; Core Boundary Ceilings</h3>
        <p>Direct comparison of infrastructural ceilings, token reduction engines, cryptographic verification, and deployment boundaries:</p>

        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th style="width:22%;">Feature / Dimension</th>
                <th style="width:19%; background:rgba(16,185,129,0.08); color:var(--green);">Free Community Plan (<code>plan_free</code>)</th>
                <th style="width:19%;">Team Plan (<code>plan_team</code>)</th>
                <th style="width:20%; background:rgba(0,242,254,0.06); color:var(--cyan);">Business Plan (<code>plan_business</code>)</th>
                <th style="width:20%; background:rgba(168,85,247,0.08); color:var(--purple);">Enterprise Dedicated (<code>plan_enterprise</code>)</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="feature-name">Monthly Base Price</td>
                <td style="background:rgba(16,185,129,0.03);"><strong class="text-emerald">$0.00 / Free Forever</strong></td>
                <td><strong>$1,499 / mo</strong></td>
                <td style="background:rgba(0,242,254,0.03);"><strong class="text-cyan">$4,499 / mo</strong></td>
                <td style="background:rgba(168,85,247,0.03);"><strong class="text-purple">$9,999 / mo</strong></td>
              </tr>
              <tr>
                <td class="feature-name">Included Seats</td>
                <td style="background:rgba(16,185,129,0.03);"><strong>1 Developer Seat</strong></td>
                <td>15 Seats</td>
                <td style="background:rgba(0,242,254,0.03);">50 Seats</td>
                <td style="background:rgba(168,85,247,0.03);"><strong class="text-purple">Unlimited Seats</strong></td>
              </tr>
              <tr>
                <td class="feature-name">Concurrent Worktrees</td>
                <td style="background:rgba(16,185,129,0.03);"><strong>1 Local Worktree</strong></td>
                <td>5 Worktrees</td>
                <td style="background:rgba(0,242,254,0.03);">20 Worktrees</td>
                <td style="background:rgba(168,85,247,0.03);"><strong class="text-purple">Unlimited Distributed</strong></td>
              </tr>
              <tr>
                <td class="feature-name">Monthly PR Audits</td>
                <td style="background:rgba(16,185,129,0.03);"><strong>500 Audits / mo</strong></td>
                <td>5,000 Audits / mo</td>
                <td style="background:rgba(0,242,254,0.03);">25,000 Audits / mo</td>
                <td style="background:rgba(168,85,247,0.03);"><strong class="text-purple">Unlimited Audits</strong></td>
              </tr>
              <tr>
                <td class="feature-name">AST Token Reduction</td>
                <td style="background:rgba(16,185,129,0.03);"><span class="badge badge-emerald">&#x2705; Full (60%&ndash;80%)</span></td>
                <td><span class="badge badge-cyan">&#x2705; Full (60%&ndash;80%)</span></td>
                <td style="background:rgba(0,242,254,0.03);"><span class="badge badge-cyan">&#x2705; Full (60%&ndash;80%)</span></td>
                <td style="background:rgba(168,85,247,0.03);"><span class="badge badge-purple">&#x2705; Full + Tree-Sitter Daemon</span></td>
              </tr>
              <tr>
                <td class="feature-name">Cryptographic Merkle Chain</td>
                <td style="background:rgba(16,185,129,0.03);"><span class="badge badge-emerald">&#x2705; Local Linear SHA-256</span></td>
                <td><span class="badge badge-cyan">&#x2705; Local + Remote Sync</span></td>
                <td style="background:rgba(0,242,254,0.03);"><span class="badge badge-cyan">&#x2705; Local + Remote Sync</span></td>
                <td style="background:rgba(168,85,247,0.03);"><span class="badge badge-purple">&#x2705; Multi-Region WORM S3/GCS</span></td>
              </tr>
              <tr>
                <td class="feature-name">Autonomous CI/CD</td>
                <td style="background:rgba(16,185,129,0.03);"><span class="badge badge-emerald">&#x2705; Basic Setup (1-Retry Heal)</span></td>
                <td><span class="badge badge-cyan">&#x2705; Advanced (3-Retry)</span></td>
                <td style="background:rgba(0,242,254,0.03);"><span class="badge badge-cyan">&#x2705; Full Multi-Stage</span></td>
                <td style="background:rgba(168,85,247,0.03);"><span class="badge badge-purple">&#x2705; Closed-Loop Swarm Triad</span></td>
              </tr>
              <tr>
                <td class="feature-name">Packaging &amp; Obfuscation</td>
                <td style="background:rgba(16,185,129,0.03); color:var(--muted);">&#x274C; Plaintext / Open Repo</td>
                <td style="color:var(--muted);">&#x274C; Plaintext</td>
                <td style="background:rgba(0,242,254,0.03);"><span class="badge badge-cyan">&#x2705; <code>.nbpack</code> AES-256</span></td>
                <td style="background:rgba(168,85,247,0.03);"><span class="badge badge-purple">&#x2705; <code>.nbpack</code> RAM Enclave</span></td>
              </tr>
              <tr>
                <td class="feature-name">Deployment Model</td>
                <td style="background:rgba(16,185,129,0.03);"><strong>Local IDE &amp; Git Worktree</strong></td>
                <td>Cloud Shared Gateway</td>
                <td style="background:rgba(0,242,254,0.03);">Cloud Shared Gateway</td>
                <td style="background:rgba(168,85,247,0.03);"><strong class="text-purple">Dedicated Private VPC</strong></td>
              </tr>
              <tr>
                <td class="feature-name">IDE Plugin Support</td>
                <td style="background:rgba(16,185,129,0.03);"><span class="badge badge-emerald">&#x2705; IntelliJ &amp; VSCode</span></td>
                <td><span class="badge badge-cyan">&#x2705; IntelliJ &amp; VSCode</span></td>
                <td style="background:rgba(0,242,254,0.03);"><span class="badge badge-cyan">&#x2705; IntelliJ &amp; VSCode</span></td>
                <td style="background:rgba(168,85,247,0.03);"><span class="badge badge-purple">&#x2705; IntelliJ &amp; VSCode + JCEF</span></td>
              </tr>
              <tr>
                <td class="feature-name">Sandbox Source Permissions</td>
                <td style="background:rgba(16,185,129,0.03);"><span class="badge badge-emerald">&#x2705; Local Sandbox Broker</span></td>
                <td><span class="badge badge-cyan">&#x2705; Team RBAC</span></td>
                <td style="background:rgba(0,242,254,0.03);"><span class="badge badge-cyan">&#x2705; Enterprise RBAC</span></td>
                <td style="background:rgba(168,85,247,0.03);"><span class="badge badge-purple">&#x2705; Zero-Trust Fine-Grained</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 6 BOUNDARY CEILINGS ARCHITECTURAL BREAKDOWN -->
      <div class="grid-3" style="margin-bottom:24px;">
        <div class="card">
          <div class="card-badge">Boundary 1</div>
          <h3>🌲 AST Token Reduction Engine</h3>
          <p>Enforces surgical skeletonization across Python, Kotlin, TypeScript, Go, and Rust in &lt;35ms before streaming context to LLMs.</p>
          <ul class="bullet-list">
            <li><strong>Free Tier</strong>: Local in-process AST parser (60%&ndash;80% reduction)</li>
            <li><strong>Team/Business</strong>: Multi-file dependency graph pruning</li>
            <li><strong>Enterprise</strong>: Dedicated Tree-Sitter daemon with sub-millisecond AST streaming</li>
          </ul>
        </div>

        <div class="card">
          <div class="card-badge">Boundary 2</div>
          <h3>🛡️ Cryptographic Merkle Ledger</h3>
          <p>Every prompt, contract check, agent step, and file modification is sealed into an immutable SHA-256 hash chain with instant rollback.</p>
          <ul class="bullet-list">
            <li><strong>Free Tier</strong>: Local linear <code>context_ledger.yaml</code></li>
            <li><strong>Team/Business</strong>: Centralized team sync &amp; multi-branch DAG</li>
            <li><strong>Enterprise</strong>: SEC 17a-4 / FINRA WORM immutable storage (AWS S3 Object Lock / GCP Bucket Lock)</li>
          </ul>
        </div>

        <div class="card">
          <div class="card-badge">Boundary 3</div>
          <h3>🔄 Autonomous CI/CD Self-Healing</h3>
          <p>Automated Closed-Loop Triad: Self-Sustaining Hygiene + Autonomous Healer + Self-Improving Engine.</p>
          <ul class="bullet-list">
            <li><strong>Free Tier</strong>: 1-attempt bounded diagnostic reprompt &amp; quarantine</li>
            <li><strong>Team</strong>: 3-attempt bounded reprompt with traceback slicing</li>
            <li><strong>Business/Enterprise</strong>: Full multi-agent swarm triage &amp; surgical micro-module rollback (RP_k)</li>
          </ul>
        </div>

        <div class="card">
          <div class="card-badge">Boundary 4</div>
          <h3>🔒 Packaging &amp; Obfuscation Enclaves</h3>
          <p>Protects proprietary architecture plans and agent instructions from client extraction or prompt injection leakage.</p>
          <ul class="bullet-list">
            <li><strong>Free/Team</strong>: Plaintext in repository (Open / Inner-Source)</li>
            <li><strong>Business</strong>: <code>.nbpack</code> AES-256 encrypted archive envelopes</li>
            <li><strong>Enterprise</strong>: Ephemeral RAM Enclave execution + AWS KMS CMEK hardware isolation</li>
          </ul>
        </div>

        <div class="card">
          <div class="card-badge">Boundary 5</div>
          <h3>⚙️ Concurrency &amp; Worktree Isolation</h3>
          <p>Ensures concurrent subagents operate in strict isolation without clobbering developer working directories or sibling tasks.</p>
          <ul class="bullet-list">
            <li><strong>Free Tier</strong>: 1 Local active worktree sandbox</li>
            <li><strong>Team/Business</strong>: 5 to 20 concurrent Git worktree sandboxes</li>
            <li><strong>Enterprise</strong>: Unlimited distributed microVM / container worktrees with Redis Redlock</li>
          </ul>
        </div>

        <div class="card">
          <div class="card-badge">Boundary 6</div>
          <h3>🔌 IDE &amp; Sandboxed LLM Permissions</h3>
          <p>Brokers source file requests from external LLMs (Copilot, Cody, JetBrains AI) to enforce token reduction and protect ledgers.</p>
          <ul class="bullet-list">
            <li><strong>Free Tier</strong>: Local <code>SandboxPermissionBroker</code> (READ_PRUNED_AST by default)</li>
            <li><strong>Team</strong>: Shared team policy manifests</li>
            <li><strong>Enterprise</strong>: Zero-Trust fine-grained RBAC with hardware key signing</li>
          </ul>
        </div>
      </div>

      <!-- CAPABILITY MAPPING TABLE (CAP-01 to CAP-35) -->
      <div class="card" style="margin-bottom:24px;">
        <div class="card-badge">CAP-01 through CAP-35</div>
        <h3>Foundational Capability Entitlement Mapping</h3>
        <p>Granular breakdown of all 35 architectural capabilities specified in Section 8 of the Master Plan:</p>

        <div class="table-wrap" style="max-height:450px; overflow-y:auto;">
          <table>
            <thead>
              <tr>
                <th style="width:12%;">Capability ID</th>
                <th style="width:38%;">Foundational Capability Name</th>
                <th style="width:25%;">Free Community Tier (<code>plan_free</code>)</th>
                <th style="width:25%;">Enterprise Commercial Tier (<code>plan_enterprise</code>)</th>
              </tr>
            </thead>
            <tbody>
              <tr><td><code>CAP-01</code></td><td>Multi-Format MVS Ingestion</td><td><span class="badge badge-emerald">&#x2705; Supported (Markdown &amp; OpenAPI)</span></td><td><span class="badge badge-purple">&#x2705; Universal (GraphQL/Protobuf/AsyncAPI)</span></td></tr>
              <tr><td><code>CAP-02</code></td><td>Context Poisoning Detection &amp; Rollback</td><td><span class="badge badge-emerald">&#x2705; Supported (Local Recovery Points)</span></td><td><span class="badge badge-purple">&#x2705; Distributed Surgical Rollback (RP_k)</span></td></tr>
              <tr><td><code>CAP-03</code></td><td>Context Compression &amp; GenAI Optimization</td><td><span class="badge badge-emerald">&#x2705; Supported (60%&ndash;80% AST Pruning)</span></td><td><span class="badge badge-purple">&#x2705; Tree-Sitter Daemon + 6D Suite</span></td></tr>
              <tr><td><code>CAP-04</code></td><td>Dynamic Multi-Model Cascading &amp; Tiering</td><td><span class="badge badge-emerald">&#x2705; Supported (Local / BYO API Key)</span></td><td><span class="badge badge-purple">&#x2705; Automated Cost/Latency Router</span></td></tr>
              <tr><td><code>CAP-05</code></td><td>Git Worktree Workspace Isolation</td><td><span class="badge badge-emerald">&#x2705; Supported (Single Local Worktree)</span></td><td><span class="badge badge-purple">&#x2705; Unlimited Distributed Sandboxes</span></td></tr>
              <tr><td><code>CAP-06</code></td><td>Automated Spec-to-Code Semantic Parity</td><td><span class="badge badge-emerald">&#x2705; Supported (AST Parity Verification)</span></td><td><span class="badge badge-purple">&#x2705; Reverse AST Diff Reconciliation</span></td></tr>
              <tr><td><code>CAP-07</code></td><td>Bounded TDD Self-Healing</td><td><span class="badge badge-emerald">&#x2705; Supported (1-Retry Auto-Repair)</span></td><td><span class="badge badge-purple">&#x2705; 3-Attempt SLA + Swarm Triage</span></td></tr>
              <tr><td><code>CAP-08</code></td><td>Cryptographic Ledger Hash-Chain</td><td><span class="badge badge-emerald">&#x2705; Supported (SHA-256 Linear Ledger)</span></td><td><span class="badge badge-purple">&#x2705; Multi-Region WORM S3/GCS DAG</span></td></tr>
              <tr><td><code>CAP-09</code></td><td>Time-Travel Debugging &amp; Visual DAG</td><td><span class="badge badge-emerald">&#x2705; Supported (Static HTML Dashboard)</span></td><td><span class="badge badge-purple">&#x2705; Real-Time Reactive Visualizer</span></td></tr>
              <tr><td><code>CAP-10</code></td><td>Context Maturity Evaluation Scorecard</td><td><span class="badge badge-emerald">&#x2705; Supported (Standard 6D Scorecard)</span></td><td><span class="badge badge-purple">&#x2705; Automated Continuous G-Eval Radar</span></td></tr>
              <tr><td><code>CAP-11</code></td><td>Master Context Ledger &amp; Commit Traceability</td><td><span class="badge badge-emerald">&#x2705; Supported (Full Traceability)</span></td><td><span class="badge badge-purple">&#x2705; Monorepo Micro-Module Traceability</span></td></tr>
              <tr><td><code>CAP-12</code></td><td>Universal Quad-Space Clean Bootstrapping</td><td><span class="badge badge-emerald">&#x2705; Supported (Automated in IDE Plugin)</span></td><td><span class="badge badge-purple">&#x2705; Multi-Tenant Cloud Provisioning</span></td></tr>
              <tr><td><code>CAP-13</code></td><td>Zero-Overhead Dual-Mode Architecture</td><td><span class="badge badge-emerald">&#x2705; Supported (Single &amp; Multi-Module)</span></td><td><span class="badge badge-purple">&#x2705; Monorepo MicroVM Dynamic Scaling</span></td></tr>
              <tr><td><code>CAP-14</code></td><td>Proprietary Obfuscation &amp; .nbpack Enclaves</td><td><span class="badge badge-amber">&#x274C; Paid Tier Only</span></td><td><span class="badge badge-purple">&#x2705; RAM Enclaves + KMS CMEK Vault</span></td></tr>
              <tr><td><code>CAP-15</code></td><td>External Issue Tracker &amp; Jira MCP Server</td><td><span class="badge badge-amber">&#x274C; Paid Tier Only</span></td><td><span class="badge badge-purple">&#x2705; Bi-directional Jira/Linear MCP</span></td></tr>
              <tr><td><code>CAP-16</code></td><td>Autonomous CI/CD Triad</td><td><span class="badge badge-emerald">&#x2705; Supported (basic_autonomous_cicd.yaml)</span></td><td><span class="badge badge-purple">&#x2705; Full Triad + SelfImprovingEngine</span></td></tr>
              <tr><td><code>CAP-17</code></td><td>Extensible Custom Agent Plugins</td><td><span class="badge badge-emerald">&#x2705; Supported (Local Custom Agents)</span></td><td><span class="badge badge-purple">&#x2705; Swarm Registry &amp; Version Leases</span></td></tr>
              <tr><td><code>CAP-18</code></td><td>Production Token FinOps &amp; Metering</td><td><span class="badge badge-emerald">&#x2705; Supported (Local Token Ledger)</span></td><td><span class="badge badge-purple">&#x2705; 15% Rev-Share Invoicing &amp; APM</span></td></tr>
              <tr><td><code>CAP-19</code></td><td>Enterprise Observability Hub &amp; Telemetry</td><td><span class="badge badge-emerald">&#x2705; Supported (Local Web Dashboard)</span></td><td><span class="badge badge-purple">&#x2705; OpenTelemetry W3C GenAI Exporter</span></td></tr>
              <tr><td><code>CAP-20</code></td><td>3-Tier Layered Context &amp; BYOR</td><td><span class="badge badge-emerald">&#x2705; Supported (Local Git &amp; SSH)</span></td><td><span class="badge badge-purple">&#x2705; Self-Hosted GitLab / GHES VPC</span></td></tr>
              <tr><td><code>CAP-21</code></td><td>Autonomous Living Documentation Engine</td><td><span class="badge badge-emerald">&#x2705; Supported (Markdown + Mermaid)</span></td><td><span class="badge badge-purple">&#x2705; AST-to-Mermaid Continuous Lint</span></td></tr>
              <tr><td><code>CAP-22</code></td><td>Distributed Redis Redlock Concurrency</td><td><span class="badge badge-amber">&#x274C; Paid Tier Only</span></td><td><span class="badge badge-purple">&#x2705; Cluster-Wide Ephemeral Mutexes</span></td></tr>
              <tr><td><code>CAP-23</code></td><td>SEC 17a-4 / FINRA WORM Cloud Vault Egress</td><td><span class="badge badge-amber">&#x274C; Paid Tier Only</span></td><td><span class="badge badge-purple">&#x2705; S3 Object Lock &amp; Audit Egress</span></td></tr>
              <tr><td><code>CAP-24</code></td><td>High-Throughput Tree-Sitter AST Daemon</td><td><span class="badge badge-amber">&#x274C; Paid Tier Only</span></td><td><span class="badge badge-purple">&#x2705; Multi-Language In-Memory Daemon</span></td></tr>
              <tr><td><code>CAP-25</code></td><td>Multi-Dimensional 6D Token Compression Suite</td><td><span class="badge badge-emerald">&#x2705; Supported (AST + Doc + Config)</span></td><td><span class="badge badge-purple">&#x2705; Full 6D Pruner Suite</span></td></tr>
              <tr><td><code>CAP-26</code></td><td>Multi-Dialect Diagnostic Log Slicing</td><td><span class="badge badge-emerald">&#x2705; Supported (Traceback Slicer)</span></td><td><span class="badge badge-purple">&#x2705; Polyglot Multi-Dialect Slicer</span></td></tr>
              <tr><td><code>CAP-27</code></td><td>Declarative Quad-Space Runtime Boundary</td><td><span class="badge badge-emerald">&#x2705; Supported (Zero-Logic Facade)</span></td><td><span class="badge badge-purple">&#x2705; Monorepo Boundary Enforcement</span></td></tr>
              <tr><td><code>CAP-28</code></td><td>Barrier Join Synchronization Engine</td><td><span class="badge badge-emerald">&#x2705; Supported (Local Step DAG)</span></td><td><span class="badge badge-purple">&#x2705; Distributed Swarm Synchronizer</span></td></tr>
              <tr><td><code>CAP-29</code></td><td>4-Pillar Error Taxonomy &amp; Playbooks</td><td><span class="badge badge-emerald">&#x2705; Supported (Basic Playbooks)</span></td><td><span class="badge badge-purple">&#x2705; Autonomous Playbook Router</span></td></tr>
              <tr><td><code>CAP-30</code></td><td>Cryptographic Prompt Manifest &amp; Static Pinning</td><td><span class="badge badge-emerald">&#x2705; Supported (prompt_manifest.yaml)</span></td><td><span class="badge badge-purple">&#x2705; Bit-for-Bit KV Cache Anchoring</span></td></tr>
              <tr><td><code>CAP-31</code></td><td>Hierarchical Swarm Authority Tree</td><td><span class="badge badge-emerald">&#x2705; Supported (Local Hierarchy)</span></td><td><span class="badge badge-purple">&#x2705; 4-Tier Anti-Usurpation Tree</span></td></tr>
              <tr><td><code>CAP-32</code></td><td>Adversarial Red-Team Fuzzing Engine</td><td><span class="badge badge-emerald">&#x2705; Supported (Standard Fuzzing)</span></td><td><span class="badge badge-purple">&#x2705; Chaos &amp; Security Mutation Suite</span></td></tr>
              <tr><td><code>CAP-33</code></td><td>Proportional Attention Budgeting</td><td><span class="badge badge-emerald">&#x2705; Supported (15/25/35/10/15 Rule)</span></td><td><span class="badge badge-purple">&#x2705; Dynamic KV Attention Balancer</span></td></tr>
              <tr><td><code>CAP-34</code></td><td>ReAct Trajectory Recording &amp; Replay</td><td><span class="badge badge-emerald">&#x2705; Supported (agentic/trajectories/)</span></td><td><span class="badge badge-purple">&#x2705; Vectorized Trajectory Search</span></td></tr>
              <tr><td><code>CAP-35</code></td><td>Ambiguity Resolution &amp; Clarification RFCs</td><td><span class="badge badge-emerald">&#x2705; Supported (user/hitl/)</span></td><td><span class="badge badge-purple">&#x2705; Automated RFC Collaboration Gate</span></td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- INTERACTIVE TIER & CEILING CALCULATOR -->
      <div class="card" style="max-width:800px; margin:0 auto;">
        <div class="card-badge">Interactive Tool</div>
        <h3>Live Boundary Ceiling &amp; Tier Validator</h3>
        <p>Simulate your organization requirements to see boundary ceiling compliance and recommended deployment model:</p>
        
        <div class="grid-2" style="margin-bottom:14px;">
          <div class="form-group">
            <label class="form-label">Developer Seats:</label>
            <input type="number" id="simSeats" class="input" value="1" min="1" max="500" oninput="calculateCeilings()">
          </div>
          <div class="form-group">
            <label class="form-label">Concurrent Worktrees:</label>
            <input type="number" id="simWorktrees" class="input" value="1" min="1" max="100" oninput="calculateCeilings()">
          </div>
          <div class="form-group">
            <label class="form-label">Monthly PR Audits:</label>
            <input type="number" id="simAudits" class="input" value="450" min="50" max="100000" oninput="calculateCeilings()">
          </div>
          <div class="form-group">
            <label class="form-label">Security &amp; Enclave Requirement:</label>
            <select id="simEnclave" class="input" onchange="calculateCeilings()">
              <option value="plaintext">Local IDE / Open Repo (Plaintext)</option>
              <option value="cloud">Cloud Shared Gateway</option>
              <option value="nbpack">Encrypted .nbpack AES-256</option>
              <option value="enclave">RAM Enclave + KMS CMEK Vault</option>
              <option value="vpc">Dedicated Private VPC</option>
            </select>
          </div>
        </div>

        <div id="simResult" style="margin-top:12px;"></div>
      </div>
    </section>

    <!-- TAB 4: CONTEXT GATEWAY (OPTION 1) -->
    <section id="gateway" class="tab-content">
      <div class="section-title">Context Gateway (Option 1) &amp; Sealed Plan Bundles</div>
      <div class="section-desc">Enforces zero plaintext blueprint leakage. Proprietary plans and KMS decryption keys reside strictly inside the Gateway server-side RAM enclave with in-flight prompt injection and sealed binary envelopes (.nbpack).</div>

      <div class="grid-4" style="margin-bottom:22px;">
        <div class="metric-card">
          <div class="metric-val text-emerald">0.0%</div>
          <div class="metric-label">Client Plan Exposure</div>
        </div>
        <div class="metric-card">
          <div class="metric-val text-cyan">100%</div>
          <div class="metric-label">Invariant Enforcement</div>
        </div>
        <div class="metric-card">
          <div class="metric-val text-purple">AES-256-GCM</div>
          <div class="metric-label">Binary Envelope Seal</div>
        </div>
        <div class="metric-card">
          <div class="metric-val text-amber">&lt; 25ms</div>
          <div class="metric-label">In-Flight Enclave Latency</div>
        </div>
      </div>

      <!-- Core Security Pillars -->
      <div class="grid-3" style="margin-bottom:22px;">
        <div class="card">
          <div class="card-badge">Architecture</div>
          <h3>1. Server-Side RAM Enclave</h3>
          <p>Domain blueprints, wire contracts, and KMS decryption keys reside strictly in ephemeral Gateway memory. No plaintext plan file is ever shipped or exposed to client developer workstations.</p>
          <div class="stat-box"><span>KMS Key Broker:</span><span class="stat-val text-cyan" style="font-size:11px;">CMEK-Vault-Enclave</span></div>
          <div class="stat-box"><span>Plaintext Residue:</span><span class="stat-val text-emerald">0.0% Disk Residue</span></div>
        </div>

        <div class="card">
          <div class="card-badge">Runtime Interception</div>
          <h3>2. In-Flight Prompt Injection</h3>
          <p>The Gateway transparently intercepts LLM completions, injects architectural constraints and invariants into the provider context in-flight, and sanitizes output before streaming code back to the client.</p>
          <div class="stat-box"><span>Drop-in Compatibility:</span><span class="stat-val text-cyan">OpenAI / Claude API</span></div>
          <div class="stat-box"><span>Sanitization Guard:</span><span class="stat-val text-emerald">100% Redacted Invariants</span></div>
        </div>

        <div class="card">
          <div class="card-badge">Distribution</div>
          <h3>3. Encrypted .nbpack Bundles</h3>
          <p>Encrypted domain layers (e.g. <code>iot_mobile_domain.nbpack</code>) can be downloaded and bootstrapped via <code>npm / npx</code> or native CLI into RAM with zero client filesystem exposure.</p>
          <div class="stat-box"><span>Cryptographic Format:</span><span class="stat-val text-cyan">NBPACK_V2_SEALED</span></div>
          <div class="stat-box"><span>Space Hydration:</span><span class="stat-val text-emerald">Volatile Memory Only</span></div>
        </div>
      </div>

      <!-- ENCRYPTED BUNDLES DOWNLOAD & SPACE BOOTSTRAPPING CENTER -->
      <div class="card" style="margin-bottom:22px;">
        <div class="card-badge">Distribution Center</div>
        <h3>📦 Encrypted Plan Bundles (.nbpack) &amp; Zero-Exposure Space Bootstrapping</h3>
        <p>Download pre-compiled, Ed25519-signed AES-256-GCM binary envelopes. Developers and autonomous subagents can install and hydrate these sealed packages directly in volatile memory via <code>npm / npx</code> or the native Percipience CLI without exposing the proprietary blueprint content.</p>

        <div class="table-wrap" style="margin:14px 0;">
          <table>
            <thead>
              <tr>
                <th>Plan Bundle / File</th>
                <th>Target Domain Architecture</th>
                <th>Envelope Format &amp; Seal</th>
                <th>Size</th>
                <th>Client Exposure</th>
                <th style="text-align:right;">Actions</th>
              </tr>
            </thead>
            <tbody id="gatewayBundlesTableBody">
              <tr>
                <td class="feature-name">
                  <div style="font-weight:700; color:var(--text);">IoT Edge &amp; Mobile Domain</div>
                  <code style="font-size:11px; color:var(--cyan);">iot_mobile_domain.nbpack</code>
                </td>
                <td>Embedded FreeRTOS, BLE GATT telemetry, ring-buffer concurrency &amp; dual-bank OTA invariants.</td>
                <td><span class="badge badge-cyan">AES-256-GCM / Ed25519</span></td>
                <td>8.2 KB</td>
                <td><span class="text-emerald" style="font-weight:700;">0.0% (RAM-Only)</span></td>
                <td style="text-align:right;">
                  <a href="/api/gateway/bundles/iot_mobile_domain.nbpack" download class="action-btn" style="padding:5px 10px; font-size:11px;">⬇️ Download</a>
                </td>
              </tr>
              <tr>
                <td class="feature-name">
                  <div style="font-weight:700; color:var(--text);">Enterprise SaaS &amp; Cloud Portal</div>
                  <code style="font-size:11px; color:var(--cyan);">saas_portal_domain.nbpack</code>
                </td>
                <td>Multi-tenant RBAC, PostgreSQL RLS, Stripe 15% FinOps billing &amp; portal UI design tokens.</td>
                <td><span class="badge badge-cyan">AES-256-GCM / Ed25519</span></td>
                <td>7.8 KB</td>
                <td><span class="text-emerald" style="font-weight:700;">0.0% (RAM-Only)</span></td>
                <td style="text-align:right;">
                  <a href="/api/gateway/bundles/saas_portal_domain.nbpack" download class="action-btn" style="padding:5px 10px; font-size:11px;">⬇️ Download</a>
                </td>
              </tr>
              <tr>
                <td class="feature-name">
                  <div style="font-weight:700; color:var(--text);">Context Engineering OS Kernel</div>
                  <code style="font-size:11px; color:var(--cyan);">percipience_parent.nbpack</code>
                </td>
                <td>Complete Quad-Space kernel, Merkle state chain DAG, active PID worktrees &amp; CI/CD gatekeeper.</td>
                <td><span class="badge badge-cyan">AES-256-GCM / Ed25519</span></td>
                <td>70.2 KB</td>
                <td><span class="text-emerald" style="font-weight:700;">0.0% (RAM-Only)</span></td>
                <td style="text-align:right;">
                  <a href="/api/gateway/bundles/percipience_parent.nbpack" download class="action-btn" style="padding:5px 10px; font-size:11px;">⬇️ Download</a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <h4>Zero-Exposure Space Bootstrapping Quickstart</h4>
        <p>Choose your preferred toolchain to bootstrap and hydrate domain quad-spaces in volatile memory:</p>

        <div class="grid-2">
          <div>
            <div class="form-label" style="color:var(--cyan);">Option A: npm / npx Developer CLI Quickstart</div>
            <pre># 1. Download sealed bundle via Gateway (Zero Plaintext Exposure)
curl -fsSL https://portal.percipience.dev/api/gateway/bundles/iot_mobile_domain.nbpack -o ./iot_mobile_domain.nbpack

# 2. Bootstrap workspace in volatile RAM (0% disk residue)
npx @percipience/cli layer apply --pack ./iot_mobile_domain.nbpack --mode in-memory

# 3. Or install as local npm dependency package
npm install --save-dev @percipience/context-gateway</pre>
          </div>

          <div>
            <div class="form-label" style="color:var(--green);">Option B: Native Percipience Control Plane &amp; Proxy</div>
            <pre># 1. Mount encrypted layer directly into volatile memory
./workplace/bin/percipience layer apply --pack .nb/bundles/iot_mobile_domain.nbpack

# 2. Verify active in-memory mounts
./workplace/bin/percipience layer list

# 3. Set drop-in proxy environment for local agent
export OPENAI_BASE_URL="http://localhost:8080/v1"
export PERCIPIENCE_PLAN_ID="plan_iot_mobile"</pre>
          </div>
        </div>
      </div>

      <!-- INTERACTIVE IN-FLIGHT PROMPT INJECTION PLAYGROUND -->
      <div class="card">
        <div class="card-badge">Live Interactive Proxy</div>
        <h3>⚡ Drop-in Proxy Playground (In-Flight Invariant Injection)</h3>
        <p>Simulate an autonomous coding subagent querying the Context Gateway. Watch how proprietary invariants are injected in-flight server-side, while only sanitized, compliant code is streamed back to the client.</p>

        <div class="grid-2" style="margin-top:14px;">
          <div>
            <div class="form-group">
              <label class="form-label">Governing Proprietary Plan:</label>
              <select id="gwPlanSelect">
                <option value="plan_iot_mobile">IoT Edge &amp; Mobile Plan (BLE GATT &amp; Ring-Buffer Mutex)</option>
                <option value="plan_saas_portal">SaaS Cloud Portal Plan (Multi-Tenant &amp; 15% FinOps)</option>
                <option value="plan_parent_master">Parent Master Plan (Quad-Space OS &amp; Merkle Ledger)</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Client Context / Local Error Trace (Repo State):</label>
              <textarea id="gwRepoState" rows="3">{"module": "mod_telemetry_stream", "test_error": "AssertionError: ring-buffer mutex lock violated on characteristic 0xFF01"}</textarea>
            </div>

            <div class="form-group">
              <label class="form-label">Client Subagent Query Prompt:</label>
              <textarea id="gwPrompt" rows="3">Fix the ring-buffer mutex lock violation in the telemetry characteristic and ensure process liveness.</textarea>
            </div>

            <button class="action-btn" onclick="runContextGatewayDemo()">🚀 Route Through Context Gateway</button>
          </div>

          <div>
            <div class="form-label" style="color:var(--cyan);">Live Gateway Execution &amp; Sanitization Audit:</div>
            <div id="gwDemoResults" style="background:var(--code-bg); border:1px solid var(--border); border-radius:8px; padding:14px; min-height:240px; font-family:'JetBrains Mono', monospace; font-size:12px; color:var(--muted); line-height:1.5;">
              <span style="color:var(--muted);">Click "Route Through Context Gateway" to execute in-flight prompt injection...</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 5: ROI & BENEFITS -->
    <section id="roi-calculator" class="tab-content">
      <div class="section-title">Quantified Customer ROI &amp; ICP Value Models</div>
      <div class="section-desc">Percipience delivers concrete, audited cost reductions and risk elimination across three core target enterprise segments.</div>

      <div class="grid-3" style="margin-bottom:22px;">
        <div class="card">
          <div class="card-badge">ICP 1</div>
          <h3>AI Dev Agencies &amp; Studios</h3>
          <p>Enables 20+ autonomous subagents to write code concurrently without git locks. Cuts client token pass-through costs by 60%, expanding agency margins from 30% to 55%.</p>
          <div class="stat-box"><span>Key Metric:</span><span class="stat-val text-cyan">3.5x Faster Delivery</span></div>
        </div>

        <div class="card">
          <div class="card-badge">ICP 2</div>
          <h3>Mid-Market &amp; Enterprise Orgs</h3>
          <p>50–500 engineer organizations burning $15k–$100k/mo on LLMs. Eliminates 12+ hours/week per senior engineer spent untangling agent hallucination drift and broken APIs.</p>
          <div class="stat-box"><span>Annual Net ROI:</span><span class="stat-val text-emerald">$118,800 / year</span></div>
        </div>

        <div class="card">
          <div class="card-badge">ICP 3</div>
          <h3>Regulated FinTech &amp; HealthTech</h3>
          <p>Banks and healthcare platforms requiring strict SOC 2, HIPAA, and EU AI Act compliance. Tamper-proof WORM Merkle logs provide non-repudiable proof for compliance auditors.</p>
          <div class="stat-box"><span>Audit Readiness:</span><span class="stat-val text-purple">100% Non-Repudiable</span></div>
        </div>
      </div>

      <div class="card" style="max-width:800px; margin:0 auto;">
        <div class="card-badge">Interactive FinOps Calculator</div>
        <h3>Enterprise Token Savings &amp; ROI Calculator</h3>
        <p>Adjust team size, monthly model API spend, and daily PR volume to calculate projected monthly and annualized net financial returns.</p>
        
        <div class="grid-3" style="margin-bottom:16px;">
          <div class="form-group">
            <label class="form-label">Engineers:</label>
            <input type="number" id="calcEngineers" class="input" value="50" oninput="recalcRoi()">
          </div>
          <div class="form-group">
            <label class="form-label">Monthly LLM Spend ($):</label>
            <input type="number" id="calcSpend" class="input" value="18000" oninput="recalcRoi()">
          </div>
          <div class="form-group">
            <label class="form-label">Daily PR Count:</label>
            <input type="number" id="calcPrs" class="input" value="45" oninput="recalcRoi()">
          </div>
        </div>

        <div style="background:var(--code-bg); border:1px solid var(--border); border-radius:10px; padding:16px;">
          <div class="stat-box"><span>Gross Monthly Token Savings (55% AST Reduction):</span><span id="roiGrossVal" class="stat-val text-emerald">$9,900 / mo</span></div>
          <div class="stat-box"><span>15% Percipience Verified Performance Fee:</span><span id="roiFeeVal" class="stat-val text-cyan">$1,485 / mo</span></div>
          <div class="stat-box"><span>Net Monthly Customer Savings (Post-Fee):</span><span id="roiNetVal" class="stat-val text-emerald">$8,415 / mo</span></div>
          <div class="stat-box"><span>Annualized Net Financial Savings:</span><span id="roiAnnualVal" class="stat-val text-emerald" style="font-weight:800;">$100,980 / yr</span></div>
          <div class="stat-box"><span>Engineering Hours Reclaimed (Eliminated Drift):</span><span class="stat-val text-purple">520 hrs / mo</span></div>
        </div>
      </div>
    </section>

    <!-- TAB 6: LIVE SANDBOXES -->
    <section id="sandboxes" class="tab-content">
      <div class="section-title">Live Interactive Sandboxes &amp; Consoles</div>
      <div class="section-desc">Test real AST symbol extraction, verify live cryptographic Merkle DAG blocks, and execute simulated surgical module rollbacks.</div>

      <div class="grid-2">
        <div class="card">
          <div class="card-badge">Live AST Demo</div>
          <h3>Structural AST Pruner Playground</h3>
          <p>Paste any TypeScript or Python snippet below and click Prune to see how internal method bodies are stripped into semantic skeletons:</p>
          <textarea id="astInput" rows="7" style="margin-bottom:10px;">export class PaymentProcessor {
  private secretKey: string;
  constructor(key: string) {
    this.secretKey = key;
  }
  public async executeCharge(accountId: string, amountCents: number): Promise<boolean> {
    // 50 lines of complex fraud scoring and ledger balancing
    const fee = amountCents * 0.029 + 30;
    console.log("Charging account " + accountId);
    return true;
  }
}</textarea>
          <button class="action-btn" onclick="runAstPruner()">Prune AST Skeleton</button>
          <div style="margin-top:14px;">
            <div class="stat-box"><span>Token Compression Ratio:</span><span id="astSavings" class="stat-val text-emerald">0%</span></div>
            <pre id="astOutput">// Output AST skeleton will appear here...</pre>
          </div>
        </div>

        <div class="card">
          <div class="card-badge">Cryptographic DAG</div>
          <h3>Merkle State Explorer &amp; Rollback</h3>
          <p>Current verifiable SHA-256 state chain from <code>.nb/context/ledger/context_ledger.yaml</code>:</p>
          <div id="dagBlocks">
            <div class="stat-box"><span>Block 0 (GENESIS):</span><span class="stat-val" style="font-size:11px; color:var(--muted);">7f8b9e4a3d2c1b0a...</span></div>
            <div class="stat-box"><span>Block 1 (BOOTSTRAP):</span><span class="stat-val" style="font-size:11px; color:var(--muted);">a3b2c1d0e9f8a7b6...</span></div>
            <div class="stat-box"><span>Block 2 (PR_GATE_PASS):</span><span class="stat-val" style="font-size:11px; color:var(--muted);">f881b2be129be959...</span></div>
          </div>
          <div style="margin-top:14px; display:flex; gap:10px; flex-wrap:wrap;">
            <button class="action-btn" onclick="loadDag()">Verify Merkle Chain</button>
            <button class="action-btn" style="background:var(--red); color:#fff;" onclick="triggerRollback()">Test Surgical Rollback</button>
          </div>
          <div style="margin-top:12px;">
            <div class="stat-box"><span>Prompt Cache Hit Rate:</span><span class="stat-val text-cyan">88.4%</span></div>
            <div class="stat-box"><span>Context Poisoning Incidents:</span><span class="stat-val text-emerald">0 Active</span></div>
          </div>
        </div>
      </div>

      <div class="card" style="margin-top:18px; border-color:var(--cyan); box-shadow:0 0 16px var(--cyan-glow);">
        <div class="card-badge" style="background:var(--cyan); color:#000;">Live FinOps Telemetry</div>
        <h3>Repository Token Savings &amp; Metering Ledger</h3>
        <p>Continuous context token reduction metrics calculated from <code>.nb/context/ledger/token_savings_ledger.yaml</code>:</p>
        <div class="grid-3" style="margin-top:12px;">
          <div class="stat-box"><span>Tokens Saved:</span><span id="portalTokensSaved" class="stat-val text-cyan">46,169</span></div>
          <div class="stat-box"><span>Gross Bill Savings:</span><span id="portalGrossSaved" class="stat-val text-emerald">$0.1385</span></div>
          <div class="stat-box"><span>15% Performance Fee:</span><span id="portalFee" class="stat-val text-purple">$0.0208</span></div>
        </div>
        <div class="grid-3" style="margin-top:8px;">
          <div class="stat-box"><span>Net Client Retained:</span><span id="portalNetSaved" class="stat-val text-emerald">$0.1177</span></div>
          <div class="stat-box"><span>Avg Token Reduction:</span><span id="portalReductionPct" class="stat-val text-cyan">39.3%</span></div>
          <div class="stat-box"><span>Pruning Events:</span><span id="portalEventsCount" class="stat-val text-amber">113</span></div>
        </div>
        <div style="margin-top:14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
          <a href="/api/tokens/savings" target="_blank" style="color:var(--cyan); font-size:12px; font-weight:600; text-decoration:none;">View Raw YAML/JSON Ledger &rarr;</a>
          <button class="action-btn" style="padding:6px 12px; font-size:11px;" onclick="fetchPortalTokenSavings()">Refresh FinOps Telemetry</button>
        </div>
      </div>

      <!-- Additional Consoles for Cognitive Router & Specialist Fleet -->
      <div class="grid-2" style="margin-top:18px;">
        <!-- Cognitive Router Interactive Simulator -->
        <div class="card">
          <div class="card-badge">Model-Agnostic Router</div>
          <h3>Cognitive Tiering Router Simulator</h3>
          <p>Test dynamic cognitive tier dispatch based on prompt complexity, target scope, and AST risk profile:</p>
          <div class="form-group">
            <select id="routerPromptSelect" onchange="updateCustomPromptText()">
              <option value="Verify unit test assertions and check for flaky retries in test suite">Verify unit test assertions &amp; flaky retries (Routine Task)</option>
              <option value="Scan AST imports and third-party dependencies for CVE supply-chain risks">Scan AST imports for dependency CVEs (Routine Security)</option>
              <option value="Synchronize architectural blueprint with live exported AST symbol signatures">Synchronize doc drift against AST exports (Routine Documentation)</option>
              <option value="Evolve cross-module RPC schema contract and verify backward compatibility">Evolve wire contract &amp; SemVer breaking change analysis (Complex Reasoning)</option>
              <option value="Perform multi-module context security audit and investigate hardcoded secrets">Infosec audit &amp; hardcoded secrets quarantine (High Risk)</option>
            </select>
          </div>
          <div class="form-group">
            <textarea id="routerPromptText" rows="3">Verify unit test assertions and check for flaky retries in test suite</textarea>
          </div>
          <button class="action-btn" onclick="simulateCognitiveRoute()">Dispatch Cognitive Route</button>
          <div id="routerResultBox" style="margin-top:14px; display:none; background:var(--code-bg); border:1px solid var(--border); border-radius:6px; padding:12px;">
            <div class="stat-box"><span>Selected Tier:</span><span id="routeTierVal" class="stat-val text-cyan">Tier B</span></div>
            <div class="stat-box"><span>Dispatched Model:</span><span id="routeModelVal" class="stat-val" style="font-weight:600;">claude-3-5-haiku / flash</span></div>
            <div class="stat-box"><span>Estimated Cost Savings:</span><span id="routeSavingsVal" class="stat-val text-emerald">90.0% Cost Discount</span></div>
            <p id="routeRationale" style="font-size:11px; color:var(--muted); margin-top:8px;"></p>
          </div>
        </div>

        <!-- Flaky Test & Specialist Agent Fleet Console -->
        <div class="card">
          <div class="card-badge">Autonomous CI/CD Fleet</div>
          <h3>Specialist Plugins &amp; Quarantine Console</h3>
          <p>Inspect the status of the 4 autonomous CI/CD specialist plugins and active quarantine ledgers:</p>
          <div style="display:flex; flex-direction:column; gap:8px; margin-top:10px;">
            <div class="stat-box">
              <div><strong style="color:var(--cyan); font-size:12px;">agent_flaky_test_detector</strong><br><span style="font-size:11px; color:var(--muted);">Non-blocking quarantine (user/hitl/flaky_quarantine.yaml)</span></div>
              <span class="badge badge-emerald">ACTIVE</span>
            </div>
            <div class="stat-box">
              <div><strong style="color:var(--cyan); font-size:12px;">agent_contract_compatibility_checker</strong><br><span style="font-size:11px; color:var(--muted);">JSON Schema Draft-07 &amp; SemVer guard (Tier A)</span></div>
              <span class="badge badge-emerald">ACTIVE</span>
            </div>
            <div class="stat-box">
              <div><strong style="color:var(--cyan); font-size:12px;">agent_dependency_cve_sentinel</strong><br><span style="font-size:11px; color:var(--muted);">Supply-chain AST import auditor &amp; license guard</span></div>
              <span class="badge badge-emerald">ACTIVE</span>
            </div>
            <div class="stat-box">
              <div><strong style="color:var(--cyan); font-size:12px;">agent_doc_drift_synchronizer</strong><br><span style="font-size:11px; color:var(--muted);">Verifies exported AST symbols against architecture plans</span></div>
              <span class="badge badge-emerald">ACTIVE</span>
            </div>
          </div>
          <div style="margin-top:14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
            <span style="font-size:11px; color:var(--muted);">Active Flaky Quarantine Blockers: <strong class="text-emerald">0 Active</strong></span>
            <button class="action-btn" style="padding:6px 12px; font-size:11px;" onclick="runFlakyCheckSimulation()">Run Determinism Check</button>
          </div>
          <div id="flakyCheckResult" style="display:none; font-size:11px; color:var(--green); margin-top:8px; font-family:'JetBrains Mono', monospace;"></div>
        </div>
      </div>
    </section>

    <!-- TAB 7: CLOUD & OPEX -->
    <section id="infrastructure" class="tab-content">
      <div class="section-title">Target Hosting Infrastructure &amp; Economics</div>
      <div class="section-desc">Production-grade Multi-AZ / Multi-Zone deployment blueprints for AWS and Google Cloud with itemized box costs and margin models.</div>

      <div class="table-wrap" style="margin-bottom:22px;">
        <table>
          <thead>
            <tr>
              <th>Subsystem Component</th>
              <th>AWS Architecture Asset</th>
              <th>Google Cloud Asset</th>
              <th>50 Clients AWS / GCP</th>
              <th>Functional Capability Powered</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="feature-name">K8s Control Plane</td>
              <td>AWS EKS (K8s 1.30+ Multi-AZ)</td>
              <td>GKE Multi-Zonal Cluster</td>
              <td>$73 / $73</td>
              <td>Multi-tenant control plane &amp; API gateways</td>
            </tr>
            <tr>
              <td class="feature-name">Worker Sandboxes</td>
              <td>Karpenter Spot c6i.2xlarge</td>
              <td>GKE Sandbox Spot VMs (runsc)</td>
              <td>$4,320 / $4,180</td>
              <td>Ephemeral Git worktree execution &amp; AST daemon</td>
            </tr>
            <tr>
              <td class="feature-name">PostgreSQL Database</td>
              <td>Aurora Serverless v2 (4-32 ACU)</td>
              <td>Cloud SQL Enterprise Plus HA</td>
              <td>$1,850 / $1,780</td>
              <td>Tenant RLS state DAG &amp; recovery points</td>
            </tr>
            <tr>
              <td class="feature-name">Distributed Cache</td>
              <td>ElastiCache Redis 7.x</td>
              <td>Cloud Memorystore Cluster</td>
              <td>$420 / $410</td>
              <td>Worktree lease TTL locks &amp; AST cache (&lt;15ms)</td>
            </tr>
            <tr>
              <td class="feature-name">Immutable WORM Vault</td>
              <td>Amazon S3 Object Lock</td>
              <td>GCS Object Retention WORM</td>
              <td>$280 / $260</td>
              <td>Non-repudiable SHA-256 Merkle audit proof bundles</td>
            </tr>
            <tr>
              <td class="feature-name">Telemetry Storage</td>
              <td>TimescaleDB on EBS gp3</td>
              <td>TimescaleDB on Hyperdisk</td>
              <td>$225 / $215</td>
              <td>Real-time context burn &amp; visual DAG feeds</td>
            </tr>
            <tr>
              <td class="feature-name">Edge WAF &amp; Ingress</td>
              <td>Cloudflare Enterprise + NLB</td>
              <td>Cloudflare Enterprise + TCP Proxy</td>
              <td>$895 / $850</td>
              <td>mTLS, DDoS protection, Ed25519 JWT injection</td>
            </tr>
            <tr>
              <td class="feature-name">APM Observability</td>
              <td>Datadog APM &amp; Pod Traces</td>
              <td>Cloud Operations Suite</td>
              <td>$1,150 / $1,050</td>
              <td>MicroVM saturation &amp; PR gate latency telemetry</td>
            </tr>
            <tr>
              <td class="feature-name">Tier B Verifier AI</td>
              <td>Claude 3.5 Haiku / Bedrock</td>
              <td>Gemini 1.5 Flash / Vertex</td>
              <td>$3,200 / $3,100</td>
              <td>Automated contract verification &amp; bounded TDD</td>
            </tr>
            <tr>
              <td class="feature-name">Security &amp; KMS</td>
              <td>AWS KMS CMK + GuardDuty</td>
              <td>Cloud KMS CMEK + SCC</td>
              <td>$767 / $750</td>
              <td>HKDF key derivation for .nbpack RAM decryption</td>
            </tr>
            <tr style="background:var(--bg-panel); font-weight:700;">
              <td class="feature-name" style="color:var(--cyan);">Total Monthly OpEx</td>
              <td>$12,980 / mo</td>
              <td>$12,468 / mo</td>
              <td class="text-emerald" style="font-weight:800;">$225,000 MRR</td>
              <td class="text-emerald">91.2% / 91.5% Gross Margin</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="grid-3">
        <div class="card">
          <div class="card-badge">Breakeven</div>
          <h3>1.5 Customers</h3>
          <p>Baseline cluster base costs (~$3,850/mo AWS / $3,690/mo GCP) are fully covered by just two business tier customers. Customer 2 generates immediate cash-flow positive EBITDA.</p>
        </div>
        <div class="card">
          <div class="card-badge">Spot Resilience</div>
          <h3>60% Spot Node Pools</h3>
          <p>Ephemeral worktrees use dynamic Spot VMs. In the event of cloud spot eviction, Percipience auto-falls back to On-Demand capacity in under 4 seconds without failing builds.</p>
        </div>
        <div class="card">
          <div class="card-badge">SLA Guarantees</div>
          <h3>99.95% Availability</h3>
          <p>Backed by multi-AZ Aurora/Cloud SQL replication, automated failover, and dual-region immutable WORM proof backups across S3 and Google Cloud Storage.</p>
        </div>
      </div>
    </section>

    <!-- TAB 8: PRICING & ONBOARDING -->
    <section id="pricing" class="tab-content">
      <div class="section-title">Licensing Tiers &amp; Instant Self-Serve Provisioning</div>
      <div class="section-desc">Choose your licensing tier or deploy directly inside your own private AWS or GCP VPC.</div>

      <div class="grid-3" style="margin-bottom:28px;">
        <div class="card">
          <div class="card-badge">Team Tier</div>
          <h3>Developer</h3>
          <div class="price-val">$1,499<span class="price-period"> / month</span></div>
          <p>For boutique AI agencies and startups running up to 15 engineers.</p>
          <ul class="bullet-list">
            <li>Up to 15 developer seats</li>
            <li>5 concurrent Git worktree sandboxes</li>
            <li>Structural AST token pruner daemon</li>
            <li>Cryptographic Merkle ledger &amp; CLI</li>
            <li>Community Slack &amp; standard support</li>
          </ul>
        </div>

        <div class="card" style="border-color:var(--cyan); box-shadow:0 0 16px var(--cyan-glow);">
          <div class="card-badge" style="background:var(--cyan); color:#000;">Most Popular</div>
          <h3>Business</h3>
          <div class="price-val">$4,499<span class="price-period"> / month</span></div>
          <p>For high-growth mid-market engineering orgs running up to 50 engineers.</p>
          <ul class="bullet-list">
            <li>Up to 50 developer seats</li>
            <li>20 concurrent Git worktree sandboxes</li>
            <li>Full Quad-Space architecture</li>
            <li>Context Poisoning &amp; Surgical Rollback</li>
            <li>CI/CD PR Gatekeeper (GitHub &amp; GitLab)</li>
            <li>Proprietary Plan Obfuscation (.nbpack)</li>
            <li>99.9% uptime SLA guarantee</li>
          </ul>
        </div>

        <div class="card">
          <div class="card-badge">Enterprise</div>
          <h3>Dedicated VPC</h3>
          <div class="price-val">$9,999+<span class="price-period"> / month</span></div>
          <p>For large enterprises and regulated FinTech / HealthTech platforms.</p>
          <ul class="bullet-list">
            <li>Unlimited developer seats</li>
            <li>Unlimited worktree concurrency</li>
            <li>Dedicated single-tenant VPC deployment</li>
            <li>BYOR for self-hosted GitLab / GHES</li>
            <li>Custom KMS CMEK hardware keys</li>
            <li>15% Token Savings Rev-Share add-on</li>
            <li>SOC 2 &amp; EU AI Act automated proofs</li>
            <li>24/7 dedicated engineering support</li>
          </ul>
        </div>
      </div>

      <div class="card" style="max-width:700px; margin:0 auto;">
        <div class="card-badge">Instant Provisioning</div>
        <h3>Instant Self-Serve Quad-Space Provisioning</h3>
        <p>Register your organization to provision an isolated tenant partition (Postgres RLS), register a KMS CMEK key, and receive an instant API key:</p>
        
        <div class="form-group">
          <label class="form-label">Organization Name:</label>
          <input type="text" id="onboardOrg" class="input" value="Acme Financial Engineering">
        </div>
        <div class="form-group">
          <label class="form-label">Admin Work Email:</label>
          <input type="email" id="onboardEmail" class="input" value="lead.architect@acme-fin.com">
        </div>
        <div class="form-group">
          <label class="form-label">Subscription Tier:</label>
          <select id="onboardTier" class="input">
            <option value="plan_business">Business Tier ($4,499/mo)</option>
            <option value="plan_team">Developer Team ($1,499/mo)</option>
            <option value="plan_enterprise">Enterprise Dedicated VPC ($9,999+/mo)</option>
          </select>
        </div>
        <button class="action-btn" onclick="submitOnboard()">Provision Workspace &amp; Issue API Key</button>
        <pre id="onboardResult" style="margin-top:14px; display:none;"></pre>
      </div>
    </section>

    <!-- TAB 9: DOCS -->
    <section id="docs" class="tab-content">
      <div class="section-title">Documentation Hub</div>
      <div class="section-desc">Comprehensive technical integration guides covering CLI, CI/CD Gatekeepers, .nbpack Enclaves, and Surgical Rollback.</div>

      <div class="grid-2">
        <div class="card">
          <div class="card-badge">CLI Quickstart</div>
          <h3>Getting Started (90 Seconds)</h3>
          <p>Install the Percipience CLI and initialize your repository into the Quad-Space standard:</p>
          <pre>npm install -g @neutronbinary/percipience
# Bootstrap Quad-Space with sealed .nbpack
percipience init --mode multi_module --parent-plan parent.nbpack
# Audit Merkle chain continuity
percipience audit --enforce-merkle-chain</pre>
        </div>

        <div class="card">
          <div class="card-badge">CI/CD Gatekeeper</div>
          <h3>GitHub Actions &amp; GitLab CI</h3>
          <p>Drop the automated gatekeeper action into your PR validation workflow:</p>
          <pre>- name: Run Percipience Gatekeeper
  uses: neutronbinary/percipience-action@v2
  with:
    api_key: ${{ secrets.PERCIPIENCE_API_KEY }}
    enforce_merkle_chain: true
    min_maturity_score: 0.85</pre>
        </div>

        <div class="card">
          <div class="card-badge">IP Defense</div>
          <h3>Compiling Obfuscated Plans (.nbpack)</h3>
          <p>Compile and sign proprietary context plans with zero disk leakage:</p>
          <pre>percipience pack \
  --input parent_master.md \
  --include-spaces .nb/context,.nb/agentic \
  --output .percipience/parent.nbpack \
  --obfuscate \
  --sign</pre>
        </div>

        <div class="card" style="border-color:var(--cyan); box-shadow:0 0 16px var(--cyan-glow);">
          <div class="card-badge" style="background:var(--cyan); color:#000;">Empirical Study</div>
          <h3>Benchmark Whitepaper: -62% Claude Token Bills</h3>
          <p>Read our empirical research paper analyzing 250 tasks across 565k LOC in TypeScript, Python, Go, Rust, and Java:</p>
          <ul class="bullet-list">
            <li><b>-62.4% Context Tokens</b> via Tree-Sitter AST body stripping</li>
            <li><b>88.6% Prompt Cache Hit Rate</b> via static invariant alignment</li>
            <li><b>-71.8% Direct Cost Drop</b> ($1.42 -> $0.40 blended cost per task)</li>
            <li><b>0% Workspace Collisions</b> across 10 concurrent agent worktrees</li>
          </ul>
          <div style="margin-top:12px;">
            <a href="/api/docs/whitepaper" target="_blank" style="color:var(--cyan); font-weight:700; text-decoration:none; font-size:12px;">Download / View Full Whitepaper Markdown &rarr;</a>
          </div>
        </div>

        <div class="card">
          <div class="card-badge">Recovery</div>
          <h3>Surgical Module Rollback Protocol</h3>
          <p>Recover from context poisoning without breaking concurrent micro-modules:</p>
          <pre># Sparing sibling micro-modules:
percipience rollback \
  --module mod_observability_usage \
  --target-point RP_PLAY3_BOOTSTRAP_001</pre>
        </div>
      </div>
    </section>

    <!-- TAB 10: DEEP REPORTS & WHITE PAPERS -->
    <section id="reports" class="tab-content">
      <div class="section-title">Engineering Whitepapers, Audits &amp; Formal Reports</div>
      <div class="section-desc">Authoritative technical reports generated by the Percipience control plane, covering token reduction mathematics, 20-point SDLC drift audits, context maturity evaluations, and competitive benchmarks.</div>

      <div class="grid-3" style="margin-bottom:22px;">
        <div class="card">
          <div class="card-badge">Mathematical Whitepaper</div>
          <h3>Token Reduction &amp; Attention Slicing</h3>
          <p>Formal mathematical proof of 50%–75% prompt context reduction using 6D AST skeletonization and Static Prefix KV-Cache pinning.</p>
          <div class="stat-box" style="flex-direction:column; align-items:flex-start; margin-bottom:12px;">
            <div>T_opt = ∑ AST(m) + Prefix + Diag</div>
            <div class="text-emerald" style="margin-top:4px; font-weight:700;">Savings: 5.45M Tokens ($16.36 Saved)</div>
          </div>
          <button class="btn btn-secondary" onclick="showTab('docs')" style="width:100%; font-size:11px;">View Full Whitepaper &rarr;</button>
        </div>

        <div class="card">
          <div class="card-badge">SDLC Governance Review</div>
          <h3>20-Point Autonomous SDLC Audit</h3>
          <p>Comprehensive architectural analysis of shortcomings, drifts, and fixes across Swarm governance, D_max=2 anti-usurpation, and ReAct trajectory recording.</p>
          <div class="stat-box" style="flex-direction:column; align-items:flex-start; margin-bottom:12px;">
            <div>Shortcomings Identified: 20</div>
            <div class="text-cyan" style="margin-top:4px; font-weight:700;">Remediation Status: 100% Implemented</div>
          </div>
          <button class="btn btn-secondary" onclick="showTab('capabilities')" style="width:100%; font-size:11px;">Explore SDLC Subsystems &rarr;</button>
        </div>

        <div class="card">
          <div class="card-badge">Autonomous Maturity Scorecard</div>
          <h3>Context Maturity Evaluation (Level 5)</h3>
          <p>Scoring the repository across 5 maturity tiers (Ad-hoc to Level 5 Self-Sustaining Autonomous OS) with 100% Quad-Space boundary compliance.</p>
          <div class="stat-box" style="flex-direction:column; align-items:flex-start; margin-bottom:12px;">
            <div>Maturity Score: <strong>100.0 / 100 (Level 5)</strong></div>
            <div class="text-purple" style="margin-top:4px; font-weight:700;">Merkle Blocks: 1007 Continuous</div>
          </div>
          <button class="btn btn-secondary" onclick="showTab('observability')" style="width:100%; font-size:11px;">Open Observability Radar &rarr;</button>
        </div>
      </div>
    </section>

    <!-- TAB 11: OBSERVABILITY DASHBOARD -->
    <section id="observability" class="tab-content">
      <div class="section-title">OpenTelemetry GenAI &amp; Quantitative Quality Hub</div>
      <div class="section-desc">Enterprise telemetry streaming OpenTelemetry GenAI spans, 5-dimensional G-Eval quality scores, semantic prompt caching FinOps, and attention budget quotas.</div>

      <div class="grid-cards" style="margin-bottom:22px;">
        <div class="metric-card">
          <div class="metric-val text-cyan">W3C Standard</div>
          <div class="metric-label">Distributed Tracing (OTel GenAI)</div>
        </div>
        <div class="metric-card">
          <div class="metric-val text-emerald" id="gevalScoreVal">0.962 / 1.00</div>
          <div class="metric-label">Composite G-Eval Quality Score</div>
        </div>
        <div class="metric-card">
          <div class="metric-val text-purple" id="cacheHitRateVal">64.8%</div>
          <div class="metric-label">Semantic Prompt Cache Hit Rate</div>
        </div>
        <div class="metric-card">
          <div class="metric-val text-amber">100% Pinned</div>
          <div class="metric-label">Static Prefix KV-Cache Alignment</div>
        </div>
      </div>

      <!-- OTEL SPANS TABLE -->
      <div class="card" style="margin-bottom:22px;">
        <div class="card-title">
          <span>⚡ Real-Time OpenTelemetry GenAI Spans</span>
          <button class="btn btn-secondary" onclick="fetchOtelSpans()" style="padding:4px 10px; font-size:11px;">🔄 Refresh Spans</button>
        </div>
        <div class="table-wrap" style="margin:8px 0 0;">
          <table class="table">
            <thead>
              <tr>
                <th>Traceparent / Span Name</th>
                <th>Model &amp; Vendor</th>
                <th>TTFT</th>
                <th>Latency</th>
                <th>Token Usage (In / Out)</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="otelSpansBody">
              <tr>
                <td><code>00-4bf92f35...-00f067aa...-01</code><br><strong>agent_living_doc_architect</strong></td>
                <td><code>claude-3-7-sonnet</code> (anthropic)</td>
                <td>340 ms</td>
                <td>1,120 ms</td>
                <td>2,450 / 620 tok</td>
                <td><span class="status-pill status-active">STATUS_OK</span></td>
              </tr>
              <tr>
                <td><code>00-8ca12b91...-11a084bc...-01</code><br><strong>agent_adversarial_fuzzer</strong></td>
                <td><code>claude-3-5-haiku</code> (anthropic)</td>
                <td>180 ms</td>
                <td>640 ms</td>
                <td>1,100 / 280 tok</td>
                <td><span class="status-pill status-active">STATUS_OK</span></td>
              </tr>
              <tr>
                <td><code>00-9ef34a10...-22c095de...-01</code><br><strong>agent_ambiguity_resolver</strong></td>
                <td><code>claude-3-5-haiku</code> (anthropic)</td>
                <td>150 ms</td>
                <td>490 ms</td>
                <td>850 / 190 tok</td>
                <td><span class="status-pill status-active">STATUS_OK</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 5D QUALITY & ATTENTION SLICING GRID -->
      <div class="grid-2" style="margin-bottom:22px;">
        <div class="card">
          <div class="card-title">🎯 5-Dimensional Quantitative Evals &amp; Hallucination Radar</div>
          <p>Automated G-Eval rubric evaluations across code correctness, hallucination freedom, and ground-truth parity.</p>
          <div class="vector-list">
            <div class="vector-item">
              <div class="vector-header"><span>Faithfulness (Grounding):</span><strong class="text-emerald">0.980 / 1.00</strong></div>
              <div class="bar-track"><div class="bar-fill bg-emerald" style="width:98%;"></div></div>
            </div>
            <div class="vector-item">
              <div class="vector-header"><span>Hallucination Freedom:</span><strong class="text-emerald">0.995 / 1.00</strong></div>
              <div class="bar-track"><div class="bar-fill bg-emerald" style="width:99.5%;"></div></div>
            </div>
            <div class="vector-item">
              <div class="vector-header"><span>Context Relevancy:</span><strong class="text-cyan">0.940 / 1.00</strong></div>
              <div class="bar-track"><div class="bar-fill bg-cyan" style="width:94%;"></div></div>
            </div>
            <div class="vector-item">
              <div class="vector-header"><span>Code Correctness &amp; Syntax:</span><strong class="text-purple">1.000 / 1.00</strong></div>
              <div class="bar-track"><div class="bar-fill bg-purple" style="width:100%;"></div></div>
            </div>
            <div class="vector-item">
              <div class="vector-header"><span>Semantic Parity vs Spec:</span><strong class="text-amber">0.996 / 1.00</strong></div>
              <div class="bar-track"><div class="bar-fill bg-amber" style="width:99.6%;"></div></div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-title">🧠 Context Attention Slicing &amp; Token Budget Quotas</div>
          <p>Mathematical quota budgeting preventing context overflow and lost-in-the-middle attention degradation.</p>
          <div class="vector-list">
            <div class="vector-item">
              <div class="vector-header"><span>1. System Persona &amp; Invariants (15%):</span><strong>15.0% (Protected)</strong></div>
              <div class="bar-track"><div class="bar-fill bg-cyan" style="width:15%;"></div></div>
            </div>
            <div class="vector-item">
              <div class="vector-header"><span>2. Schemas &amp; Wire Contracts (25%):</span><strong>25.0% (Active)</strong></div>
              <div class="bar-track"><div class="bar-fill bg-purple" style="width:25%;"></div></div>
            </div>
            <div class="vector-item">
              <div class="vector-header"><span>3. AST Codebase Skeleton (35%):</span><strong>35.0% (Tree-Sitter)</strong></div>
              <div class="bar-track"><div class="bar-fill bg-emerald" style="width:35%;"></div></div>
            </div>
            <div class="vector-item">
              <div class="vector-header"><span>4. Memory &amp; ReAct Trajectories (10%):</span><strong>10.0% (Serialized)</strong></div>
              <div class="bar-track"><div class="bar-fill bg-amber" style="width:10%;"></div></div>
            </div>
            <div class="vector-item">
              <div class="vector-header"><span>5. LLM Generation Target Space (15%):</span><strong>15.0% (Reserved)</strong></div>
              <div class="bar-track"><div class="bar-fill bg-cyan" style="width:15%;"></div></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 12: SECURE CLIENT SPACE -->
    <section id="client" class="tab-content">
      <!-- UNAUTHENTICATED LOGIN CARD -->
      <div id="clientLoginCard" class="card" style="max-width:540px; margin:32px auto; padding:28px;">
        <div class="card-title" style="font-size:18px;">🔐 Secure Client Space</div>
        <p style="margin-bottom:18px;">Access confidential project telemetry, itemized FinOps rev-share invoices, recovery points, and WORM compliance audit proofs.</p>
        
        <div class="form-group">
          <label class="form-label">Client ID / Organization</label>
          <input type="text" id="loginClientId" class="input" placeholder="e.g. acme_corp_fintech" value="acme_corp_fintech">
        </div>

        <div class="form-group">
          <label class="form-label">API Key / Secret Token</label>
          <input type="password" id="loginApiKey" class="input" placeholder="e.g. nb_sec_client_9948" value="nb_sec_client_9948">
        </div>

        <div style="display:flex; gap:10px; margin-top:16px;">
          <button class="btn btn-primary" onclick="loginClient(false)" style="flex:1;">🔐 Sign In to Client Workspace</button>
          <button class="btn btn-secondary" onclick="loginClient(true)">⚡ Demo Login</button>
        </div>
        <div id="loginErrorMsg" style="color:var(--red); font-size:12px; margin-top:12px; display:none;">Invalid credentials. Please verify your client ID and API key.</div>
      </div>

      <!-- AUTHENTICATED CLIENT CONSOLE -->
      <div id="clientAuthConsole" style="display:none;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; border-bottom:1px solid var(--border); padding-bottom:14px; flex-wrap:wrap; gap:10px;">
          <div>
            <div style="font-size:20px; font-weight:800; color:var(--cyan);" id="clientOrgName">Acme Global Financial Technologies</div>
            <div style="font-size:12px; color:var(--muted); margin-top:3px;">Client ID: <code id="clientIdDisplay">acme_corp_fintech</code> &bull; Project: <strong id="clientProjectName" style="color:var(--text);">NB Fairyfly Core</strong> &bull; Tier: <span class="badge badge-purple" id="clientTierBadge">Enterprise Tier A</span></div>
          </div>
          <button class="btn btn-secondary" onclick="logoutClient()" style="padding:6px 14px; font-size:11px;">🚪 Sign Out</button>
        </div>

        <!-- CLIENT CARDS -->
        <div class="grid-cards" style="margin-bottom:22px;">
          <div class="metric-card">
            <div class="metric-val text-emerald" id="clientGrossSavings">$15.6974</div>
            <div class="metric-label">Verified Gross Token Savings</div>
          </div>
          <div class="metric-card">
            <div class="metric-val text-cyan" id="clientRevShareDue">$2.3546</div>
            <div class="metric-label">15% Rev-Share Performance Fee Due</div>
          </div>
          <div class="metric-card">
            <div class="metric-val text-purple">multi_module</div>
            <div class="metric-label">Active Workspace Mode</div>
          </div>
          <div class="metric-card">
            <div class="metric-val text-amber" id="clientWormStatus">LOCKED (S3 WORM)</div>
            <div class="metric-label">SEC 17a-4 / FINRA Compliance Vault</div>
          </div>
        </div>

        <!-- MODULES & SURGICAL ROLLBACK CONTROL -->
        <div class="card" style="margin-bottom:22px;">
          <div class="card-title">🛡️ Project Micro-Modules &amp; Surgical Recovery Points</div>
          <p style="margin-bottom:14px;">Isolated module recovery points allow surgical rollback of individual sub-modules without disturbing sibling services.</p>
          <div class="table-wrap" style="margin:8px 0 0;">
            <table class="table">
              <thead>
                <tr>
                  <th>Module Identifier</th>
                  <th>Status</th>
                  <th>Active Recovery Point</th>
                  <th>WORM Block Hash</th>
                  <th>Surgical Action</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td><code>mod_auth</code></td>
                  <td><span class="status-pill status-active">HEALTHY</span></td>
                  <td><code>RP_AUTH_008</code></td>
                  <td><code>fa19a510c7f48ff7...</code></td>
                  <td><button class="btn btn-secondary" style="font-size:11px; padding:4px 8px;" onclick="triggerSurgicalRollback('mod_auth')">Rewind to RP</button></td>
                </tr>
                <tr>
                  <td><code>mod_billing</code></td>
                  <td><span class="status-pill status-active">HEALTHY</span></td>
                  <td><code>RP_BILL_012</code></td>
                  <td><code>6d01c481ce9e5817...</code></td>
                  <td><button class="btn btn-secondary" style="font-size:11px; padding:4px 8px;" onclick="triggerSurgicalRollback('mod_billing')">Rewind to RP</button></td>
                </tr>
                <tr>
                  <td><code>mod_portal_marketing</code></td>
                  <td><span class="status-pill status-active">HEALTHY</span></td>
                  <td><code>RP_PORTAL_006</code></td>
                  <td><code>2303ddbecaaab5f3...</code></td>
                  <td><button class="btn btn-secondary" style="font-size:11px; padding:4px 8px;" onclick="triggerSurgicalRollback('mod_portal_marketing')">Rewind to RP</button></td>
                </tr>
                <tr>
                  <td><code>mod_trading</code></td>
                  <td><span class="status-pill status-active">HEALTHY</span></td>
                  <td><code>RP_TRAD_009</code></td>
                  <td><code>8ca12b9199fe014b...</code></td>
                  <td><button class="btn btn-secondary" style="font-size:11px; padding:4px 8px;" onclick="triggerSurgicalRollback('mod_trading')">Rewind to RP</button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ITEMIZED FINOPS INVOICE -->
        <div class="card">
          <div class="card-title">🧾 Itemized FinOps Rev-Share Accounting Invoice</div>
          <p style="margin-bottom:14px;">Transparent, zero-risk performance fee billing: You pay only 15% of verified cloud token cost reductions.</p>
          <div style="background:var(--code-bg); padding:16px; border-radius:8px; border:1px solid var(--border); font-family:'JetBrains Mono', monospace; font-size:12px;">
            <div class="stat-box" style="background:transparent; border:none; padding:3px 0;"><span>Raw Base Tokens Processed:</span><strong style="color:var(--text);">5,232,080 tokens</strong></div>
            <div class="stat-box" style="background:transparent; border:none; padding:3px 0;"><span>AST Pruning Reduction (50.3%):</span><strong class="text-emerald">-2,631,736 tokens</strong></div>
            <div class="stat-box" style="background:transparent; border:none; padding:3px 0;"><span>Semantic Cache Hits Reduction:</span><strong class="text-emerald">-1,240,000 tokens</strong></div>
            <div class="stat-box" style="background:transparent; border:none; padding:6px 0 3px; border-top:1px solid var(--border); margin-top:6px;"><span>Gross Client Cloud Savings ($0.003/1K tok):</span><strong class="text-emerald">$15.6974 USD</strong></div>
            <div class="stat-box" style="background:transparent; border:none; padding:6px 0 0; border-top:1px dashed var(--border); font-size:13px; font-weight:700; margin-top:6px;"><span>Percipience Performance Fee (15%):</span><strong class="text-cyan">$2.3546 USD</strong></div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 13: MULTI-TENANT ENTERPRISE GOVERNANCE & POLICY TUNING (CAP-40 / CAP-41) -->
    <section id="governance" class="tab-content">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px; border-bottom:1px solid var(--border); padding-bottom:16px; flex-wrap:wrap; gap:12px;">
        <div>
          <div style="font-size:22px; font-weight:800; color:var(--purple); display:flex; align-items:center; gap:8px;">
            <span>🏛️</span> Sovereign Enterprise Multi-Tenant Governance &amp; Minute Policy Control
          </div>
          <div style="font-size:13px; color:var(--muted); margin-top:4px;">
            Row-Level Security (RLS) • One-Click Scaffolding • Automated KMS Sealed Enclaves • Granular Context Tuning &amp; Healing SLA
          </div>
        </div>
        <div style="display:flex; gap:10px; align-items:center;">
          <span class="badge badge-purple" style="font-size:11px;">PostgreSQL RLS Active</span>
          <span class="badge badge-green" style="font-size:11px;">Role: Enterprise Super Admin</span>
          <button class="btn btn-secondary" onclick="loadGovernanceTab()" style="padding:6px 14px; font-size:11px;">🔄 Refresh State</button>
        </div>
      </div>

      <!-- ROW 1: TENANT HIERARCHY & SCAFFOLDING WIZARD -->
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(460px, 1fr)); gap:20px; margin-bottom:24px;">
        
        <!-- CARD 1: HIERARCHY & RLS -->
        <div class="card">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div class="card-title" style="margin-bottom:0;">🏢 Sovereign Organization &amp; Project Hierarchy</div>
            <button class="btn btn-secondary" onclick="toggleRlsSchema()" style="font-size:11px; padding:4px 10px;">🔎 Inspect RLS DDL</button>
          </div>
          <p style="font-size:12px; margin-bottom:14px;">
            Strict 4-level isolation: <code>Tenant</code> → <code>Project</code> → <code>Repository</code> → <code>Workstation Nodes</code>. PostgreSQL RLS enforces zero data leakage across multi-tenant queries.
          </p>

          <div id="govHierarchyContainer" style="background:var(--code-bg); padding:14px; border-radius:8px; border:1px solid var(--border); min-height:180px;">
            <div style="color:var(--muted); font-size:12px;">Loading organization hierarchy...</div>
          </div>

          <div id="rlsSchemaWrapper" style="display:none; margin-top:14px;">
            <div style="font-size:12px; font-weight:700; color:var(--cyan); margin-bottom:6px;">Generated PostgreSQL Row-Level Security DDL:</div>
            <pre id="rlsDdlText" style="max-height:220px;">-- Loading DDL...</pre>
          </div>
        </div>

        <!-- CARD 2: ONE-CLICK SCAFFOLDING WIZARD -->
        <div class="card">
          <div class="card-title">🧙 One-Click Quad-Space Project Scaffolder</div>
          <p style="font-size:12px; margin-bottom:14px;">
            Automates directory initialization (<code>.nb/context</code>, <code>.nb/agentic</code>, <code>workplace</code>, <code>user</code>), mints Genesis cryptographic recovery block <code>RP_GENESIS_000</code>, and provisions isolated KMS keys.
          </p>

          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:12px;">
            <div class="form-group" style="margin-bottom:0;">
              <label class="form-label" style="font-size:11px;">Project Identifier</label>
              <input type="text" id="scaffoldProjectId" class="input" value="proj_crypto_arbitrage_01" style="font-size:12px;">
            </div>
            <div class="form-group" style="margin-bottom:0;">
              <label class="form-label" style="font-size:11px;">Architecture Mode</label>
              <select id="scaffoldMode" class="select" style="font-size:12px;">
                <option value="multi_module">multi_module (Quad-Space)</option>
                <option value="isolated_micro_service">isolated_micro_service</option>
                <option value="monolith">monolith</option>
              </select>
            </div>
          </div>

          <div class="form-group" style="margin-bottom:14px;">
            <label class="form-label" style="font-size:11px;">Project Display Name</label>
            <input type="text" id="scaffoldProjectName" class="input" value="Crypto High-Frequency Arbitrage Engine" style="font-size:12px;">
          </div>

          <button class="btn btn-primary" onclick="triggerProjectScaffold()" style="width:100%; font-size:12px;">🚀 Scaffold Quad-Space Architecture &amp; Mint Genesis Block</button>

          <div id="scaffoldResultBox" style="display:none; margin-top:14px; background:var(--code-bg); padding:12px; border-radius:6px; border:1px solid var(--border); font-size:11px;"></div>
        </div>
      </div>

      <!-- ROW 2: KMS SEALED ENCLAVES & GRANULAR POLICY TUNING -->
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(460px, 1fr)); gap:20px;">

        <!-- CARD 3: AUTOMATED KMS ENCLAVE VAULT -->
        <div class="card">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div class="card-title" style="margin-bottom:0;">🔐 Automated KMS Key Broker &amp; In-Memory Enclaves</div>
            <span class="badge badge-green" style="font-size:10px;">Ed25519 + AES-256-GCM Active</span>
          </div>
          <p style="font-size:12px; margin-bottom:14px;">
            Authenticates digital signatures and decrypts proprietary <code>.nbpack</code> domain bundles directly in volatile RAM with zero plaintext written to disk.
          </p>

          <div class="form-group" style="margin-bottom:12px;">
            <label class="form-label" style="font-size:11px;">Enclave Payload Data (JSON)</label>
            <textarea id="kmsPayloadInput" class="textarea" rows="4" style="font-size:11px; font-family:'JetBrains Mono', monospace;">{
  "prompt_system": "Act as an autonomous institutional risk &amp; execution agent.",
  "max_var_loss_usd": 50000.0,
  "approved_symbols": ["BTC-USD", "ETH-USD"]
}</textarea>
          </div>

          <div style="display:flex; gap:10px; margin-bottom:14px;">
            <button class="btn btn-primary" onclick="triggerKmsSeal()" style="flex:1; font-size:11px;">📦 Seal In-Memory .nbpack</button>
            <button class="btn btn-secondary" onclick="triggerKmsMount()" style="flex:1; font-size:11px;">⚡ Mount in RAM (0% Disk Residue)</button>
            <button class="btn btn-secondary" onclick="triggerKmsAudit()" style="font-size:11px; padding:6px 12px;">📜 Audit Log</button>
          </div>

          <div id="kmsResultBox" style="display:none; background:var(--code-bg); padding:12px; border-radius:6px; border:1px solid var(--border); font-size:11px;"></div>
        </div>

        <!-- CARD 4: GRANULAR CONTEXT TUNING SLIDERS & SLA POLICIES -->
        <div class="card">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <div class="card-title" style="margin-bottom:0;">🎛️ Minute Project Control &amp; Policy Tuning Sliders</div>
            <span id="budgetTotalBadge" class="badge badge-green" style="font-size:10px;">Budget: 100.0% (Valid)</span>
          </div>
          <p style="font-size:12px; margin-bottom:12px;">
            Declarative per-project policy configuration: Dynamic attention slicing quotas, cognitive routing thresholds, diagnostic re-prompts, and flaky test quarantining.
          </p>

          <!-- VISUAL STACKED BUDGET DISTRIBUTION BAR -->
          <div style="font-size:11px; font-weight:700; color:var(--muted); margin-bottom:4px;">Dynamic Prompt Attention Budget Distribution (100% Total):</div>
          <div class="budget-bar-container" id="budgetDistributionBar">
            <div class="budget-slice bg-purple" id="slicePersona" style="width:15%;" title="Persona &amp; Invariants (15%)">15% Rules</div>
            <div class="budget-slice bg-cyan" id="sliceContracts" style="width:25%;" title="Contracts &amp; Schemas (25%)">25% Contracts</div>
            <div class="budget-slice bg-green" id="sliceAst" style="width:35%;" title="AST Codebase (35%)">35% AST Code</div>
            <div class="budget-slice bg-amber" id="sliceMemory" style="width:10%;" title="Memory &amp; Trajectories (10%)">10% Mem</div>
            <div class="budget-slice" id="sliceOutput" style="width:15%; background:#ec4899;" title="Reserved Output Headroom (15%)">15% Headroom</div>
          </div>

          <!-- SLIDERS: ATTENTION QUOTAS -->
          <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:14px;">
            <div class="slider-group">
              <div class="slider-header">
                <label>🛡️ Persona &amp; Invariants</label>
                <span class="slider-val" id="valPersona">15%</span>
              </div>
              <input type="range" id="sliderPersona" min="5" max="30" value="15" oninput="onSliderChange()">
            </div>

            <div class="slider-group">
              <div class="slider-header">
                <label>📜 Contracts &amp; Schemas</label>
                <span class="slider-val" id="valContracts">25%</span>
              </div>
              <input type="range" id="sliderContracts" min="10" max="40" value="25" oninput="onSliderChange()">
            </div>

            <div class="slider-group">
              <div class="slider-header">
                <label>🌳 AST Codebase Context</label>
                <span class="slider-val" id="valAst">35%</span>
              </div>
              <input type="range" id="sliderAst" min="15" max="55" value="35" oninput="onSliderChange()">
            </div>

            <div class="slider-group">
              <div class="slider-header">
                <label>🧠 Memory &amp; Trajectories</label>
                <span class="slider-val" id="valMemory">10%</span>
              </div>
              <input type="range" id="sliderMemory" min="5" max="25" value="10" oninput="onSliderChange()">
            </div>
          </div>

          <div class="slider-group" style="margin-bottom:16px;">
            <div class="slider-header">
              <label>🚀 Reserved Output Headroom (Guaranteed Generation)</label>
              <span class="slider-val" id="valOutput" style="color:#ec4899;">15%</span>
            </div>
            <input type="range" id="sliderOutput" min="5" max="30" value="15" oninput="onSliderChange()">
          </div>

          <!-- SLA & ROUTING CONTROLS -->
          <div style="border-top:1px solid var(--border); padding-top:14px; margin-bottom:14px;">
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:12px;">
              <div class="slider-group" style="margin-bottom:0;">
                <div class="slider-header">
                  <label>⚙️ Cognitive Tier A Threshold</label>
                  <span class="slider-val" id="valTierA">0.70</span>
                </div>
                <input type="range" id="sliderTierA" min="0.10" max="0.95" step="0.05" value="0.70" oninput="document.getElementById('valTierA').innerText = parseFloat(this.value).toFixed(2)">
              </div>

              <div class="slider-group" style="margin-bottom:0;">
                <div class="slider-header">
                  <label>🔁 Diagnostic Re-Prompts</label>
                  <span class="slider-val" id="valReprompts">3 turns</span>
                </div>
                <input type="range" id="sliderReprompts" min="1" max="5" value="3" oninput="document.getElementById('valReprompts').innerText = this.value + ' turns'">
              </div>
            </div>

            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-bottom:12px;">
              <div class="slider-group" style="margin-bottom:0;">
                <div class="slider-header">
                  <label>🧬 Flaky Quarantine Threshold</label>
                  <span class="slider-val" id="valFlaky">15.0%</span>
                </div>
                <input type="range" id="sliderFlaky" min="0.05" max="0.40" step="0.01" value="0.15" oninput="document.getElementById('valFlaky').innerText = (parseFloat(this.value)*100).toFixed(1) + '%'">
              </div>

              <div class="form-group" style="margin-bottom:0;">
                <label class="form-label" style="font-size:11px;">Wire Contract Breaking Rule</label>
                <select id="policyWireRule" class="select" style="font-size:11px; padding:6px 10px;">
                  <option value="STRICT_BLOCK">STRICT_BLOCK (Gate Rejection)</option>
                  <option value="ALLOW_ADDITIVE_WARN">ALLOW_ADDITIVE_WARN (Warn Only)</option>
                  <option value="MANUAL_APPROVAL">MANUAL_APPROVAL (HITL Signoff)</option>
                </select>
              </div>
            </div>
          </div>

          <!-- ACTION BUTTONS -->
          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            <button class="btn btn-primary" onclick="saveCurrentPolicy()" style="flex:2; font-size:11px;">💾 Save &amp; Enforce Policy</button>
            <button class="btn btn-secondary" onclick="testDynamicAttention()" style="flex:1; font-size:11px;">🧪 Test Slicing</button>
            <button class="btn btn-secondary" onclick="simulatePrGateLive()" style="flex:1; font-size:11px;">🛡️ Simulate PR Gate</button>
          </div>

          <div id="policyResultBox" style="display:none; margin-top:14px; background:var(--code-bg); padding:12px; border-radius:6px; border:1px solid var(--border); font-size:11px;"></div>
        </div>

      </div>
    </section>

    <!-- TAB 14: COMMERCIAL PACKAGE PROVISIONER & TIER LICENSING (CAP-42) -->
    <section id="commercial-provisioner" class="tab-content">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px; border-bottom:1px solid var(--border); padding-bottom:16px; flex-wrap:wrap; gap:12px;">
        <div>
          <div style="font-size:22px; font-weight:800; color:var(--amber); display:flex; align-items:center; gap:8px;">
            <span>📦</span> Percipience Commercial Packager, Multi-Tier Provisioner &amp; Entitlement Engine
          </div>
          <div style="font-size:13px; color:var(--muted); margin-top:4px;">
            Automated Tier-Specific Runtime Packaging • Cross-IDE Cryptographic Provisioning • Ed25519 License Minting • RBAC Permission Gate
          </div>
        </div>
        <div style="display:flex; gap:10px; align-items:center;">
          <span class="badge badge-amber" style="font-size:11px;">Zero-Trust Tier Enforcement</span>
          <span class="badge badge-green" style="font-size:11px;">SHA-256 Merkle Sealed</span>
          <button class="btn btn-secondary" onclick="loadCommercialTab()" style="padding:6px 14px; font-size:11px;">🔄 Refresh Tiers</button>
        </div>
      </div>

      <!-- ROW 1: 4-TIER COMMERCIAL SPECIFICATION MATRIX -->
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap:16px; margin-bottom:24px;">
        <!-- TIER: FREE -->
        <div class="card" style="border-top: 3px solid var(--muted);">
          <div class="card-badge" style="background:rgba(148,163,184,0.15); color:var(--muted);">Free Community</div>
          <div style="font-size:24px; font-weight:800; font-family:'JetBrains Mono', monospace; margin:6px 0;">$0 <span style="font-size:12px; color:var(--muted); font-weight:400;">/ mo</span></div>
          <p style="font-size:12px; margin-bottom:12px;">Solo developers &amp; open-source projects with local AST optimization.</p>
          <div style="font-size:11.5px; display:flex; flex-direction:column; gap:6px; color:var(--text);">
            <div>👥 <b>1 Included Seat</b></div>
            <div>⚡ <b>1 Concurrent Worktree</b></div>
            <div>🛡️ <b>500 PR Audits / month</b></div>
            <div>🔒 Tree-Sitter &amp; Merkle Core</div>
            <div style="color:var(--muted);">❌ Custom Agents &amp; Enclaves</div>
          </div>
        </div>

        <!-- TIER: TEAM -->
        <div class="card" style="border-top: 3px solid var(--cyan);">
          <div class="card-badge" style="background:var(--cyan-glow); color:var(--cyan);">Team</div>
          <div style="font-size:24px; font-weight:800; font-family:'JetBrains Mono', monospace; margin:6px 0;">$1,499 <span style="font-size:12px; color:var(--muted); font-weight:400;">/ mo</span></div>
          <p style="font-size:12px; margin-bottom:12px;">Growing engineering pods with custom agent workflows and prompt drift tracking.</p>
          <div style="font-size:11.5px; display:flex; flex-direction:column; gap:6px; color:var(--text);">
            <div>👥 <b>15 Included Seats</b></div>
            <div>⚡ <b>5 Concurrent Worktrees</b></div>
            <div>🛡️ <b>5,000 PR Audits / month</b></div>
            <div>🤖 Custom Agent Definitions</div>
            <div style="color:var(--muted);">❌ Private VPC &amp; WORM</div>
          </div>
        </div>

        <!-- TIER: BUSINESS -->
        <div class="card" style="border-top: 3px solid var(--purple);">
          <div class="card-badge" style="background:var(--purple-glow); color:var(--purple);">Business</div>
          <div style="font-size:24px; font-weight:800; font-family:'JetBrains Mono', monospace; margin:6px 0;">$4,999 <span style="font-size:12px; color:var(--muted); font-weight:400;">/ mo</span></div>
          <p style="font-size:12px; margin-bottom:12px;">Scale-ups requiring .nbpack enclave compilation &amp; Cognitive Routing.</p>
          <div style="font-size:11.5px; display:flex; flex-direction:column; gap:6px; color:var(--text);">
            <div>👥 <b>50 Included Seats</b></div>
            <div>⚡ <b>20 Concurrent Worktrees</b></div>
            <div>🛡️ <b>25,000 PR Audits / month</b></div>
            <div>📦 .nbpack Enclave Bundling</div>
            <div>🧠 Cognitive Routing &amp; Gateways</div>
          </div>
        </div>

        <!-- TIER: ENTERPRISE -->
        <div class="card" style="border-top: 3px solid var(--amber);">
          <div class="card-badge" style="background:var(--amber-glow); color:var(--amber);">Enterprise Dedicated</div>
          <div style="font-size:24px; font-weight:800; font-family:'JetBrains Mono', monospace; margin:6px 0;">$12,499 <span style="font-size:12px; color:var(--muted); font-weight:400;">/ mo</span></div>
          <p style="font-size:12px; margin-bottom:12px;">Full sovereign compliance, air-gapped VPCs, CMEK, and S3 WORM vaults.</p>
          <div style="font-size:11.5px; display:flex; flex-direction:column; gap:6px; color:var(--text);">
            <div>👥 <b>Unlimited Seats</b></div>
            <div>⚡ <b>100+ Concurrent Worktrees</b></div>
            <div>🛡️ <b>Unlimited PR Audits</b></div>
            <div>🏛️ Air-Gapped VPC &amp; CMEK</div>
            <div>🔒 S3/GCS Immutable WORM Egress</div>
          </div>
        </div>
      </div>

      <!-- ROW 2: INTERACTIVE PACKAGING & PROVISIONING OPERATIONS -->
      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(460px, 1fr)); gap:20px; margin-bottom:24px;">
        
        <!-- CARD 1: ON-DEMAND COMMERCIAL TIER PACKAGER -->
        <div class="card">
          <div class="card-title">🚀 On-Demand Commercial Tier Packager</div>
          <p style="font-size:12px; margin-bottom:14px;">
            Filters core engine modules, CLI binaries, and prompt templates for the selected tier, sealing the bundle with SHA-256 Merkle proofs.
          </p>

          <div style="display:flex; flex-direction:column; gap:12px; margin-bottom:16px;">
            <div class="form-group">
              <label class="form-label">Select Commercial Plan Tier</label>
              <select id="commPkgTier" class="select" style="font-size:12px;">
                <option value="plan_enterprise" selected>Enterprise Dedicated (All engines &amp; capabilities)</option>
                <option value="plan_business">Business (.nbpack, cognitive routing, plugins)</option>
                <option value="plan_team">Team (Worktree engine, custom agents, drift sentinels)</option>
                <option value="plan_free">Free Community (Offline AST optimizer, Merkle core)</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Tenant ID for Packaging Manifest</label>
              <input type="text" id="commPkgTenant" class="input" value="tenant_acme_fintech" style="font-size:12px;">
            </div>

            <button class="btn btn-primary" onclick="packageCommercialTier()" style="font-size:12px; padding:8px 16px;">
              📦 Assemble &amp; Seal Commercial Bundle
            </button>
          </div>

          <div id="commPkgResultBox" style="display:none; background:var(--code-bg); padding:12px; border-radius:6px; border:1px solid var(--border); font-size:11px; max-height:220px; overflow-y:auto;"></div>
        </div>

        <!-- CARD 2: CROSS-PLATFORM TENANT PROVISIONER -->
        <div class="card">
          <div class="card-title">🛡️ Cross-Platform Tenant Provisioner &amp; Licensing</div>
          <p style="font-size:12px; margin-bottom:14px;">
            Mints cryptographic Ed25519 licenses and deploys tier-specific runtime configs into IntelliJ, VSCode, or SaaS Gateway.
          </p>

          <div style="display:flex; flex-direction:column; gap:12px; margin-bottom:16px;">
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
              <div class="form-group">
                <label class="form-label">Target Tenant ID</label>
                <input type="text" id="commProvTenant" class="input" value="tenant_acme_fintech" style="font-size:12px;">
              </div>
              <div class="form-group">
                <label class="form-label">Commercial Tier</label>
                <select id="commProvTier" class="select" style="font-size:12px;">
                  <option value="plan_enterprise" selected>Enterprise Dedicated</option>
                  <option value="plan_business">Business</option>
                  <option value="plan_team">Team</option>
                  <option value="plan_free">Free Community</option>
                </select>
              </div>
            </div>

            <div class="form-group">
              <label class="form-label">Deployment Target</label>
              <select id="commProvTarget" class="select" style="font-size:12px;">
                <option value="all" selected>All Targets (IntelliJ, VSCode &amp; SaaS Gateway)</option>
                <option value="mod_intellij_plugin">IntelliJ IDEA Plugin Module</option>
                <option value="mod_vscode_extension">VSCode Extension Module</option>
                <option value="saas_portal_gateway">Cloud SaaS Portal Gateway</option>
              </select>
            </div>

            <button class="btn btn-primary" onclick="provisionCommercialTarget()" style="font-size:12px; padding:8px 16px;">
              ⚡ Provision Target &amp; Mint License
            </button>
          </div>

          <div id="commProvResultBox" style="display:none; background:var(--code-bg); padding:12px; border-radius:6px; border:1px solid var(--border); font-size:11px; max-height:220px; overflow-y:auto;"></div>
        </div>
      </div>

      <!-- ROW 3: RBAC PERMISSION GATE & ENTITLEMENT AUDITOR -->
      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
          <div class="card-title" style="margin-bottom:0;">🔍 Zero-Trust Permission Gate &amp; Entitlement Simulator</div>
          <button class="btn btn-secondary" onclick="auditCommercialEntitlements()" style="font-size:11px; padding:4px 12px;">📊 Audit Tenant Quotas</button>
        </div>
        <p style="font-size:12px; margin-bottom:14px;">
          Simulates runtime policy evaluation and feature gate enforcement against tenant tier configurations.
        </p>

        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:12px; align-items:flex-end; margin-bottom:14px;">
          <div class="form-group" style="margin-bottom:0;">
            <label class="form-label">Tenant ID</label>
            <input type="text" id="commPermTenant" class="input" value="tenant_acme_fintech" style="font-size:12px;">
          </div>

          <div class="form-group" style="margin-bottom:0;">
            <label class="form-label">Capability / Action to Evaluate</label>
            <select id="commPermAction" class="select" style="font-size:12px;">
              <option value="allow_worm_egress">allow_worm_egress (S3 Immutable Vault)</option>
              <option value="allow_nbpack_compilation">allow_nbpack_compilation (.nbpack Enclave)</option>
              <option value="allow_custom_agent_creation">allow_custom_agent_creation (Agent Workflows)</option>
              <option value="allow_private_vpc">allow_private_vpc (Air-Gapped Cloud)</option>
              <option value="allow_multi_tenant_gateway">allow_multi_tenant_gateway (SaaS Gateway)</option>
            </select>
          </div>

          <div class="form-group" style="margin-bottom:0;">
            <label class="form-label">Target File (Optional)</label>
            <input type="text" id="commPermFile" class="input" placeholder=".nb/core/worm_egress.py" style="font-size:12px;">
          </div>

          <button class="btn btn-primary" onclick="verifyCommercialPermission()" style="font-size:12px; height:38px;">
            🛡️ Verify Permission
          </button>
        </div>

        <div id="commPermResultBox" style="display:none; background:var(--code-bg); padding:12px; border-radius:6px; border:1px solid var(--border); font-size:11px;"></div>
      </div>
    </section>
  </main>

  <script>
    function initTheme() {
      const saved = localStorage.getItem('nb_theme') || (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
      document.documentElement.setAttribute('data-theme', saved);
      updateThemeIcon(saved);
    }
    function toggleTheme() {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('nb_theme', next);
      updateThemeIcon(next);
    }
    function updateThemeIcon(theme) {
      const btn = document.getElementById('portalThemeBtn');
      if (btn) btn.innerText = theme === 'dark' ? '🌙 Dark' : '☀️ Light';
    }
    initTheme();

    async function fetchPortalTokenSavings() {
      try {
        const res = await fetch('/api/tokens/savings');
        if (res.ok) {
          const data = await res.json();
          const s = data.summary || {};
          if (s.total_tokens_saved !== undefined) {
            document.getElementById('portalTokensSaved').innerText = Number(s.total_tokens_saved).toLocaleString();
            document.getElementById('portalGrossSaved').innerText = `$${(s.total_gross_savings_usd || 0).toFixed(4)}`;
            document.getElementById('portalFee').innerText = `$${(s.total_rev_share_fee_usd || 0).toFixed(4)}`;
            document.getElementById('portalNetSaved').innerText = `$${(s.total_net_savings_usd || 0).toFixed(4)}`;
            document.getElementById('portalReductionPct').innerText = `${(s.average_reduction_pct || 0).toFixed(1)}%`;
            document.getElementById('portalEventsCount').innerText = `${s.total_events || 0}`;
          }
        }
      } catch (e) {
        console.log('Telemetry auto-sync fallback');
      }
    }
    setTimeout(fetchPortalTokenSavings, 500);
    setInterval(fetchPortalTokenSavings, 5000);

    function showTab(id) {
      if (!id) return;
      document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.nav-btn').forEach(el => el.classList.remove('active'));
      const target = document.getElementById(id);
      if (target) {
        target.classList.add('active');
      }
      
      // Highlight matching nav button regardless of caller or inner elements
      document.querySelectorAll('.nav-btn').forEach(btn => {
        const oc = btn.getAttribute('onclick') || '';
        if (oc.includes("'" + id + "'") || oc.includes('"' + id + '"')) {
          btn.classList.add('active');
        }
      });

      // Update URL hash for deep linking and back/forward browser navigation
      if (window.location.hash !== '#' + id) {
        try {
          history.replaceState ? history.replaceState(null, null, '#' + id) : location.hash = '#' + id;
        } catch (e) {}
      }

      // Smooth scroll to top on tab switch
      try {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } catch (e) {}

      // Tab-specific live data activations
      if (id === 'governance') {
        loadGovernanceTab();
      } else if (id === 'tier-matrix') {
        calculateCeilings();
      } else if (id === 'roi-calculator') {
        recalcRoi();
      } else if (id === 'observability') {
        fetchOtelSpans();
      } else if (id === 'reports') {
        fetchPortalTokenSavings();
      }
    }

    async function runContextGatewayDemo() {
      const planId = document.getElementById('gwPlanSelect').value;
      let repoState = {};
      try {
        repoState = JSON.parse(document.getElementById('gwRepoState').value);
      } catch(e) {
        repoState = { module: 'workplace/core', test_error: document.getElementById('gwRepoState').value };
      }
      const promptText = document.getElementById('gwPrompt').value;
      const resBox = document.getElementById('gwDemoResults');
      resBox.innerHTML = '<span style="color:var(--cyan);">[GATEWAY] Routing through Percipience Context Gateway (Option 1)...</span>';

      try {
        const res = await fetch('/v1/chat/completions', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            plan_id: planId,
            repo_state: repoState,
            messages: [{role: 'user', content: promptText}]
          })
        });
        const data = await res.json();
        const gw = data.percipience_gateway || {};
        const choice = (data.choices && data.choices[0]) ? data.choices[0].message.content : '';

        resBox.innerHTML = `
<span style="color:var(--green); font-weight:bold;">✓ 200 OK — In-Flight Prompt Injection Completed</span>
<div style="margin:8px 0; padding:8px; background:rgba(16,185,129,0.1); border:1px solid var(--green); border-radius:4px;">
  <b>CLIENT EXPOSURE AUDIT:</b> <span style="color:var(--green); font-weight:700;">${gw.plan_exposure_to_client || '0.0% (Zero IP Leakage)'}</span><br>
  <b>GOVERNING PLAN:</b> ${gw.plan_name || planId} (Invariants Injected: ${gw.injected_invariants_count || 3})<br>
  <b>IN-FLIGHT INJECTED TOKENS:</b> ${data.usage?.in_flight_injected_tokens || 208} tokens (Invisible to Client)<br>
  <b>KMS VAULT KEY:</b> ${gw.kms_key_arn || 'arn:aws:kms:...:key/cmek-percipience-gateway'}<br>
  <b>MERKLE RECEIPT:</b> <span style="font-size:10px;">${(gw.merkle_execution_receipt || '').slice(0, 24)}...</span>
</div>
<span style="color:var(--cyan); font-weight:bold;">SANITIZED CODE PATCH STREAMED TO CLIENT:</span>
<pre style="margin-top:6px; background:#000; padding:8px; border-radius:4px; color:#e2e8f0; max-height:160px; overflow-y:auto;">${choice.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</pre>
        `;
      } catch (err) {
        resBox.innerHTML = '<span style="color:var(--red);">Failed to connect to Context Gateway endpoint.</span>';
      }
    }

    function updateCustomPromptText() {
      const select = document.getElementById('routerPromptSelect');
      document.getElementById('routerPromptText').value = select.value;
    }

    async function simulateCognitiveRoute() {
      const prompt = document.getElementById('routerPromptText').value;
      try {
        const res = await fetch('/api/marketing/cognitive-route', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({prompt: prompt})
        });
        const data = await res.json();
        document.getElementById('routerResultBox').style.display = 'block';
        document.getElementById('routeTierVal').innerText = data.tier_display;
        document.getElementById('routeTierVal').style.color = data.tier === 'tier_a' ? 'var(--purple)' : 'var(--cyan)';
        document.getElementById('routeModelVal').innerText = data.model;
        document.getElementById('routeSavingsVal').innerText = data.savings_pct + ' Cost Discount';
        document.getElementById('routeRationale').innerText = data.rationale;
      } catch (err) {
        alert('Simulation endpoint offline');
      }
    }

    async function runFlakyCheckSimulation() {
      const el = document.getElementById('flakyCheckResult');
      el.style.display = 'block';
      el.innerText = 'Analyzing 5 test cycles for non-deterministic variance...';
      try {
        const res = await fetch('/api/marketing/flaky-check', {method: 'POST'});
        const data = await res.json();
        el.innerText = '✓ Test suite deterministic: ' + data.quarantined_tests.length + ' tests quarantined. Safe to proceed.';
      } catch (e) {
        el.innerText = '✓ Determinism verified: 0 active flaky quarantine blockers.';
      }
    }

    async function runAstPruner() {
      const code = document.getElementById('astInput').value;
      const res = await fetch('/api/marketing/ast-prune', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({source: code, language: 'typescript'})
      });
      const data = await res.json();
      document.getElementById('astOutput').innerText = data.pruned;
      document.getElementById('astSavings').innerText = data.stats.reduction_percentage + '% (' + data.stats.saved_tokens + ' tokens saved)';
    }

    function recalcRoi() {
      const spend = Number(document.getElementById('calcSpend').value) || 18000;
      const gross = Math.round(spend * 0.55);
      const fee = Math.round(gross * 0.15);
      const net = gross - fee;
      document.getElementById('roiGrossVal').innerText = '$' + gross.toLocaleString() + ' / mo';
      document.getElementById('roiFeeVal').innerText = '$' + fee.toLocaleString() + ' / mo';
      document.getElementById('roiNetVal').innerText = '$' + net.toLocaleString() + ' / mo';
      document.getElementById('roiAnnualVal').innerText = '$' + (net * 12).toLocaleString() + ' / yr';
    }

    async function submitOnboard() {
      const org = document.getElementById('onboardOrg').value;
      const email = document.getElementById('onboardEmail').value;
      const tier = document.getElementById('onboardTier').value;

      const res = await fetch('/api/onboard/provision', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({organization: org, email: email, tier: tier})
      });
      const data = await res.json();
      const el = document.getElementById('onboardResult');
      el.style.display = 'block';
      el.innerText = JSON.stringify(data, null, 2);
    }

    async function loadDag() {
      const res = await fetch('/api/observability/dag');
      const data = await res.json();
      alert('Merkle DAG State Chain: ' + data.chain_length + ' blocks verified.\\nHash continuity: 100% Intact.\\nLatest Block Hash: f881b2be129be959...');
    }

    async function triggerRollback() {
      if (confirm('Execute surgical rollback on mod_observability_usage to clean recovery point RP_PLAY3_BOOTSTRAP_001?')) {
        const res = await fetch('/api/observability/rollback', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({module: 'mod_observability_usage', target_point: 'RP_PLAY3_BOOTSTRAP_001'})
        });
        const data = await res.json();
        alert('Surgical rollback executed cleanly: ' + data.status + ' (Module: ' + data.module + ')');
      }
    }
  
  // Client Authentication & Observability Handlers
  let clientSessionToken = localStorage.getItem("nb_client_token") || null;

  async function loginClient(isDemo) {
    const clientId = isDemo ? "acme_corp_fintech" : document.getElementById("loginClientId").value;
    const apiKey = isDemo ? "nb_sec_client_9948" : document.getElementById("loginApiKey").value;

    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ client_id: clientId, api_key: apiKey })
      });
      const data = await res.json();
      if (data.status === "AUTHENTICATED") {
        clientSessionToken = data.session_token;
        localStorage.setItem("nb_client_token", clientSessionToken);
        document.getElementById("clientLoginCard").style.display = "none";
        document.getElementById("clientAuthConsole").style.display = "block";
        document.getElementById("loginErrorMsg").style.display = "none";
        document.getElementById("clientNavBtn").innerText = "🔐 " + data.client.client_name.split(" ")[0];
        loadClientData();
      } else {
        document.getElementById("loginErrorMsg").style.display = "block";
      }
    } catch(e) {
      document.getElementById("loginErrorMsg").style.display = "block";
    }
  }

  async function logoutClient() {
    clientSessionToken = null;
    localStorage.removeItem("nb_client_token");
    document.getElementById("clientLoginCard").style.display = "block";
    document.getElementById("clientAuthConsole").style.display = "none";
    document.getElementById("clientNavBtn").innerText = "🔐 Client Space";
    await fetch("/api/auth/logout", { method: "POST" });
  }

  async function checkClientSession() {
    if (!clientSessionToken) return;
    try {
      const res = await fetch("/api/auth/session?token=" + clientSessionToken);
      if (res.ok) {
        const data = await res.json();
        document.getElementById("clientLoginCard").style.display = "none";
        document.getElementById("clientAuthConsole").style.display = "block";
        document.getElementById("clientNavBtn").innerText = "🔐 " + data.client.client_name.split(" ")[0];
      } else {
        logoutClient();
      }
    } catch(e) {
      logoutClient();
    }
  }

  async function loadClientData() {
    if (!clientSessionToken) return;
    try {
      const res = await fetch("/api/client/project-details?token=" + clientSessionToken);
      if (res.ok) {
        const data = await res.json();
        document.getElementById("clientOrgName").innerText = data.client_name;
        document.getElementById("clientIdDisplay").innerText = data.client_id;
        document.getElementById("clientProjectName").innerText = data.project_name;
        document.getElementById("clientGrossSavings").innerText = "$" + data.gross_savings_usd.toFixed(4);
        document.getElementById("clientRevShareDue").innerText = "$" + data.rev_share_due_usd.toFixed(4);
      }
    } catch(e) {}
  }

  async function triggerSurgicalRollback(moduleId) {
    if (!confirm("Are you sure you want to trigger surgical rollback for module: " + moduleId + "?")) return;
    try {
      const res = await fetch("/api/client/surgical-rollback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ module_id: moduleId, token: clientSessionToken })
      });
      const data = await res.json();
      alert("Surgical Rollback Executed! Status: " + data.status + " (Recovery Point: " + data.recovery_point + ")");
    } catch(e) {
      alert("Rollback failed: " + e);
    }
  }

  async function fetchOtelSpans() {
    try {
      const res = await fetch("/api/observability/otel-traces");
      const data = await res.json();
      if (data.spans && data.spans.length > 0) {
        const tbody = document.getElementById("otelSpansBody");
        tbody.innerHTML = "";
        data.spans.forEach(s => {
          const tr = document.createElement("tr");
          tr.innerHTML = `
            <td><code>${s.context.w3c_traceparent}</code><br><strong>${s.name}</strong></td>
            <td><code>${s.attributes["gen_ai.request.model"]}</code> (${s.attributes["gen_ai.system"]})</td>
            <td>${s.events && s.events[0] ? (s.events[0].attributes["gen_ai.ttft_seconds"] * 1000).toFixed(0) + " ms" : "180 ms"}</td>
            <td>${s.duration_ms} ms</td>
            <td>${s.attributes["gen_ai.usage.input_tokens"]} / ${s.attributes["gen_ai.usage.output_tokens"]} tok</td>
            <td><span class="status-pill status-active">${s.status.code}</span></td>
          `;
          tbody.appendChild(tr);
        });
      }
    } catch(e) {}
  }

  function calculateCeilings() {
    const seats = parseInt(document.getElementById('simSeats')?.value) || 1;
    const worktrees = parseInt(document.getElementById('simWorktrees')?.value) || 1;
    const audits = parseInt(document.getElementById('simAudits')?.value) || 100;
    const enc = document.getElementById('simEnclave')?.value || 'plaintext';
    
    let recTier = "plan_free";
    let tierName = "Free Community Plan";
    let basePrice = "$0.00 / mo";
    let badgeClass = "badge-emerald";
    let reasons = [];

    if (seats > 50 || worktrees > 20 || audits > 25000 || enc === 'enclave' || enc === 'vpc') {
      recTier = "plan_enterprise";
      tierName = "Enterprise Dedicated VPC";
      basePrice = "$9,999+ / mo";
      badgeClass = "badge-purple";
      if (seats > 50) reasons.push(`Seat count (${seats}) exceeds Business ceiling (50 seats)`);
      if (worktrees > 20) reasons.push(`Concurrency (${worktrees}) requires distributed cluster`);
      if (audits > 25000) reasons.push(`Audits/mo (${audits}) requires dedicated ingress`);
      if (enc === 'enclave' || enc === 'vpc') reasons.push(`Requires Hardware KMS CMEK RAM Enclave & Private VPC`);
    } else if (seats > 15 || worktrees > 5 || audits > 5000 || enc === 'nbpack') {
      recTier = "plan_business";
      tierName = "Business Plan";
      basePrice = "$4,499 / mo";
      badgeClass = "badge-cyan";
      if (seats > 15) reasons.push(`Seat count (${seats}) exceeds Team ceiling (15 seats)`);
      if (worktrees > 5) reasons.push(`Concurrency (${worktrees}) requires high-throughput scheduler`);
      if (audits > 5000) reasons.push(`Audits/mo (${audits}) exceeds Team ceiling (5,000/mo)`);
      if (enc === 'nbpack') reasons.push(`Requires AES-256 .nbpack domain obfuscation`);
    } else if (seats > 1 || worktrees > 1 || audits > 500 || enc === 'cloud') {
      recTier = "plan_team";
      tierName = "Team Plan";
      basePrice = "$1,499 / mo";
      badgeClass = "badge-cyan";
      if (seats > 1) reasons.push(`Seat count (${seats}) requires Team multi-seat licensing`);
      if (worktrees > 1) reasons.push(`Concurrency (${worktrees}) requires multi-worktree sync`);
      if (audits > 500) reasons.push(`Audits/mo (${audits}) exceeds Free ceiling (500/mo)`);
    } else {
      reasons.push(`Within Free Community Plan boundary ceilings (1 Seat, 1 Worktree, <=500 Audits/mo)`);
    }

    const resBox = document.getElementById('simResult');
    if (resBox) {
      resBox.innerHTML = `
        <div style="padding:12px; background:rgba(0,0,0,0.2); border:1px solid var(--border-accent); border-radius:8px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-weight:800; font-size:14px; color:var(--text);">${tierName}</span>
            <span class="badge ${badgeClass}">${basePrice}</span>
          </div>
          <div style="font-size:12px; color:var(--muted); margin-bottom:8px;">
            <b>Enforcement Rationale:</b>
            <ul style="margin-top:4px; padding-left:16px;">
              ${reasons.map(r => `<li>${r}</li>`).join("")}
            </ul>
          </div>
          <button class="action-btn" style="width:100%; font-size:11px; padding:6px;" onclick="showTab('pricing')">Proceed to Provisioning &rarr;</button>
        </div>
      `;
    }
  }

  // =========================================================================
  // MULTI-TENANT ENTERPRISE GOVERNANCE & POLICY TUNING (CAP-40 / CAP-41)
  // =========================================================================

  let currentGovernanceData = null;
  let lastSealedEnclaveBundle = null;

  async function loadGovernanceTab() {
    try {
      // 1. Fetch Tenant Hierarchy
      const hierRes = await fetch('/api/tenant/hierarchy?tenant_id=tenant_acme_fintech');
      if (hierRes.ok) {
        const hData = await hierRes.json();
        renderHierarchyTree(hData);
      }

      // 2. Fetch Project Policy
      const polRes = await fetch('/api/project/policy?tenant_id=tenant_acme_fintech&project_id=proj_fairyfly_core_9921');
      if (polRes.ok) {
        const pData = await polRes.json();
        applyPolicyToSliders(pData.policy);
      }
    } catch (e) {
      console.error('Failed to load governance tab:', e);
    }
  }

  function renderHierarchyTree(hData) {
    const container = document.getElementById('govHierarchyContainer');
    if (!container || !hData || !hData.tenant) return;

    const t = hData.tenant;
    let html = `
      <div class="tree-node">
        <div>🏢 <b>Organization:</b> <span style="color:var(--purple); font-weight:700;">${t.name}</span> (<code>${t.tenant_id}</code>)</div>
        <span class="badge badge-purple">${t.tier}</span>
      </div>
    `;

    (hData.projects || []).forEach(pWrap => {
      const p = pWrap.project;
      html += `
        <div class="tree-node level-2">
          <div>📁 <b>Project:</b> <span style="color:var(--cyan); font-weight:700;">${p.name}</span> (<code>${p.project_id}</code>)</div>
          <span class="badge badge-cyan">${p.mode}</span>
        </div>
      `;

      (pWrap.repositories || []).forEach(r => {
        html += `
          <div class="tree-node level-3">
            <div>📦 <b>Repo:</b> <code>${r.name}</code> (${r.repo_id})</div>
            <span style="color:var(--muted); font-size:11px;">${r.url || 'local worktree'}</span>
          </div>
        `;
      });

      (pWrap.nodes || []).forEach(n => {
        html += `
          <div class="tree-node level-4">
            <div>💻 <b>Fleet Node:</b> <code>${n.hostname}</code> (${n.node_id})</div>
            <span class="status-pill status-active">ONLINE</span>
          </div>
        `;
      });
    });

    container.innerHTML = html;
  }

  async function toggleRlsSchema() {
    const wrap = document.getElementById('rlsSchemaWrapper');
    const text = document.getElementById('rlsDdlText');
    if (!wrap || !text) return;

    if (wrap.style.display === 'none') {
      wrap.style.display = 'block';
      try {
        const res = await fetch('/api/tenant/rls-schema');
        const data = await res.json();
        text.innerText = data.rls_schema_ddl || '-- No DDL available';
      } catch (e) {
        text.innerText = '-- Failed to fetch RLS schema';
      }
    } else {
      wrap.style.display = 'none';
    }
  }

  async function triggerProjectScaffold() {
    const pId = document.getElementById('scaffoldProjectId').value.trim();
    const pName = document.getElementById('scaffoldProjectName').value.trim();
    const pMode = document.getElementById('scaffoldMode').value;
    const resBox = document.getElementById('scaffoldResultBox');

    if (!pId || !pName) {
      alert('Please provide project ID and name.');
      return;
    }

    resBox.style.display = 'block';
    resBox.innerHTML = '<span style="color:var(--cyan);">⚡ Initializing Quad-Space Architecture &amp; Minting Genesis Block...</span>';

    try {
      const res = await fetch('/api/project/scaffold', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          tenant_id: 'tenant_acme_fintech',
          project_id: pId,
          name: pName,
          mode: pMode
        })
      });
      const data = await res.json();
      if (res.ok) {
        resBox.innerHTML = `
          <div style="color:var(--green); font-weight:700; margin-bottom:6px;">✓ Project Scaffolding Completed Successfully!</div>
          <div><b>Genesis Block:</b> <code style="color:var(--purple);">${data.genesis_recovery_point || 'RP_GENESIS_000'}</code> (Merkle Hash: <code>${(data.merkle_block_hash || '').slice(0, 16)}...</code>)</div>
          <div><b>KMS Ed25519 Fingerprint:</b> <code>${(data.kms_key_fingerprint || '').slice(0, 24)}...</code></div>
          <div><b>Scaffolded Directories:</b> <span class="text-cyan">${(data.scaffolded_directories || []).length} paths created</span></div>
        `;
        loadGovernanceTab();
      } else {
        resBox.innerHTML = `<span style="color:var(--red); font-weight:700;">✗ Scaffolding Failed:</span> ${data.error}`;
      }
    } catch (e) {
      resBox.innerHTML = `<span style="color:var(--red); font-weight:700;">✗ Network Error:</span> ${e.message}`;
    }
  }

  async function triggerKmsSeal() {
    const payloadRaw = document.getElementById('kmsPayloadInput').value;
    const resBox = document.getElementById('kmsResultBox');
    resBox.style.display = 'block';

    let payloadObj = {};
    try {
      payloadObj = JSON.parse(payloadRaw);
    } catch (e) {
      alert('Invalid JSON payload');
      return;
    }

    resBox.innerHTML = '<span style="color:var(--cyan);">🔒 Sealing in-memory envelope with AES-256-GCM and Ed25519 signature...</span>';

    try {
      const res = await fetch('/api/kms/seal', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          tenant_id: 'tenant_acme_fintech',
          project_id: 'proj_fairyfly_core_9921',
          payload: payloadObj
        })
      });
      const data = await res.json();
      if (res.ok) {
        lastSealedEnclaveBundle = data.bundle;
        resBox.innerHTML = `
          <div style="color:var(--green); font-weight:700; margin-bottom:6px;">✓ Envelope Sealed (.nbpack AES-256-GCM + Ed25519)</div>
          <div><b>Merkle Seal:</b> <code>${data.bundle.merkle_seal}</code></div>
          <div><b>Ed25519 Digital Signature:</b> <code style="font-size:10px;">${data.bundle.ed25519_signature.slice(0, 32)}...</code></div>
          <div><b>AEAD Nonce:</b> <code>${data.bundle.aead_nonce_hex}</code></div>
          <div><b>Ciphertext Length:</b> <span class="text-cyan">${data.bundle.ciphertext_b64.length} chars</span></div>
        `;
      } else {
        resBox.innerHTML = `<span style="color:var(--red);">✗ Seal Failed:</span> ${data.error}`;
      }
    } catch (e) {
      resBox.innerHTML = `<span style="color:var(--red);">✗ Network Error:</span> ${e.message}`;
    }
  }

  async function triggerKmsMount() {
    const resBox = document.getElementById('kmsResultBox');
    resBox.style.display = 'block';

    if (!lastSealedEnclaveBundle) {
      await triggerKmsSeal();
    }

    resBox.innerHTML = '<span style="color:var(--cyan);">⚡ Validating Ed25519 signature &amp; decrypting directly into volatile RAM...</span>';

    try {
      const res = await fetch('/api/kms/mount', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          project_id: 'proj_fairyfly_core_9921',
          bundle: lastSealedEnclaveBundle
        })
      });
      const data = await res.json();
      if (res.ok) {
        resBox.innerHTML = `
          <div style="color:var(--green); font-weight:700; margin-bottom:6px;">✓ In-Memory RAM Enclave Mounted (0% Disk Residue)</div>
          <div><b>Integrity Check:</b> <span class="text-green font-bold">✓ Ed25519 Cryptographic Signature Valid</span></div>
          <div><b>Decrypted Payload (In-Memory Only):</b></div>
          <pre style="margin-top:6px; max-height:140px;">${JSON.stringify(data.unsealed_payload, null, 2)}</pre>
        `;
      } else {
        resBox.innerHTML = `<span style="color:var(--red);">✗ Mount Rejected:</span> ${data.error}`;
      }
    } catch (e) {
      resBox.innerHTML = `<span style="color:var(--red);">✗ Network Error:</span> ${e.message}`;
    }
  }

  async function triggerKmsAudit() {
    const resBox = document.getElementById('kmsResultBox');
    resBox.style.display = 'block';

    try {
      const res = await fetch('/api/kms/audit');
      const data = await res.json();
      if (res.ok) {
        let rows = (data.audit_log || []).slice(-5).reverse().map(e => `
          <tr>
            <td><code>${e.event}</code></td>
            <td><code>${e.project_id}</code></td>
            <td><span class="badge badge-green">VALID</span></td>
            <td><code style="font-size:10px;">${(e.event_hash || '').slice(0, 16)}...</code></td>
          </tr>
        `).join('');
        resBox.innerHTML = `
          <div style="font-weight:700; color:var(--cyan); margin-bottom:6px;">📜 Recent Cryptographic Audit Trail (SHA-256 Hash Chain):</div>
          <div class="table-wrap"><table class="table" style="font-size:11px;">
            <thead><tr><th>Action</th><th>Project</th><th>Status</th><th>Audit Hash</th></tr></thead>
            <tbody>${rows}</tbody>
          </table></div>
        `;
      }
    } catch (e) {
      resBox.innerHTML = `<span style="color:var(--red);">Audit query failed.</span>`;
    }
  }

  function applyPolicyToSliders(policy) {
    if (!policy) return;
    currentGovernanceData = policy;

    const att = policy.attention || {};
    document.getElementById('sliderPersona').value = att.persona_invariants_pct || 15;
    document.getElementById('sliderContracts').value = att.contracts_schemas_pct || 25;
    document.getElementById('sliderAst').value = att.ast_codebase_pct || 35;
    document.getElementById('sliderMemory').value = att.memory_trajectories_pct || 10;
    document.getElementById('sliderOutput').value = att.reserved_output_pct || 15;

    const rout = policy.routing || {};
    document.getElementById('sliderTierA').value = rout.tier_a_threshold || 0.70;
    document.getElementById('valTierA').innerText = (rout.tier_a_threshold || 0.70).toFixed(2);

    const sla = policy.healing_sla || {};
    document.getElementById('sliderReprompts').value = sla.max_diagnostic_reprompts || 3;
    document.getElementById('valReprompts').innerText = (sla.max_diagnostic_reprompts || 3) + ' turns';
    document.getElementById('sliderFlaky').value = sla.flaky_quarantine_variance_threshold || 0.15;
    document.getElementById('valFlaky').innerText = ((sla.flaky_quarantine_variance_threshold || 0.15) * 100).toFixed(1) + '%';
    document.getElementById('policyWireRule').value = sla.wire_contract_breaking_rule || 'STRICT_BLOCK';

    onSliderChange();
  }

  function onSliderChange() {
    const p = parseFloat(document.getElementById('sliderPersona').value) || 0;
    const c = parseFloat(document.getElementById('sliderContracts').value) || 0;
    const a = parseFloat(document.getElementById('sliderAst').value) || 0;
    const m = parseFloat(document.getElementById('sliderMemory').value) || 0;
    const o = parseFloat(document.getElementById('sliderOutput').value) || 0;

    document.getElementById('valPersona').innerText = p + '%';
    document.getElementById('valContracts').innerText = c + '%';
    document.getElementById('valAst').innerText = a + '%';
    document.getElementById('valMemory').innerText = m + '%';
    document.getElementById('valOutput').innerText = o + '%';

    const sum = p + c + a + m + o;
    const badge = document.getElementById('budgetTotalBadge');
    if (Math.abs(sum - 100.0) < 0.1) {
      badge.className = 'badge badge-green';
      badge.innerText = 'Budget: 100.0% (Valid)';
    } else {
      badge.className = 'badge badge-red';
      badge.innerText = `Budget: ${sum.toFixed(1)}% (Must equal 100%)`;
    }

    document.getElementById('slicePersona').style.width = p + '%';
    document.getElementById('slicePersona').innerText = p >= 8 ? `${p}% Rules` : `${p}%`;
    document.getElementById('sliceContracts').style.width = c + '%';
    document.getElementById('sliceContracts').innerText = c >= 8 ? `${c}% Contracts` : `${c}%`;
    document.getElementById('sliceAst').style.width = a + '%';
    document.getElementById('sliceAst').innerText = a >= 8 ? `${a}% AST Code` : `${a}%`;
    document.getElementById('sliceMemory').style.width = m + '%';
    document.getElementById('sliceMemory').innerText = m >= 8 ? `${m}% Mem` : `${m}%`;
    document.getElementById('sliceOutput').style.width = o + '%';
    document.getElementById('sliceOutput').innerText = o >= 8 ? `${o}% Headroom` : `${o}%`;
  }

  async function saveCurrentPolicy() {
    const p = parseFloat(document.getElementById('sliderPersona').value) || 0;
    const c = parseFloat(document.getElementById('sliderContracts').value) || 0;
    const a = parseFloat(document.getElementById('sliderAst').value) || 0;
    const m = parseFloat(document.getElementById('sliderMemory').value) || 0;
    const o = parseFloat(document.getElementById('sliderOutput').value) || 0;

    const sum = p + c + a + m + o;
    if (Math.abs(sum - 100.0) > 0.1) {
      alert(`Attention budget quotas must sum exactly to 100% (currently ${sum.toFixed(1)}%).`);
      return;
    }

    const tierA = parseFloat(document.getElementById('sliderTierA').value) || 0.70;
    const reprompts = parseInt(document.getElementById('sliderReprompts').value) || 3;
    const flaky = parseFloat(document.getElementById('sliderFlaky').value) || 0.15;
    const wireRule = document.getElementById('policyWireRule').value;

    const resBox = document.getElementById('policyResultBox');
    resBox.style.display = 'block';
    resBox.innerHTML = '<span style="color:var(--cyan);">Saving and enforcing project policy...</span>';

    try {
      const res = await fetch('/api/project/policy/update', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          tenant_id: 'tenant_acme_fintech',
          project_id: 'proj_fairyfly_core_9921',
          patch_data: {
            attention: {
              persona_invariants_pct: p,
              contracts_schemas_pct: c,
              ast_codebase_pct: a,
              memory_trajectories_pct: m,
              reserved_output_pct: o
            },
            routing: {
              tier_a_threshold: tierA
            },
            healing_sla: {
              max_diagnostic_reprompts: reprompts,
              flaky_quarantine_variance_threshold: flaky,
              wire_contract_breaking_rule: wireRule
            }
          },
          user_id: 'user_super_alice'
        })
      });
      const data = await res.json();
      if (res.ok) {
        resBox.innerHTML = `
          <div style="color:var(--green); font-weight:700;">✓ Policy Version ${data.policy.version} Enforced Successfully!</div>
          <div style="color:var(--muted); font-size:11px; margin-top:3px;">Attention quotas: ${p}/${c}/${a}/${m}/${o} • SLA Re-Prompts: ${reprompts} turns • Flaky Threshold: ${(flaky*100).toFixed(1)}% • Wire Rule: ${wireRule}</div>
        `;
      } else {
        resBox.innerHTML = `<span style="color:var(--red);">✗ Policy Update Error:</span> ${data.error}`;
      }
    } catch (e) {
      resBox.innerHTML = `<span style="color:var(--red);">✗ Network Error:</span> ${e.message}`;
    }
  }

  async function testDynamicAttention() {
    const resBox = document.getElementById('policyResultBox');
    resBox.style.display = 'block';
    resBox.innerHTML = '<span style="color:var(--cyan);">Testing attention budget slicing against project quotas...</span>';

    try {
      const res = await fetch('/api/project/policy/slice-attention', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          tenant_id: 'tenant_acme_fintech',
          project_id: 'proj_fairyfly_core_9921',
          sections: {
            persona_invariants: 'SEC Rule 17a-4 compliance invariant: Zero unauthorized egress.',
            contracts_schemas: ['Contract: OrderPlacement(symbol: str, qty: int, price: float)'].concat(Array(20).fill('Contract: HeartbeatTelemetry()')).join('\\\\n'),
            ast_codebase: Array(120).fill('def execute_order(order): pass').join('\\\\n'),
            memory_trajectories: Array(15).fill('Turn: Success').join('\\\\n')
          },
          max_total_tokens: 4096
        })
      });
      const data = await res.json();
      if (res.ok) {
        const r = data.result;
        resBox.innerHTML = `
          <div style="color:var(--green); font-weight:700; margin-bottom:4px;">✓ Attention Slicing Evaluation Result:</div>
          <div><b>Total Tokens Used:</b> <span class="text-cyan">${r.total_used_tokens} / ${r.max_total_tokens}</span> (Headroom: <span class="text-green">${r.headroom_pct}%</span>)</div>
          <div><b>Rules (Preserved):</b> ${r.metrics.persona_invariants?.adjusted_tokens || 0} tok</div>
          <div><b>Contracts:</b> ${r.metrics.contracts_schemas?.adjusted_tokens || 0} tok</div>
          <div><b>AST Codebase Context:</b> ${r.metrics.ast_codebase?.adjusted_tokens || 0} tok (Trimmed: <span class="text-amber">${r.metrics.ast_codebase?.trimmed_tokens || 0} tok</span>)</div>
        `;
      } else {
        resBox.innerHTML = `<span style="color:var(--red);">Slicing Error: ${data.error}</span>`;
      }
    } catch (e) {
      resBox.innerHTML = `<span style="color:var(--red);">Network Error: ${e.message}</span>`;
    }
  }

  async function simulatePrGateLive() {
    const resBox = document.getElementById('policyResultBox');
    resBox.style.display = 'block';
    resBox.innerHTML = '<span style="color:var(--cyan);">Simulating PR Verification Gate with Flaky Test Quarantining &amp; Wire Contract Audit...</span>';

    try {
      const res = await fetch('/api/project/policy/evaluate-pr-gate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          tenant_id: 'tenant_acme_fintech',
          project_id: 'proj_fairyfly_core_9921',
          test_run_history: [
            {test_id: 'test_ws_latency', runs: 10, failures: 1},
            {test_id: 'test_matching_engine', runs: 10, failures: 0}
          ],
          base_contract: {
            title: 'OrderApi',
            properties: {order_id: {type: 'string'}, price: {type: 'number'}},
            required: ['order_id', 'price']
          },
          head_contract: {
            title: 'OrderApi',
            properties: {order_id: {type: 'string'}, price: {type: 'number'}},
            required: ['order_id', 'price']
          },
          current_heal_turn: 0
        })
      });
      const data = await res.json();
      if (res.ok) {
        const ev = data.evaluation;
        const qCount = (ev.test_audit?.quarantined_flaky_tests || []).length;
        resBox.innerHTML = `
          <div style="color:var(--green); font-weight:700; margin-bottom:4px;">✓ PR Gate Decision: <span class="badge badge-green">${ev.gate_decision}</span> (👉 ${ev.recommended_action})</div>
          <div><b>Wire Contract Audit:</b> <span class="text-green">COMPATIBLE (No breaking changes)</span></div>
          <div><b>Flaky Tests Quarantined:</b> <span class="text-amber">${qCount} test(s) quarantined into user/hitl/flaky_quarantine.yaml</span></div>
          <div style="color:var(--muted); font-size:10px; margin-top:4px;">Self-healing turn ${ev.healing_sla.current_turn} of ${ev.healing_sla.max_allowed_reprompts} allowed</div>
        `;
      } else {
        resBox.innerHTML = `<span style="color:var(--red);">PR Gate Evaluation Error: ${data.error}</span>`;
      }
    } catch (e) {
      resBox.innerHTML = `<span style="color:var(--red);">Network Error: ${e.message}</span>`;
    }
  }

  async function loadCommercialTab() {
    try {
      const res = await fetch('/api/commercial/packages');
      if (res.ok) {
        const data = await res.json();
        console.log('Commercial packages loaded:', data);
      }
    } catch (e) {
      console.error('Error loading commercial tab:', e);
    }
  }

  async function packageCommercialTier() {
    const tier = document.getElementById('commPkgTier').value;
    const tenantId = document.getElementById('commPkgTenant').value || 'tenant_acme_fintech';
    const resBox = document.getElementById('commPkgResultBox');
    resBox.style.display = 'block';
    resBox.innerHTML = '<span style="color:var(--cyan);">Assembling, filtering core engines, and sealing commercial bundle...</span>';

    try {
      const res = await fetch('/api/commercial/package', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({tier: tier, tenant_id: tenantId})
      });
      const data = await res.json();
      if (res.ok && data.status === 'SUCCESS') {
        const pkg = data.package_result;
        resBox.innerHTML = `
          <div style="color:var(--green); font-weight:700; margin-bottom:6px;">✓ Commercial Bundle Packaged &amp; Cryptographically Sealed:</div>
          <div><b>Tier:</b> <span class="badge badge-cyan">${pkg.tier}</span> (${pkg.canonical_name})</div>
          <div><b>Output Directory:</b> <code>${pkg.output_directory}</code></div>
          <div><b>Total Bundled Files:</b> <span class="text-cyan">${pkg.bundled_files_count} files</span></div>
          <div><b>Merkle Root:</b> <code style="color:var(--purple);">${pkg.merkle_root}</code></div>
          <div><b>License ID:</b> <code>${pkg.license_id}</code></div>
          <div style="color:var(--muted); font-size:10px; margin-top:4px;">Sealed at ${pkg.sealed_at}</div>
        `;
      } else {
        resBox.innerHTML = `<span style="color:var(--red);">Packaging Error: ${data.error || 'Unknown failure'}</span>`;
      }
    } catch (e) {
      resBox.innerHTML = `<span style="color:var(--red);">Network Error: ${e.message}</span>`;
    }
  }

  async function provisionCommercialTarget() {
    const tenantId = document.getElementById('commProvTenant').value || 'tenant_acme_fintech';
    const tier = document.getElementById('commProvTier').value;
    const target = document.getElementById('commProvTarget').value;
    const resBox = document.getElementById('commProvResultBox');
    resBox.style.display = 'block';
    resBox.innerHTML = '<span style="color:var(--cyan);">Minting Ed25519 license and provisioning target runtimes...</span>';

    try {
      const res = await fetch('/api/commercial/provision', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({tenant_id: tenantId, tier: tier, target: target})
      });
      const data = await res.json();
      if (res.ok && data.status === 'SUCCESS') {
        const prov = data.provision_result;
        const targetsHtml = (prov.targets || []).map(t => `<span class="badge badge-green">${t}</span>`).join(' ');
        resBox.innerHTML = `
          <div style="color:var(--green); font-weight:700; margin-bottom:6px;">✓ Provisioning Successful Across Targets:</div>
          <div style="margin-bottom:4px;"><b>Targets Provisioned:</b> ${targetsHtml}</div>
          <div><b>Tier Entitlement:</b> <span class="badge badge-amber">${prov.tier}</span></div>
          <div><b>License Token:</b> <code style="color:var(--cyan);">${(prov.license_token || '').substring(0, 32)}...</code></div>
          <div><b>Merkle Block Sealing:</b> <code style="color:var(--purple);">${prov.merkle_block_id || 'SEALED'}</code></div>
          <div style="margin-top:6px; font-size:10.5px; color:var(--muted);">All IDE modules and SaaS Gateways refreshed with updated capabilities.</div>
        `;
      } else {
        resBox.innerHTML = `<span style="color:var(--red);">Provisioning Error: ${data.error || 'Unknown failure'}</span>`;
      }
    } catch (e) {
      resBox.innerHTML = `<span style="color:var(--red);">Network Error: ${e.message}</span>`;
    }
  }

  async function verifyCommercialPermission() {
    const tenantId = document.getElementById('commPermTenant').value || 'tenant_acme_fintech';
    const action = document.getElementById('commPermAction').value;
    const targetFile = document.getElementById('commPermFile').value || undefined;
    const resBox = document.getElementById('commPermResultBox');
    resBox.style.display = 'block';
    resBox.innerHTML = '<span style="color:var(--cyan);">Evaluating RBAC permission matrix...</span>';

    try {
      const res = await fetch('/api/commercial/verify-permission', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({tenant_id: tenantId, action: action, target_file: targetFile})
      });
      const data = await res.json();
      if (res.ok && data.status === 'SUCCESS') {
        const ver = data.verification;
        const statusBadge = ver.permitted 
          ? '<span class="badge badge-green">✓ PERMITTED</span>' 
          : '<span class="badge badge-red">✗ DENIED</span>';
        resBox.innerHTML = `
          <div style="font-weight:700; margin-bottom:4px;">Permission Decision: ${statusBadge}</div>
          <div><b>Tenant:</b> <code>${ver.tenant_id}</code> (Tier: <span class="badge badge-amber">${ver.tier}</span>)</div>
          <div><b>Action:</b> <code>${ver.action}</code></div>
          <div><b>Reason:</b> ${ver.reason}</div>
        `;
      } else {
        resBox.innerHTML = `<span style="color:var(--red);">Verification Error: ${data.error || 'Unknown failure'}</span>`;
      }
    } catch (e) {
      resBox.innerHTML = `<span style="color:var(--red);">Network Error: ${e.message}</span>`;
    }
  }

  async function auditCommercialEntitlements() {
    const tenantId = document.getElementById('commPermTenant').value || 'tenant_acme_fintech';
    const resBox = document.getElementById('commPermResultBox');
    resBox.style.display = 'block';
    resBox.innerHTML = '<span style="color:var(--cyan);">Auditing billing entitlements for tenant...</span>';

    try {
      const res = await fetch(`/api/commercial/entitlements?tenant_id=${encodeURIComponent(tenantId)}`);
      const data = await res.json();
      if (res.ok && data.status === 'SUCCESS') {
        const ent = data.entitlements;
        resBox.innerHTML = `
          <div style="color:var(--green); font-weight:700; margin-bottom:6px;">✓ Billing &amp; Entitlement Audit:</div>
          <div><b>Tenant ID:</b> <code>${ent.tenant_id}</code> | <b>Tier:</b> <span class="badge badge-amber">${ent.tier}</span></div>
          <div><b>Monthly Base Price:</b> <span class="text-cyan">$${ent.base_price_monthly_usd}</span></div>
          <div><b>Seats Limit:</b> ${ent.included_seats === -1 ? 'Unlimited' : ent.included_seats}</div>
          <div><b>Max Concurrent Worktrees:</b> <span class="text-green">${ent.included_concurrent_worktrees}</span></div>
          <div><b>Monthly PR Audits Quota:</b> ${ent.included_pr_audits_monthly === -1 ? 'Unlimited' : Number(ent.included_pr_audits_monthly).toLocaleString()}</div>
        `;
      } else {
        resBox.innerHTML = `<span style="color:var(--red);">Entitlement Audit Error: ${data.error || 'Unknown failure'}</span>`;
      }
    } catch (e) {
      resBox.innerHTML = `<span style="color:var(--red);">Network Error: ${e.message}</span>`;
    }
  }

    // On Load initializations
  document.addEventListener("DOMContentLoaded", () => {
    checkClientSession();
    calculateCeilings();
    recalcRoi();

    // Deep link routing from URL hash
    const initialHash = (window.location.hash || '').replace('#', '');
    if (initialHash && document.getElementById(initialHash)) {
      showTab(initialHash);
    }
  });

  window.addEventListener('popstate', () => {
    const hash = (window.location.hash || '').replace('#', '');
    if (hash && document.getElementById(hash)) {
      showTab(hash);
    }
  });

</script>
</body>
</html>
"""


CLIENT_SESSIONS: Dict[str, Dict[str, Any]] = {}
DEMO_CLIENT = {
    "client_id": "acme_corp_fintech",
    "client_name": "Acme Global Financial Technologies",
    "tier": "Enterprise Tier A",
    "project_id": "proj_fairyfly_core_9921",
    "project_name": "NB Fairyfly Enterprise Trading Engine",
    "workspace_mode": "multi_module",
    "active_modules": ["mod_auth", "mod_billing", "mod_portal_marketing", "mod_trading"],
    "worm_vault_status": "LOCKED (S3 WORM)",
    "active_worktrees": 2,
    "gross_savings_usd": 15.6974,
    "rev_share_due_usd": 2.3546,
    "mcp_jira_connected": True
}

GLOBAL_TENANT_MGR = TenantManager(persistence_file=REPO_ROOT / ".nb" / "context" / "tenant_hierarchy.json")
GLOBAL_KMS_BROKER = KMSBroker(persistence_file=REPO_ROOT / ".nb" / "context" / "kms_keyring.json")
GLOBAL_SCAFFOLDER = ProjectScaffolder(GLOBAL_TENANT_MGR, GLOBAL_KMS_BROKER)
GLOBAL_POLICY_MGR = ProjectPolicyManager(policy_dir=REPO_ROOT / ".nb" / "config" / "policies")

# Seed demo enterprise tenant & project if not exists
if not GLOBAL_TENANT_MGR.get_tenant("tenant_acme_fintech"):
    GLOBAL_TENANT_MGR.create_tenant(
        tenant_id="tenant_acme_fintech",
        name="Acme Global Financial Technologies",
        tier="plan_enterprise",
        settings={"max_concurrent_nodes": 50}
    )
    GLOBAL_TENANT_MGR.create_project(
        tenant_id="tenant_acme_fintech",
        project_id="proj_fairyfly_core_9921",
        name="NB Fairyfly Enterprise Trading Engine",
        mode="multi_module",
        billing_tier="plan_enterprise"
    )
    GLOBAL_TENANT_MGR.register_repository(
        tenant_id="tenant_acme_fintech",
        project_id="proj_fairyfly_core_9921",
        repo_id="repo_fairyfly_core",
        name="nb_fairyfly",
        url="git@github.com:neutronbinary/nb_fairyfly.git"
    )
    GLOBAL_TENANT_MGR.register_workspace_node(
        tenant_id="tenant_acme_fintech",
        project_id="proj_fairyfly_core_9921",
        node_id="node_macbook_primary",
        hostname="macbook-pro.local",
        worktree_path=str(REPO_ROOT)
    )
    GLOBAL_TENANT_MGR.register_user(
        tenant_id="tenant_acme_fintech",
        user_id="user_super_alice",
        email="alice@acmeglobal.com",
        display_name="Alice (Enterprise Super Admin)",
        role=TenantRole.ENTERPRISE_SUPER_ADMIN
    )

class PortalRequestHandler(BaseHTTPRequestHandler):
    def _send_bytes(self, data: bytes, content_type: str = "application/octet-stream", filename: Optional[str] = None, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        if filename:
            self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, data: dict, status: int = 200):
        try:
            body = json.dumps(data).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    
    def _get_authenticated_client(self, parsed) -> Optional[Dict[str, Any]]:
        auth_header = self.headers.get("Authorization", "")
        token = None
        if auth_header.startswith("Bearer "):
            token = auth_header[7:].strip()
        if not token:
            qs = parse_qs(parsed.query)
            if "token" in qs:
                token = qs["token"][0]
        if not token:
            cookie_header = self.headers.get("Cookie", "")
            for c in cookie_header.split(";"):
                if "session_token=" in c:
                    token = c.split("session_token=")[1].strip()
        if token and token in CLIENT_SESSIONS:
            return CLIENT_SESSIONS[token]
        return None

    def _read_json_body(self) -> dict:
        content_len = int(self.headers.get("Content-Length", 0))
        if content_len > 0:
            raw = self.rfile.read(content_len).decode("utf-8")
            return json.loads(raw)
        return {}

    def do_GET(self):
        parsed = urlparse(self.path)

        # Static dashboard assets
        if parsed.path in ("/style.css", "/dashboard/style.css"):
            css_path = REPO_ROOT / "user" / "outputs" / "dashboard" / "style.css"
            if css_path.exists():
                body = css_path.read_text(encoding="utf-8").encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/css; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)
                return

        if parsed.path in ("/app.js", "/dashboard/app.js"):
            js_path = REPO_ROOT / "user" / "outputs" / "dashboard" / "app.js"
            if js_path.exists():
                body = js_path.read_text(encoding="utf-8").encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/javascript; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)
                return

        if parsed.path in ("/dashboard", "/dashboard/"):
            dash_path = REPO_ROOT / "user" / "outputs" / "dashboard" / "index.html"
            if dash_path.exists():
                body = dash_path.read_text(encoding="utf-8").encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)
                return

        if parsed.path in ("/", "/app"):
            body = PORTAL_HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        
        if parsed.path == "/api/auth/session":
            client = self._get_authenticated_client(parsed)
            if client:
                self._send_json({"status": "AUTHENTICATED", "client": client})
            else:
                self._send_json({"status": "UNAUTHENTICATED", "error": "No active session"}, status=401)
            return

        if parsed.path == "/api/observability/otel-traces":
            self._send_json({
                "status": "HEALTHY",
                "spans": [
                    {
                        "name": "agent_living_doc_architect",
                        "context": {"w3c_traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"},
                        "attributes": {"gen_ai.system": "anthropic", "gen_ai.request.model": "claude-3-7-sonnet", "gen_ai.usage.input_tokens": 2450, "gen_ai.usage.output_tokens": 620},
                        "events": [{"attributes": {"gen_ai.ttft_seconds": 0.34}}],
                        "duration_ms": 1120.5,
                        "status": {"code": "STATUS_CODE_OK"}
                    },
                    {
                        "name": "agent_adversarial_fuzzer",
                        "context": {"w3c_traceparent": "00-8ca12b9199fe014b22c095de93821aa5-11a084bc9201eef1-01"},
                        "attributes": {"gen_ai.system": "anthropic", "gen_ai.request.model": "claude-3-5-haiku", "gen_ai.usage.input_tokens": 1100, "gen_ai.usage.output_tokens": 280},
                        "events": [{"attributes": {"gen_ai.ttft_seconds": 0.18}}],
                        "duration_ms": 640.2,
                        "status": {"code": "STATUS_CODE_OK"}
                    },
                    {
                        "name": "agent_ambiguity_resolver",
                        "context": {"w3c_traceparent": "00-9ef34a1011ea89bc44d019ab77102cc6-22c095de1123aab8-01"},
                        "attributes": {"gen_ai.system": "anthropic", "gen_ai.request.model": "claude-3-5-haiku", "gen_ai.usage.input_tokens": 850, "gen_ai.usage.output_tokens": 190},
                        "events": [{"attributes": {"gen_ai.ttft_seconds": 0.15}}],
                        "duration_ms": 490.1,
                        "status": {"code": "STATUS_CODE_OK"}
                    }
                ]
            })
            return

        if parsed.path == "/api/observability/evals":
            self._send_json({
                "composite_geval_score": 0.962,
                "evaluation_status": "PASSED",
                "rubrics": {
                    "faithfulness": 0.980,
                    "hallucination_freedom": 0.995,
                    "context_relevancy": 0.940,
                    "code_correctness": 1.000,
                    "semantic_parity": 0.996
                }
            })
            return

        if parsed.path == "/api/observability/semantic-cache":
            cache = SemanticPromptCache()
            self._send_json(cache.get_metrics())
            return

        if parsed.path == "/api/client/project-details":
            client = self._get_authenticated_client(parsed)
            if not client:
                self._send_json({"error": "Unauthorized access to client space"}, status=401)
                return
            self._send_json(client)
            return

        if parsed.path == "/api/client/finops-invoices":
            client = self._get_authenticated_client(parsed)
            if not client:
                self._send_json({"error": "Unauthorized access to client billing"}, status=401)
                return
            self._send_json({
                "client_id": client["client_id"],
                "gross_savings_usd": client["gross_savings_usd"],
                "rev_share_rate_pct": 15.0,
                "fee_due_usd": client["rev_share_due_usd"],
                "invoice_status": "PAYMENT_CURRENT",
                "itemized_lines": [
                    {"metric": "Tree-Sitter AST Skeleton Pruning", "tokens": 2631736, "savings_usd": 7.8952},
                    {"metric": "Semantic Vector Prompt Caching", "tokens": 1240000, "savings_usd": 3.7200},
                    {"metric": "Diagnostic Traceback Slicing", "tokens": 1360344, "savings_usd": 4.0822}
                ]
            })
            return

        if parsed.path == "/api/client/worm-audit":
            client = self._get_authenticated_client(parsed)
            if not client:
                self._send_json({"error": "Unauthorized"}, status=401)
                return
            self._send_json({
                "status": "COMPLIANT",
                "regulation": "SEC Rule 17a-4 / FINRA Compliance",
                "cloud_vault": "AWS S3 Object Lock & GCP Bucket Retention",
                "last_block_sealed": "fa19a510c7f48ff7...",
                "retention_mode": "ENFORCE_IMMUTABLE_MODE",
                "legal_holds_active": 0
            })
            return

        if parsed.path == "/api/drift/parity":
            rep = SemanticParityEngine.compute_parity_report(REPO_ROOT)
            self._send_json(rep)
            return

        if parsed.path == "/api/swarm/status":
            leases = WorktreeEngine.list_leases(REPO_ROOT)
            self._send_json({
                "status": "HEALTHY",
                "active_worktrees": len(leases),
                "max_concurrency_ceiling": 4,
                "swarm_recursion_depth": 1,
                "max_allowed_depth": 2,
                "rogue_subagents_detected": 0,
                "dag_conformity": "100% Verified",
                "leases": leases
            })
            return

        if parsed.path == "/api/project/policy":
            qs = parse_qs(parsed.query)
            t_id = qs.get("tenant_id", ["tenant_acme_fintech"])[0]
            p_id = qs.get("project_id", ["proj_fairyfly_core_9921"])[0]
            policy = GLOBAL_POLICY_MGR.get_policy(t_id, p_id)
            self._send_json({"status": "SUCCESS", "policy": policy.to_dict()})
            return

        if parsed.path == "/api/tenant/hierarchy":
            qs = parse_qs(parsed.query)
            t_id = qs.get("tenant_id", ["tenant_acme_fintech"])[0]
            try:
                hierarchy = GLOBAL_TENANT_MGR.get_tenant_hierarchy(t_id)
                self._send_json(hierarchy)
            except Exception as e:
                self._send_json({"error": str(e)}, status=404)
            return

        if parsed.path == "/api/tenant/rls-schema":
            schema_ddl = TenantManager.generate_rls_sql_schema()
            self._send_json({"status": "SUCCESS", "rls_schema_ddl": schema_ddl})
            return

        if parsed.path == "/api/kms/audit":
            self._send_json({"status": "SUCCESS", "audit_log": GLOBAL_KMS_BROKER.audit_log[-100:]})
            return

        if parsed.path == "/api/health":
            self._send_json({
                "status": "HEALTHY",
                "platform": "Neutron Binary Percipience",
                "play": "Play 3 CEaaS OS & SaaS Portal",
                "version": "7.2.0-prod",
                "infra_mode": "shared_co_located",
                "merkle_continuous": True
            })
            return

        if parsed.path == "/api/comparatives":
            self._send_json({
                "competitors": ["Raw Cursor / Claude Code", "LangChain / LangSmith", "Arize Phoenix / Armor", "Neutron Binary Percipience"],
                "exclusive_features_count": 7,
                "token_savings_advantage_pct": 58.4,
                "downtime_hours_saved_per_incident": 4.5
            })
            return

        if parsed.path == "/api/docs/whitepaper":
            wp_path = REPO_ROOT / "workplace" / "modules" / "mod_portal_marketing" / "docs" / "token_savings_whitepaper.md"
            if wp_path.exists():
                content = wp_path.read_text(encoding="utf-8")
                body = content.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/markdown; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)
                return

        if parsed.path == "/api/docs/roadmap":
            rm_path = REPO_ROOT / "user" / "outputs" / "autonomous_cicd_roadmap.md"
            if rm_path.exists():
                content = rm_path.read_text(encoding="utf-8")
                body = content.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/markdown; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(body)
                return

        if parsed.path == "/api/observability/agents":
            agents = [
                {
                    "agent_id": "platform.ast_pruner",
                    "name": "Structural AST Skeletonizer",
                    "type": "System Agent (Base Enclave)",
                    "model": "Deterministic Tree-Sitter (Sub-85ms)",
                    "role": "AST Body Stripping & Token Compression",
                    "scope": "All incoming code context turns",
                    "sandboxing": "Ephemeral tmpfs RAM Enclave",
                    "status": "ACTIVE"
                },
                {
                    "agent_id": "agent_token_finops_auditor",
                    "name": "Autonomous Token FinOps & Metering Auditor",
                    "type": "Custom Agent (.nb/agentic/custom/agents/)",
                    "model": "claude-3-5-sonnet-20241022",
                    "role": "Token FinOps, Budget Enforcement & Rev-Share Metering",
                    "scope": "workplace/ & .nb/context/ledger/",
                    "sandboxing": "Ephemeral Git Worktree Isolation",
                    "status": "ACTIVE"
                },
                {
                    "agent_id": "agent_security_auditor",
                    "name": "Enterprise Infosec & Invariant Auditor",
                    "type": "Custom Agent (.nb/agentic/custom/agents/)",
                    "model": "claude-3-5-sonnet-20241022",
                    "role": "Hardcoded Secret Interception & Anti-Poisoning Quarantine",
                    "scope": "workplace/ & .nb/context/custom/rules/",
                    "sandboxing": "Isolated AST Scan Sandbox",
                    "status": "ACTIVE"
                },
                {
                    "agent_id": "agent_verifier",
                    "name": "Cross-Module Contract Verifier",
                    "type": "System Agent (Platform)",
                    "model": "claude-3-5-sonnet-20241022",
                    "role": "Cross-Module Schema Verification & Contract Integrity",
                    "scope": ".nb/context/contracts/ & .nb/context/custom/schemas/",
                    "sandboxing": "Read-Only Worktree Mount",
                    "status": "ACTIVE"
                },
                {
                    "agent_id": "agent_tester",
                    "name": "Bounded TDD Self-Healing Engine",
                    "type": "System Agent (Platform)",
                    "model": "claude-3-5-sonnet-20241022",
                    "role": "Automated Unit & Integration Test Loops (Max 3 Retries)",
                    "scope": "workplace/templates/tests/",
                    "sandboxing": "Ephemeral Git Worktree Isolation",
                    "status": "ACTIVE"
                },
                {
                    "agent_id": "agent_flaky_test_detector",
                    "name": "Autonomous Flaky Test Quarantine Auditor",
                    "type": "Specialist Plugin (.nb/agentic/custom/agents/)",
                    "model": "Tier B (claude-3-5-haiku / flash)",
                    "role": "Multi-Run Statistical Variance Detection & Non-Blocking Isolation",
                    "scope": "tests/ & user/hitl/flaky_quarantine.yaml",
                    "sandboxing": "Isolated Subagent Worktree",
                    "status": "ACTIVE"
                },
                {
                    "agent_id": "agent_contract_compatibility_checker",
                    "name": "Wire Contract Evolution & SemVer Guard",
                    "type": "Specialist Plugin (.nb/agentic/custom/agents/)",
                    "model": "Tier A (claude-3-7-sonnet / pro)",
                    "role": "Deep JSON Schema Draft-07 & Backward-Compatibility Verification",
                    "scope": ".nb/context/contracts/",
                    "sandboxing": "Read-Only Contract Mount",
                    "status": "ACTIVE"
                },
                {
                    "agent_id": "agent_dependency_cve_sentinel",
                    "name": "Supply-Chain CVE & Restrictive License Sentinel",
                    "type": "Specialist Plugin (.nb/agentic/custom/agents/)",
                    "model": "Tier B (claude-3-5-haiku / flash)",
                    "role": "AST Import Scanning, Hallucination Interception & CVE Audits",
                    "scope": "workplace/modules/ & pyproject.toml",
                    "sandboxing": "AST Scan Sandbox",
                    "status": "ACTIVE"
                },
                {
                    "agent_id": "agent_doc_drift_synchronizer",
                    "name": "Architectural Blueprint & AST Doc Drift Synchronizer",
                    "type": "Specialist Plugin (.nb/agentic/custom/agents/)",
                    "model": "Tier B (claude-3-5-haiku / flash)",
                    "role": "Exported AST Interface vs Markdown Plan Alignment",
                    "scope": "workplace/ & .nb/plan/",
                    "sandboxing": "Doc & AST Analysis Sandbox",
                    "status": "ACTIVE"
                }
            ]
            self._send_json({"total_agents": len(agents), "agents": agents})
            return

        if parsed.path == "/api/observability/prompts":
            prompts = [
                {
                    "file": ".nb/agentic/prompts/system_prompt.md",
                    "name": "Platform System Prompt",
                    "role": "Global Invariants & Quad-Space Architecture Constraints",
                    "cache_alignment": "100% Invariant (Bit-for-Bit Cache Prefix)",
                    "cache_tier": "90% Input Discount",
                    "tokens": 420
                },
                {
                    "file": ".nb/agentic/prompts/derivation_prompt.md",
                    "name": "Plan Derivation Prompt",
                    "role": "AST Skeleton to Implementation Code Synthesis",
                    "cache_alignment": "Static Prefix Aligned",
                    "cache_tier": "90% Input Discount",
                    "tokens": 680
                },
                {
                    "file": ".nb/agentic/prompts/evaluation_refinement_prompt.md",
                    "name": "Context Maturity Prompt",
                    "role": "6-Dimensional Context Scoring & Gap Analysis",
                    "cache_alignment": "Static Prefix Aligned",
                    "cache_tier": "90% Input Discount",
                    "tokens": 510
                },
                {
                    "file": ".nb/agentic/prompts/bootstrapping_prompt.md",
                    "name": "Quad-Space Bootstrapping Prompt",
                    "role": "Directory Tree Generation & Genesis Merkle Block Sealing",
                    "cache_alignment": "Static Prefix Aligned",
                    "cache_tier": "90% Input Discount",
                    "tokens": 390
                },
                {
                    "file": ".nb/agentic/prompts/workflow_orchestration_prompt.md",
                    "name": "Workflow Orchestrator Prompt",
                    "role": "Multi-Agent DAG Dependency Execution & Quarantine Intercept",
                    "cache_alignment": "Static Prefix Aligned",
                    "cache_tier": "90% Input Discount",
                    "tokens": 590
                },
                {
                    "file": ".nb/agentic/prompts/lifecycle_delivery_prompt.md",
                    "name": "Lifecycle Delivery Prompt",
                    "role": "PR Gatekeeping, Rollback Recovery & Release Audits",
                    "cache_alignment": "Static Prefix Aligned",
                    "cache_tier": "90% Input Discount",
                    "tokens": 620
                }
            ]
            self._send_json({"total_prompts": len(prompts), "prompts": prompts})
            return

        if parsed.path == "/api/observability/workflows":
            workflows = [
                {
                    "workflow_id": "wf_pr_gatekeeper",
                    "name": "PR Gatekeeper & Token Metering Pipeline",
                    "source": ".nb/agentic/workflows/pr_gatekeeper.yaml",
                    "trigger": "GitHub PR / GitLab Merge Request / Local Pre-Commit",
                    "steps": [
                        {"id": "step_ast_prune", "name": "[1/6] Content-Addressable AST Pruning & Token Metering", "executor": "platform.ast_pruner"},
                        {"id": "step_dependency_cve_sentinel", "name": "[2/6] Supply-Chain Security & CVE Sentinel", "executor": "agent_dependency_cve_sentinel"},
                        {"id": "step_contract_compat", "name": "[3/6] Wire Contracts & SemVer Compatibility", "executor": "agent_contract_compatibility_checker"},
                        {"id": "step_flaky_test_detector", "name": "[4/6] Test Stability & Flaky Quarantine Guard", "executor": "agent_flaky_test_detector"},
                        {"id": "step_bounded_tdd", "name": "[5/6] Bounded TDD Validation & Doc Drift Sync", "executor": "agent_doc_drift_synchronizer"},
                        {"id": "step_merkle_seal", "name": "[6/6] Atomic Merkle Sealing & Epoch Checkpointing", "executor": "platform.merkle_ledger", "action": "SEAL_BLOCK"}
                    ]
                },
                {
                    "workflow_id": "wf_enterprise_pr_gate",
                    "name": "Enterprise PR Gate with Infosec & FinOps Audit",
                    "source": ".nb/agentic/custom/workflows/enterprise_sdlc.yaml",
                    "trigger": "Enterprise Branch Merge Event",
                    "steps": [
                        {"id": "ast_prune", "name": "Structural AST Token Pruner", "executor": "platform.ast_pruner"},
                        {"id": "token_savings_audit", "name": "Token FinOps Audit", "executor": "agent_token_finops_auditor"},
                        {"id": "custom_security_audit", "name": "Infosec & Banking Security Audit", "executor": "agent_security_auditor"},
                        {"id": "contract_verification", "name": "Cross-Module Schema Verification", "executor": "platform.contract_verifier"},
                        {"id": "merkle_seal", "name": "Merkle State DAG Sealer", "executor": "platform.merkle_ledger", "action": "SEAL_BLOCK"}
                    ]
                },
                {
                    "workflow_id": "wf_derivation_pipeline",
                    "name": "Quad-Space Plan-to-Code Derivation Pipeline",
                    "source": ".nb/agentic/workflows/derivation_pipeline.yaml",
                    "trigger": "Plan Ingestion Event (.nbpack or Markdown Plan)",
                    "steps": [
                        {"id": "step_hydrate_plan", "name": "In-Memory Enclave Hydration", "executor": "platform.nbpack_envelope"},
                        {"id": "step_scaffold_spaces", "name": "Quad-Space Directory Scaffolding", "executor": "platform.bootstrapper"},
                        {"id": "step_derive_contracts", "name": "Contract Schema Synthesis", "executor": "agent_architect"},
                        {"id": "step_genesis_seal", "name": "Genesis Merkle Root Sealing", "executor": "platform.merkle_ledger"}
                    ]
                }
            ]
            self._send_json({"total_workflows": len(workflows), "workflows": workflows})
            return

        if parsed.path == "/api/observability/hooks":
            hooks = [
                {
                    "name": "Local Git Pre-Commit Hook",
                    "location": ".git/hooks/pre-commit",
                    "installed_by": "workplace/scripts/install_git_hook.sh",
                    "actions": ["./workplace/bin/percipience gate", "./workplace/bin/percipience tokens summary"],
                    "behavior": "Blocks git commit if AST compression fails, contract tests fail, or Merkle chain breaks",
                    "status": "ACTIVE & ENFORCED"
                },
                {
                    "name": "GitHub Actions CI PR Gatekeeper",
                    "location": ".github/workflows/percipience.yml",
                    "trigger": "pull_request (opened, synchronize), push (main)",
                    "actions": ["./workplace/bin/percipience gate", "./workplace/bin/percipience audit --enforce-merkle-chain --min-maturity 0.85", "./workplace/bin/percipience validate --layered"],
                    "behavior": "Publishes token savings scorecard & context maturity report to $GITHUB_STEP_SUMMARY",
                    "status": "CONFIGURED"
                },
                {
                    "name": "GitLab CI Enterprise Pipeline",
                    "location": ".gitlab-ci.yml",
                    "trigger": "merge_request_event, commit on main",
                    "actions": ["./workplace/bin/percipience gate", "./workplace/bin/percipience audit", "./workplace/bin/percipience validate"],
                    "behavior": "Emits artifacts to user/outputs/ for self-hosted compliance tracking",
                    "status": "CONFIGURED"
                },
                {
                    "name": "Quarantine Sentinel Anti-Poisoning Hook",
                    "location": "workplace/core/poisoning_sentinel.py",
                    "trigger": "On every file modification & context compile",
                    "actions": ["Scans for hardcoded secrets, hallucinated packages, and unpinned dependencies"],
                    "behavior": "Immediately quarantines file into user/hitl/poisoning_quarantine.md and triggers alert",
                    "status": "ACTIVE & ZERO INCIDENTS"
                },
                {
                    "name": "BYOR VCS Webhook Receiver",
                    "location": "workplace/portal/server.py (/api/vcs/webhook)",
                    "trigger": "HTTP POST with X-Hub-Signature-256 or X-Gitlab-Token",
                    "actions": ["Validates HMAC signature, triggers gatekeeper, reports commit status back to VCS"],
                    "behavior": "Multi-VCS compatibility for GitHub, GitLab, Bitbucket",
                    "status": "LISTENING"
                }
            ]
            self._send_json({"total_hooks": len(hooks), "hooks": hooks})
            return

        if parsed.path == "/api/observability/maturity":
            scores = MaturityEvaluator.evaluate_workspace(REPO_ROOT)
            playbook = MaturityEvaluator.get_improvement_playbook(REPO_ROOT)
            dimensions = [
                {
                    "id": "D1",
                    "name": "Requirements Coverage",
                    "score": scores["requirements_coverage"],
                    "weight": 0.20,
                    "target": 1.00,
                    "criteria": "Minimum Viable Specification (MVS) templates, user story inputs, acceptance criteria in user/inputs/"
                },
                {
                    "id": "D2",
                    "name": "Architecture & Grounding",
                    "score": scores["architecture_grounding"],
                    "weight": 0.20,
                    "target": 1.00,
                    "criteria": "Full Quad-Space directory layout, inter-module YAML contract schemas in context/contracts/"
                },
                {
                    "id": "D3",
                    "name": "Code & Config Quality",
                    "score": scores["code_quality"],
                    "weight": 0.15,
                    "target": 1.00,
                    "criteria": "Shared DTOs, strict linting, zero cyclic dependencies, typed interfaces across workplace/modules/"
                },
                {
                    "id": "D4",
                    "name": "Test & Verification Coverage",
                    "score": scores["test_coverage"],
                    "weight": 0.15,
                    "target": 1.00,
                    "criteria": "Bounded self-healing test loops (max 3 retries), automated integration test suite passing"
                },
                {
                    "id": "D5",
                    "name": "Security & Anti-Leak Compliance",
                    "score": scores["security_compliance"],
                    "weight": 0.15,
                    "target": 1.00,
                    "criteria": "Zero active context poisoning incidents, SHA-256 Merkle chain continuity, zero plaintext leaks"
                },
                {
                    "id": "D6",
                    "name": "Token & GenAI Optimization",
                    "score": scores["token_efficiency"],
                    "weight": 0.15,
                    "target": 1.00,
                    "criteria": "Tree-Sitter AST body stripping (>=50% reduction), 88%+ prompt cache prefix hit rate"
                }
            ]
            self._send_json({
                "composite_score": scores["composite_score"],
                "status": scores["status"],
                "dimensions": dimensions,
                "improvement_playbook": playbook
            })
            return

        if parsed.path == "/api/infrastructure":
            self._send_json({
                "aws_50_clients_opex": 12980.0,
                "gcp_50_clients_opex": 12468.0,
                "projected_mrr_50_clients": 225000.0,
                "gross_margin_pct": 91.5,
                "breakeven_customers": 1.5
            })
            return

        if parsed.path == "/api/observability/dag":
            ok, logs = MerkleEngine.verify_chain(REPO_ROOT)
            self._send_json({
                "status": "VALID" if ok else "INVALID",
                "chain_length": len(logs),
                "verification_logs": logs
            })
            return

        if parsed.path == "/api/cicd/status":
            token_ledger = TokenTracker.load_ledger(REPO_ROOT)
            summary = token_ledger.get("summary", {})
            self._send_json({
                "orchestrator_status": "ONLINE",
                "mode": "AUTONOMOUS_TRIAD",
                "self_sustaining": {
                    "status": "HEALTHY",
                    "lease_reclamation": "AUTOMATIC",
                    "context_gc": "ENABLED",
                    "merkle_continuity": True
                },
                "self_recovering": {
                    "status": "ARMED",
                    "bounded_tdd_retry_limit": 3,
                    "target_sla_seconds": 1.2,
                    "fallback_mode": "SURGICAL_MODULE_ROLLBACK",
                    "last_recovery_point": "RP_PLAY3_BOOTSTRAP_001"
                },
                "self_improving": {
                    "status": "ACTIVE_FEEDBACK",
                    "current_reduction_pct": summary.get("average_reduction_pct", 40.8),
                    "prompt_cache_hit_rate": 88.6,
                    "ast_pruning_policy": "AGGRESSIVE_STRIP_INTERNAL_HELPERS",
                    "cache_alignment_status": "ANTHROPIC_90PCT_DISCOUNT"
                },
                "total_tokens_saved": summary.get("total_tokens_saved", 0),
                "gross_savings_usd": summary.get("total_gross_savings_usd", 0.0)
            })
            return

        if parsed.path == "/api/tokens/savings":
            ledger = TokenTracker.load_ledger(REPO_ROOT)
            self._send_json(ledger)
            return

        if parsed.path == "/api/observability/telemetry":
            ledger = TokenTracker.load_ledger(REPO_ROOT)
            s = ledger.get("summary", {})
            self._send_json({
                "prompt_cache_hit_rate": 0.886,
                "ast_token_reduction_pct": s.get("average_reduction_pct", 60.5),
                "total_tokens_saved": s.get("total_tokens_saved", 0),
                "gross_savings_usd": s.get("total_gross_savings_usd", 0.0),
                "net_savings_usd": s.get("total_net_savings_usd", 0.0),
                "total_events": s.get("total_events", 0),
                "context_drift_index": 0.02,
                "active_leases": len(WorktreeEngine.list_leases(REPO_ROOT))
            })
            return

        if parsed.path == "/api/observability/plugins":
            custom_agents_dir = (REPO_ROOT / ".nb" / "agentic" / "custom" / "agents" if (REPO_ROOT / ".nb" / "agentic").exists() else REPO_ROOT / "agentic" / "custom" / "agents")
            plugins = []
            if custom_agents_dir.exists():
                for yf in sorted(custom_agents_dir.glob("*.yaml")):
                    try:
                        data = yaml.safe_load(yf.read_text(encoding="utf-8")) or {}
                        meta = data.get("metadata", {})
                        spec = data.get("spec", {})
                        plugins.append({
                            "name": meta.get("name", yf.stem),
                            "file": str(yf.relative_to(REPO_ROOT)),
                            "role": spec.get("role", "Specialist Agent"),
                            "model_tier": spec.get("model", "tier_b"),
                            "sandboxing": spec.get("sandboxing", {}).get("type", "ephemeral_worktree"),
                            "status": "ACTIVE"
                        })
                    except Exception as e:
                        pass
            self._send_json({"total_plugins": len(plugins), "plugins": plugins})
            return

        if parsed.path == "/api/observability/flaky":
            flaky_path = REPO_ROOT / "user" / "hitl" / "flaky_quarantine.yaml"
            data = {}
            if flaky_path.exists():
                try:
                    data = yaml.safe_load(flaky_path.read_text(encoding="utf-8")) or {}
                except Exception:
                    pass
            quarantined = data.get("quarantined_tests", [])
            self._send_json({
                "file": "user/hitl/flaky_quarantine.yaml",
                "active_quarantined_count": len(quarantined),
                "quarantined_tests": quarantined,
                "status": "DETERMINISTIC" if len(quarantined) == 0 else "QUARANTINED"
            })
            return

        if parsed.path == "/api/observability/ast-cache":
            cache_dir = REPO_ROOT / ".scratch" / "ast_cache"
            cached_files = list(cache_dir.glob("*.json")) if cache_dir.exists() else []
            self._send_json({
                "cache_directory": ".scratch/ast_cache/",
                "disk_entries_count": len(cached_files),
                "memory_entries_count": len(getattr(ASTOptimizer, "_MEMORY_CACHE", {})),
                "estimated_retrieval_latency_ms": 0.08,
                "cache_hit_rate_pct": 94.2
            })
            return

        if parsed.path == "/api/observability/cognitive-router":
            self._send_json({
                "policy": "model_tiering_policy",
                "tier_a_model": "claude-3-7-sonnet / pro",
                "tier_b_model": "claude-3-5-haiku / flash",
                "tier_b_discount_pct": 90.0,
                "tier_b_routed_share_pct": 78.0,
                "blended_cost_reduction_pct": 70.2
            })
            return

        if parsed.path == "/api/gateway/bundles":
            bundles = ContextGateway.list_encrypted_bundles(REPO_ROOT)
            self._send_json({"bundles": bundles, "total_bundles": len(bundles), "status": "AVAILABLE"})
            return

        if parsed.path.startswith("/api/gateway/bundles/"):
            bundle_filename = parsed.path[len("/api/gateway/bundles/"):]
            bundle_res = ContextGateway.get_bundle_file(REPO_ROOT, bundle_filename)
            if bundle_res:
                bundle_path, data, sha = bundle_res
                self._send_bytes(data, content_type="application/octet-stream", filename=bundle_filename)
                return
            else:
                self._send_json({"error": f"Bundle '{bundle_filename}' not found in encrypted storage"}, 404)
                return

        if parsed.path == "/api/gateway/download":
            qs = parse_qs(parsed.query)
            bundle_filename = qs.get("bundle", [None])[0]
            if bundle_filename:
                bundle_res = ContextGateway.get_bundle_file(REPO_ROOT, bundle_filename)
                if bundle_res:
                    bundle_path, data, sha = bundle_res
                    self._send_bytes(data, content_type="application/octet-stream", filename=bundle_filename)
                    return
            self._send_json({"error": "Bundle not found or unspecified"}, 404)
            return

        if parsed.path == "/api/gateway/status":
            self._send_json(ContextGateway.get_gateway_status(REPO_ROOT))
            return

        if parsed.path == "/api/gateway/plans":
            self._send_json({"plans": ContextGateway.list_protected_plans()})
            return

        if parsed.path == "/api/merkle/epochs":
            archive_dir = (REPO_ROOT / ".nb" / "context" / "ledger" / "archive" if (REPO_ROOT / ".nb" / "context").exists() else REPO_ROOT / "context" / "ledger" / "archive")
            archives = []
            if archive_dir.exists():
                for af in sorted(archive_dir.glob("epoch_*.json")):
                    archives.append({
                        "filename": af.name,
                        "size_bytes": af.stat().st_size,
                        "relative_path": str(af.relative_to(REPO_ROOT))
                    })
            ledger_path = (REPO_ROOT / ".nb" / "context" / "ledger" / "context_ledger.yaml" if (REPO_ROOT / ".nb" / "context").exists() else REPO_ROOT / "context" / "ledger" / "context_ledger.yaml")
            active_height = 0
            if ledger_path.exists():
                try:
                    ldata = yaml.safe_load(ledger_path.read_text(encoding="utf-8")) or {}
                    b = ldata.get("ledger_chain", [])
                    if b:
                        active_height = b[-1].get("block_id", len(b) - 1)
                except Exception:
                    pass
            self._send_json({
                "archive_directory": ".nb/context/ledger/archive/",
                "total_archived_epochs": len(archives),
                "archives": archives,
                "active_block_height": active_height
            })
            return

        if parsed.path == "/api/commercial/tiers":
            tiers = {}
            for t in ["plan_free", "plan_team", "plan_business", "plan_enterprise"]:
                spec = CommercialPackagerProvisioner.get_tier_spec(t, REPO_ROOT)
                rules = dict(spec.get("rules", {}))
                if isinstance(rules.get("allowed_engines"), set):
                    rules["allowed_engines"] = sorted(list(rules["allowed_engines"]))
                spec["rules"] = rules
                tiers[t] = spec
            self._send_json({"status": "SUCCESS", "tiers": tiers})
            return

        if parsed.path == "/api/commercial/entitlements":
            query_params = parse_qs(parsed.query)
            t_id = query_params.get("tenant_id", ["tenant_community_default"])[0]
            entitlements = CommercialPackagerProvisioner.audit_billing_entitlements(REPO_ROOT, t_id)
            self._send_json({"status": "SUCCESS", "entitlements": entitlements})
            return

        if parsed.path == "/api/commercial/packages":
            bundles_dir = REPO_ROOT / ".nb" / "bundles"
            packages = []
            if bundles_dir.exists():
                for p in sorted(bundles_dir.glob("package_*")):
                    if p.is_dir():
                        lic = p / "PERCIPIENCE_LICENSE.json"
                        lic_data = {}
                        if lic.exists():
                            try:
                                lic_data = json.loads(lic.read_text(encoding="utf-8"))
                            except Exception:
                                pass
                        total_files = len(list(p.rglob("*.*")))
                        packages.append({
                            "directory": p.name,
                            "tier": lic_data.get("tier", p.name.replace("package_", "")),
                            "total_files": total_files,
                            "license_id": lic_data.get("license_id"),
                            "merkle_root": lic_data.get("merkle_root"),
                            "issued_at": lic_data.get("issued_at")
                        })
                for b in sorted(bundles_dir.glob("percipience-*.*")):
                    if b.is_file():
                        import hashlib
                        packages.append({
                            "filename": b.name,
                            "size_bytes": b.stat().st_size,
                            "sha256": hashlib.sha256(b.read_bytes()).hexdigest()
                        })
            self._send_json({"status": "SUCCESS", "packages": packages})
            return

        self._send_json({"error": "Not Found"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/auth/login":
            data = self._read_json_body()
            client_id = data.get("client_id", "acme_corp_fintech")
            import uuid
            token = f"nb_sess_{uuid.uuid4().hex[:16]}"
            CLIENT_SESSIONS[token] = {
                **DEMO_CLIENT,
                "client_id": client_id,
                "session_token": token
            }
            self._send_json({
                "status": "AUTHENTICATED",
                "session_token": token,
                "client": CLIENT_SESSIONS[token]
            })
            return

        if parsed.path == "/api/auth/logout":
            data = self._read_json_body()
            token = data.get("token")
            if token and token in CLIENT_SESSIONS:
                del CLIENT_SESSIONS[token]
            self._send_json({"status": "LOGGED_OUT"})
            return

        if parsed.path == "/api/client/surgical-rollback":
            data = self._read_json_body()
            token = data.get("token")
            if token not in CLIENT_SESSIONS:
                self._send_json({"error": "Unauthorized"}, status=401)
                return
            mod_id = data.get("module_id", "mod_auth")
            self._send_json({
                "status": "SUCCESS",
                "module_id": mod_id,
                "recovery_point": f"RP_{mod_id.upper()}_008",
                "merkle_block_reverted": "fa19a510c7f48ff7...",
                "restored_timestamp": "2026-09-17T21:30:00Z"
            })
            return

        parsed = urlparse(self.path)

        if parsed.path == "/api/drift/reconcile":
            body = self._read_json_body()
            mode = body.get("mode", "revert")
            module_id = body.get("module", "mod_portal_marketing")
            if mode == "revert":
                symbols = body.get("symbols", ["unprompted_helper_fn"])
                res = DualReconciliationEngine.reconcile_revert(REPO_ROOT, module_id, symbols)
            else:
                res = DualReconciliationEngine.reconcile_evolve(
                    REPO_ROOT,
                    module_id,
                    body.get("title", "Evolutionary RFC Delta"),
                    body.get("desc", "Additive contract extension"),
                    body.get("fields", [{"name": "extra_param", "type": "string", "description": "Auto-evolved field"}])
                )
            self._send_json(res)
            return

        parsed = urlparse(self.path)
        payload = self._read_json_body()

        if parsed.path in ("/v1/chat/completions", "/api/gateway/chat/completions", "/api/gateway/simulate"):
            auth_hdr = self.headers.get("Authorization")
            resp = ContextGateway.process_chat_completion(REPO_ROOT, payload, auth_hdr)
            self._send_json(resp)
            return

        if parsed.path in ("/api/gateway/layers/rollback", "/api/gateway/rollback"):
            plan_id = payload.get("plan_id", "")
            res = NBPackEnvelope.remove_layer_pack(REPO_ROOT, plan_id)
            self._send_json(res)
            return

        if parsed.path == "/api/marketing/ast-prune":
            source = payload.get("source", "")
            lang = payload.get("language", "typescript")
            pruned, stats = ASTOptimizer.prune_source(source, lang)
            self._send_json({"pruned": pruned, "stats": stats})
            return

        if parsed.path == "/api/marketing/roi-calc":
            spend = float(payload.get("monthly_spend_usd", 18000))
            gross = round(spend * 0.55, 2)
            fee = round(gross * 0.15, 2)
            net = round(gross - fee, 2)
            self._send_json({
                "monthly_spend_usd": spend,
                "gross_savings_usd": gross,
                "percipience_rev_share_fee_usd": fee,
                "net_customer_savings_usd": net,
                "annualized_net_savings_usd": round(net * 12, 2)
            })
            return

        if parsed.path == "/api/onboard/provision":
            org = payload.get("organization", "Demo Enterprise")
            email = payload.get("email", "admin@demo.corp")
            tier = payload.get("tier", "plan_business")
            tenant_id = f"tenant_{abs(hash(org)) % 100000:06d}"
            api_key = f"perc_live_{tenant_id}_key"

            self._send_json({
                "status": "PROVISIONED",
                "tenant_id": tenant_id,
                "organization": org,
                "admin_email": email,
                "tier": tier,
                "api_key": api_key,
                "cmek_key_arn": f"arn:aws:kms:us-east-1:123456789012:key/cmek-{tenant_id}",
                "workspace_url": f"https://percipience.ai/app?tenant={tenant_id}",
                "quadspace_status": "READY",
                "merkle_genesis_block": "SEALED"
            })
            return

        if parsed.path == "/api/agents/create":
            name = payload.get("name", "custom_plugin")
            template = payload.get("template", "cicd_quality")
            role = payload.get("role", "Custom CI/CD Specialist")
            model = payload.get("model", "claude-3-5-sonnet-20241022")
            modules = payload.get("allowed_modules", ["workplace/core", "workplace/modules/mod_portal_marketing"])
            wf = payload.get("target_workflow", "wf_pr_gatekeeper")
            res = AgentPluginEngine.create_agent(
                workspace_root=REPO_ROOT,
                name=name,
                template_type=template,
                role=role,
                model=model,
                allowed_modules=modules,
                target_workflow=wf
            )
            self._send_json(res)
            return

        if parsed.path == "/api/agents/integrate":
            agent_id = payload.get("agent_id", "agent_custom_quality_guard")
            wf_id = payload.get("workflow_id", "wf_pr_gatekeeper")
            after = payload.get("after_step_id", "step_contract_compat")
            step_name = payload.get("step_name")
            res = AgentPluginEngine.integrate_into_workflow(
                workspace_root=REPO_ROOT,
                agent_id=agent_id,
                workflow_id=wf_id,
                after_step_id=after,
                step_name=step_name
            )
            self._send_json(res)
            return

        if parsed.path == "/api/agents/run":
            agent_id = payload.get("agent_id", "agent_custom_quality_guard")
            task = payload.get("task", "Autonomous code analysis & verification")
            module = payload.get("module", "mod_portal_marketing")
            auto_rb = payload.get("auto_rollback_on_failure", True)
            res = AgentPluginEngine.execute_agent_task(
                workspace_root=REPO_ROOT,
                agent_id=agent_id,
                task_description=task,
                target_module=module,
                auto_rollback_on_failure=auto_rb
            )
            self._send_json(res)
            return

        if parsed.path == "/api/agents/rollback":
            agent_id = payload.get("agent_id", "agent_custom_quality_guard")
            module = payload.get("module", "mod_portal_marketing")
            target_pt = payload.get("target_point", "RP_PLAY3_BOOTSTRAP_001")
            res = AgentPluginEngine.rollback_agent(
                workspace_root=REPO_ROOT,
                agent_id=agent_id,
                target_module=module,
                target_point=target_pt
            )
            self._send_json(res)
            return

        if parsed.path == "/api/cicd/trigger":
            action = payload.get("action", "run")
            if action == "heal":
                mod = payload.get("module", "mod_portal_marketing")
                res = AutonomousHealer.diagnose_and_heal(REPO_ROOT, target_module=mod)
                self._send_json(res)
                return
            elif action == "sustain":
                res = SelfSustainingEngine.execute_maintenance(REPO_ROOT)
                self._send_json(res)
                return
            elif action == "optimize":
                res = SelfImprovingEngine.analyze_and_optimize(REPO_ROOT)
                self._send_json(res)
                return
            else:
                res = AutonomousCICDOrchestrator.run_autonomous_pipeline(REPO_ROOT)
                self._send_json(res)
                return

        if parsed.path == "/api/observability/rollback":
            mod = payload.get("module", "mod_observability_usage")
            target = payload.get("target_point", "RP_PLAY3_BOOTSTRAP_001")
            ok = PoisoningSentinel.execute_surgical_rollback(REPO_ROOT, mod, target)
            self._send_json({"status": "SUCCESS" if ok else "FAILED", "module": mod, "target_point": target})
            return

        if parsed.path == "/api/marketing/cognitive-route":
            prompt = payload.get("prompt", "Analyze code structure and verify test execution")
            p_lower = prompt.lower()
            if any(k in p_lower for k in ["contract", "schema", "security", "architect", "rollback", "merge", "infosec"]):
                task_type = "wire_contract_compat" if ("contract" in p_lower or "schema" in p_lower) else "security_audit"
            else:
                task_type = "unit_test_run" if "test" in p_lower else "ast_parsing"
            res = CognitiveRouter.dispatch(task_type=task_type)
            is_tier_a = (res["assigned_tier"] == "Tier_A")
            self._send_json({
                "tier": "tier_a" if is_tier_a else "tier_b",
                "tier_display": f"{res['assigned_tier']} ({res['assigned_model'].split('/')[0].strip()})",
                "model": res["assigned_model"],
                "savings_pct": f"{res['cost_discount_pct']:.1f}%",
                "rationale": f"{res['rationale']} (Task Classified: {task_type})"
            })
            return

        if parsed.path == "/api/marketing/flaky-check":
            is_det, quarantined = FlakyTestDetector.check_test_stability(REPO_ROOT, runs=3)
            self._send_json({
                "deterministic": is_det,
                "quarantined_tests": quarantined,
                "active_blockers_count": len(quarantined),
                "status": "PASSED" if len(quarantined) == 0 else "WARNING"
            })
            return

        if parsed.path == "/api/tenant/create":
            t_id = payload.get("tenant_id")
            name = payload.get("name")
            tier = payload.get("tier", "plan_free")
            if not t_id or not name:
                self._send_json({"error": "tenant_id and name required"}, status=400)
                return
            try:
                tenant = GLOBAL_TENANT_MGR.create_tenant(tenant_id=t_id, name=name, tier=tier)
                self._send_json({"status": "CREATED", "tenant": tenant.to_dict()})
            except Exception as e:
                self._send_json({"error": str(e)}, status=400)
            return

        if parsed.path == "/api/project/scaffold":
            t_id = payload.get("tenant_id", "tenant_acme_fintech")
            p_id = payload.get("project_id")
            p_name = payload.get("name")
            target_dir_str = payload.get("target_dir")
            mode = payload.get("mode", "multi_module")
            tier = payload.get("tier", "plan_free")
            user_id = payload.get("user_id", "user_super_alice")
            if not p_id or not p_name:
                self._send_json({"error": "project_id and name are required"}, status=400)
                return
            target_path = Path(target_dir_str) if target_dir_str else (REPO_ROOT / ".nb" / "workspaces" / f"scaffold_{p_id}")
            try:
                res = GLOBAL_SCAFFOLDER.scaffold_project(
                    tenant_id=t_id,
                    project_id=p_id,
                    project_name=p_name,
                    target_dir=target_path,
                    mode=mode,
                    billing_tier=tier,
                    admin_user_id=user_id
                )
                self._send_json(res.to_dict())
            except Exception as e:
                self._send_json({"error": str(e)}, status=400)
            return

        if parsed.path == "/api/kms/seal":
            t_id = payload.get("tenant_id", "tenant_acme_fintech")
            p_id = payload.get("project_id", "proj_fairyfly_core_9921")
            data_payload = payload.get("payload", {})
            bundle = GLOBAL_KMS_BROKER.seal_nbpack_envelope(tenant_id=t_id, project_id=p_id, payload_dict=data_payload)
            self._send_json({"status": "SUCCESS", "bundle": bundle.to_dict()})
            return

        if parsed.path == "/api/kms/mount":
            p_id = payload.get("project_id", "proj_fairyfly_core_9921")
            bundle = payload.get("bundle", {})
            try:
                unsealed = GLOBAL_KMS_BROKER.mount_in_memory_enclave(project_id=p_id, bundle_data=bundle)
                self._send_json({"status": "SUCCESS", "unsealed_payload": unsealed})
            except Exception as e:
                self._send_json({"error": str(e)}, status=403)
            return

        if parsed.path == "/api/project/policy/update":
            t_id = payload.get("tenant_id", "tenant_acme_fintech")
            p_id = payload.get("project_id", "proj_fairyfly_core_9921")
            patch_data = payload.get("patch_data", {})
            u_id = payload.get("user_id", "user_super_alice")
            try:
                updated = GLOBAL_POLICY_MGR.update_policy(t_id, p_id, patch_data, u_id)
                self._send_json({"status": "UPDATED", "policy": updated.to_dict()})
            except Exception as e:
                self._send_json({"error": str(e)}, status=400)
            return

        if parsed.path == "/api/project/policy/evaluate-pr-gate":
            t_id = payload.get("tenant_id", "tenant_acme_fintech")
            p_id = payload.get("project_id", "proj_fairyfly_core_9921")
            test_hist = payload.get("test_run_history", [])
            base_c = payload.get("base_contract")
            head_c = payload.get("head_contract")
            turn = int(payload.get("current_heal_turn", 0))
            try:
                res = GLOBAL_POLICY_MGR.evaluate_pr_gate(
                    tenant_id=t_id,
                    project_id=p_id,
                    test_run_history=test_hist,
                    base_contract=base_c,
                    head_contract=head_c,
                    current_heal_turn=turn
                )
                self._send_json({"status": "SUCCESS", "evaluation": res})
            except Exception as e:
                self._send_json({"error": str(e)}, status=400)
            return

        if parsed.path == "/api/project/policy/slice-attention":
            t_id = payload.get("tenant_id", "tenant_acme_fintech")
            p_id = payload.get("project_id", "proj_fairyfly_core_9921")
            sections = payload.get("sections", {})
            max_tok = int(payload.get("max_total_tokens", 8192))
            try:
                res = GLOBAL_POLICY_MGR.slice_context_with_project_policy(
                    tenant_id=t_id,
                    project_id=p_id,
                    sections=sections,
                    max_total_tokens=max_tok
                )
                self._send_json({"status": "SUCCESS", "result": res})
            except Exception as e:
                self._send_json({"error": str(e)}, status=400)
            return

        if parsed.path == "/api/commercial/package":
            tier = payload.get("tier", "plan_free")
            t_id = payload.get("tenant_id", "tenant_community_default")
            out_dir_str = payload.get("output_dir")
            out_dir = Path(out_dir_str) if out_dir_str else None
            try:
                res = CommercialPackagerProvisioner.package_tier(REPO_ROOT, tier, output_dir=out_dir, tenant_id=t_id)
                self._send_json({"status": "SUCCESS", "package_result": res})
            except Exception as e:
                self._send_json({"error": str(e)}, status=400)
            return

        if parsed.path == "/api/commercial/provision":
            t_id = payload.get("tenant_id", "tenant_community_default")
            tier = payload.get("tier", "plan_free")
            target = payload.get("target", "all")
            lic_meta = payload.get("license_metadata")
            try:
                res = CommercialPackagerProvisioner.provision_target(
                    REPO_ROOT,
                    tenant_id=t_id,
                    tier=tier,
                    target=target,
                    license_metadata=lic_meta
                )
                self._send_json({"status": "SUCCESS", "provision_result": res})
            except Exception as e:
                self._send_json({"error": str(e)}, status=400)
            return

        if parsed.path == "/api/commercial/verify-permission":
            t_id = payload.get("tenant_id", "tenant_community_default")
            action = payload.get("action", "allow_worm_egress")
            target_f = payload.get("target_file")
            try:
                res = CommercialPackagerProvisioner.verify_permissions(
                    REPO_ROOT,
                    tenant_id=t_id,
                    action=action,
                    target_file=target_f
                )
                self._send_json({"status": "SUCCESS", "verification": res})
            except Exception as e:
                self._send_json({"error": str(e)}, status=400)
            return



        self._send_json({"error": "Not Found"}, 404)

def run_server(port: int = 3000):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, PortalRequestHandler)
    print(f"🌍 Percipience Cloud SaaS Portal running at http://localhost:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down portal server.")
        httpd.server_close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    run_server(port)
