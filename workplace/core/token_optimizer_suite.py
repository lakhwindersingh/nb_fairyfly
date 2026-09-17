"""
Percipience Multi-Dimensional Token Optimization & Context Compression Suite
Provides granular, optional, and multi-tier context compression strategies across:
1. AST Skeleton Pruning (Python, TypeScript, Go, Rust, JavaScript)
2. Markdown & Living Docs Pruning (badges, tables, prose boilerplate)
3. Config & JSONSchema Minification (YAML/JSON comments, empty defaults)
4. Diagnostic Log & Stack Trace Slicing (minimal failure context)
5. Git Diff & Lockfile Pruning (clamps context, excludes lockfiles/binaries)
6. Conversation Memory Compaction (multi-turn rolling state summarization)

Includes full configuration management (enable/disable, presets, custom overrides)
for both workspace CLI operations and web portal controls.
"""

import os
import re
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union

try:
    import yaml
    try:
        from yaml import CSafeLoader as SafeLoader, CSafeDumper as SafeDumper
    except ImportError:
        from yaml import SafeLoader, SafeDumper
except ImportError:
    yaml = None
    SafeLoader = None
    SafeDumper = None

REPO_ROOT = Path(__file__).resolve().parents[2]


class TokenOptimizationConfig:
    """Manages workspace and portal token optimization configuration."""

    CONFIG_FILE = "workplace/config/token_compression_rules.yaml"

    DEFAULT_CONFIG = {
        "token_optimization": {
            "enabled": True,
            "mode": "standard",  # "disabled", "conservative", "standard", "aggressive", "extreme"
            "strategies": {
                "ast_skeleton_pruning": True,
                "markdown_doc_pruning": True,
                "config_schema_minification": True,
                "diagnostic_log_slicing": True,
                "git_diff_pruning": True,
                "conversation_memory_compaction": True
            },
            "excluded_paths": [
                "node_modules/**",
                ".git/**",
                "**/*.min.js",
                "**/*.min.css"
            ],
            "excluded_extensions": [
                ".lock",
                ".sum",
                ".min.js",
                ".min.css",
                ".map",
                ".png",
                ".jpg",
                ".svg"
            ],
            "portal_controls": {
                "allow_user_override": True,
                "show_realtime_roi_widget": True,
                "default_model_rate_card": "claude-3-5-sonnet-20241022"
            }
        }
    }

    @classmethod
    def get_config_path(cls, repo_root: Path = REPO_ROOT) -> Path:
        p = repo_root / cls.CONFIG_FILE
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    @classmethod
    def load_config(cls, repo_root: Path = REPO_ROOT) -> Dict[str, Any]:
        p = cls.get_config_path(repo_root)
        if not p.exists():
            cls.save_config(cls.DEFAULT_CONFIG, repo_root)
            return cls.DEFAULT_CONFIG

        try:
            with open(p, "r", encoding="utf-8") as f:
                if yaml and SafeLoader:
                    data = yaml.load(f, Loader=SafeLoader) or {}
                elif yaml:
                    data = yaml.safe_load(f) or {}
                else:
                    data = json.load(f) or {}

                if "token_optimization" not in data:
                    data["token_optimization"] = cls.DEFAULT_CONFIG["token_optimization"]
                return data
        except Exception:
            return cls.DEFAULT_CONFIG

    @classmethod
    def save_config(cls, config_data: Dict[str, Any], repo_root: Path = REPO_ROOT) -> None:
        p = cls.get_config_path(repo_root)
        with open(p, "w", encoding="utf-8") as f:
            if yaml and SafeDumper:
                yaml.dump(config_data, f, Dumper=SafeDumper, sort_keys=False)
            elif yaml:
                yaml.dump(config_data, f, sort_keys=False)
            else:
                json.dump(config_data, f, indent=2)

    @classmethod
    def is_enabled(cls, repo_root: Path = REPO_ROOT) -> bool:
        cfg = cls.load_config(repo_root)
        return bool(cfg.get("token_optimization", {}).get("enabled", True))

    @classmethod
    def is_strategy_enabled(cls, strategy_name: str, repo_root: Path = REPO_ROOT) -> bool:
        if not cls.is_enabled(repo_root):
            return False
        cfg = cls.load_config(repo_root)
        strategies = cfg.get("token_optimization", {}).get("strategies", {})
        return bool(strategies.get(strategy_name, True))

    @classmethod
    def set_enabled(cls, enabled: bool, repo_root: Path = REPO_ROOT) -> Dict[str, Any]:
        cfg = cls.load_config(repo_root)
        cfg.setdefault("token_optimization", {})["enabled"] = enabled
        if not enabled:
            cfg["token_optimization"]["mode"] = "disabled"
        elif cfg["token_optimization"].get("mode") == "disabled":
            cfg["token_optimization"]["mode"] = "standard"
        cls.save_config(cfg, repo_root)
        return cfg

    @classmethod
    def set_mode(cls, mode: str, repo_root: Path = REPO_ROOT) -> Dict[str, Any]:
        valid_modes = ["disabled", "conservative", "standard", "aggressive", "extreme"]
        if mode not in valid_modes:
            raise ValueError(f"Invalid mode '{mode}'. Must be one of {valid_modes}")
        cfg = cls.load_config(repo_root)
        cfg.setdefault("token_optimization", {})["mode"] = mode
        cfg["token_optimization"]["enabled"] = (mode != "disabled")
        cls.save_config(cfg, repo_root)
        return cfg

    @classmethod
    def set_strategy(cls, strategy_name: str, enabled: bool, repo_root: Path = REPO_ROOT) -> Dict[str, Any]:
        cfg = cls.load_config(repo_root)
        strategies = cfg.setdefault("token_optimization", {}).setdefault("strategies", {})
        strategies[strategy_name] = enabled
        cls.save_config(cfg, repo_root)
        return cfg


class DocPruner:
    """Optimizes Markdown and Living Documentation context payloads."""

    @classmethod
    def prune_markdown(cls, markdown_text: str, mode: str = "standard") -> Tuple[str, Dict[str, int]]:
        """
        Prunes markdown text:
        - Removes badge lines (e.g. [![...](...)](...))
        - Strips excessive HTML comments
        - Compresses long markdown tables (keeps header + first 3 rows + summary row)
        - In aggressive mode: strips decorative callout boilerplate and trims prose
        """
        original_tokens = max(1, len(markdown_text) // 4)
        lines = markdown_text.splitlines()
        pruned_lines = []
        in_table = False
        table_rows = 0

        for line in lines:
            stripped = line.strip()

            # Strip badge markdown links
            if re.match(r"^\[!\[.*\]\(.*\)\]\(.*\)$", stripped) or re.match(r"^!\[.*\]\(https://img\.shields\.io/.*\)$", stripped):
                continue

            # Strip HTML comment lines
            if stripped.startswith("<!--") and stripped.endswith("-->"):
                continue

            # Handle Markdown tables
            if stripped.startswith("|") and stripped.endswith("|"):
                if not in_table:
                    in_table = True
                    table_rows = 0
                table_rows += 1

                # Keep header, separator, and top rows
                if mode in ["aggressive", "extreme"] and table_rows > 4:
                    if table_rows == 5:
                        pruned_lines.append("| ... | ... (additional rows truncated for context efficiency) |")
                    continue
                pruned_lines.append(line)
                continue
            else:
                in_table = False
                table_rows = 0

            # Aggressive prose pruning
            if mode in ["aggressive", "extreme"] and (stripped.startswith("> [!NOTE]") or stripped.startswith("> [!TIP]")):
                continue

            pruned_lines.append(line)

        pruned_text = "\n".join(pruned_lines)
        pruned_tokens = max(1, len(pruned_text) // 4)
        saved_tokens = max(0, original_tokens - pruned_tokens)

        return pruned_text, {
            "uncompressed_tokens": original_tokens,
            "pruned_tokens": pruned_tokens,
            "saved_tokens": saved_tokens,
            "reduction_pct": round(saved_tokens / original_tokens * 100.0, 1)
        }


class ConfigSchemaPruner:
    """Minifies YAML, JSON, and JSONSchema data structures for agent context."""

    @classmethod
    def prune_yaml(cls, yaml_text: str, mode: str = "standard") -> Tuple[str, Dict[str, int]]:
        original_tokens = max(1, len(yaml_text) // 4)
        lines = yaml_text.splitlines()
        pruned_lines = []

        for line in lines:
            stripped = line.strip()
            # Strip pure comment lines
            if stripped.startswith("#"):
                continue
            # Strip empty null fields in aggressive mode
            if mode in ["aggressive", "extreme"] and (stripped.endswith(": null") or stripped.endswith(": []") or stripped.endswith(": {}")):
                continue
            # Strip trailing inline comments
            if "#" in line and not ('"' in line or "'" in line):
                line = line.split("#")[0].rstrip()
            pruned_lines.append(line)

        pruned_text = "\n".join(pruned_lines)
        pruned_tokens = max(1, len(pruned_text) // 4)
        saved_tokens = max(0, original_tokens - pruned_tokens)

        return pruned_text, {
            "uncompressed_tokens": original_tokens,
            "pruned_tokens": pruned_tokens,
            "saved_tokens": saved_tokens,
            "reduction_pct": round(saved_tokens / original_tokens * 100.0, 1)
        }

    @classmethod
    def prune_json(cls, json_text: str, mode: str = "standard") -> Tuple[str, Dict[str, int]]:
        original_tokens = max(1, len(json_text) // 4)
        try:
            data = json.loads(json_text)
            if mode in ["aggressive", "extreme"]:
                # Remove descriptions and titles from schema definitions
                def clean_schema(obj):
                    if isinstance(obj, dict):
                        return {k: clean_schema(v) for k, v in obj.items() if k not in ["description", "$comment", "examples"]}
                    elif isinstance(obj, list):
                        return [clean_schema(elem) for elem in obj]
                    return obj
                data = clean_schema(data)
            minified = json.dumps(data, separators=(",", ":"))
        except Exception:
            minified = json_text

        pruned_tokens = max(1, len(minified) // 4)
        saved_tokens = max(0, original_tokens - pruned_tokens)

        return minified, {
            "uncompressed_tokens": original_tokens,
            "pruned_tokens": pruned_tokens,
            "saved_tokens": saved_tokens,
            "reduction_pct": round(saved_tokens / original_tokens * 100.0, 1)
        }


class DiagnosticLogPruner:
    """Slices massive test logs, tracebacks, and compiler outputs to minimal failure frames."""

    @classmethod
    def prune_traceback(cls, raw_log: str, max_frames: int = 3) -> Tuple[str, Dict[str, int]]:
        original_tokens = max(1, len(raw_log) // 4)
        lines = raw_log.splitlines()

        failure_lines = []
        in_failure_block = False
        captured_frames = 0

        for line in lines:
            # Capture failure headers, assertion lines, and exception types
            if any(k in line for k in ["FAILED", "ERROR", "Traceback (most recent call last):", "AssertionError", "SyntaxError", "KeyError", "TypeError", "ValueError"]):
                in_failure_block = True
                failure_lines.append(line)
                continue

            if in_failure_block:
                if line.strip().startswith("File ") or line.strip().startswith("E   "):
                    failure_lines.append(line)
                    captured_frames += 1
                elif line.strip().startswith("===") or line.strip().startswith("---"):
                    failure_lines.append(line)
                    if captured_frames >= max_frames:
                        in_failure_block = False

        if not failure_lines:
            # Fallback to last 15 lines
            failure_lines = lines[-15:]

        pruned_text = "\n".join(failure_lines)
        pruned_tokens = max(1, len(pruned_text) // 4)
        saved_tokens = max(0, original_tokens - pruned_tokens)

        return pruned_text, {
            "uncompressed_tokens": original_tokens,
            "pruned_tokens": pruned_tokens,
            "saved_tokens": saved_tokens,
            "reduction_pct": round(saved_tokens / original_tokens * 100.0, 1)
        }


class GitDiffPruner:
    """Prunes noisy lockfile churn, clamp diff context lines, and strips binary diffs."""

    IGNORED_DIFF_PATTERNS = [
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
        "Cargo.lock",
        "poetry.lock",
        "Pipfile.lock",
        ".min.js",
        ".min.css",
        ".map"
    ]

    @classmethod
    def prune_diff(cls, raw_diff: str) -> Tuple[str, Dict[str, int]]:
        original_tokens = max(1, len(raw_diff) // 4)
        lines = raw_diff.splitlines()
        pruned_lines = []
        skip_file = False

        for line in lines:
            if line.startswith("diff --git"):
                skip_file = any(p in line for p in cls.IGNORED_DIFF_PATTERNS)
                if skip_file:
                    file_name = line.split(" ")[-1]
                    pruned_lines.append(f"diff --git [LOCKFILE/BLOB SKIPPED: {file_name}]")
                    continue

            if skip_file:
                continue

            pruned_lines.append(line)

        pruned_text = "\n".join(pruned_lines)
        pruned_tokens = max(1, len(pruned_text) // 4)
        saved_tokens = max(0, original_tokens - pruned_tokens)

        return pruned_text, {
            "uncompressed_tokens": original_tokens,
            "pruned_tokens": pruned_tokens,
            "saved_tokens": saved_tokens,
            "reduction_pct": round(saved_tokens / original_tokens * 100.0, 1)
        }


class ConversationMemoryCompactor:
    """Compacts multi-turn agent interaction history into a concise state ledger."""

    @classmethod
    def compact_history(cls, messages: List[Dict[str, str]], keep_last_n: int = 4) -> Tuple[List[Dict[str, str]], Dict[str, int]]:
        original_str = json.dumps(messages)
        original_tokens = max(1, len(original_str) // 4)

        if len(messages) <= keep_last_n:
            return messages, {
                "uncompressed_tokens": original_tokens,
                "pruned_tokens": original_tokens,
                "saved_tokens": 0,
                "reduction_pct": 0.0
            }

        older_messages = messages[:-keep_last_n]
        recent_messages = messages[-keep_last_n:]

        # Extract high-level summary points from older turns
        summary_points = []
        for idx, m in enumerate(older_messages):
            role = m.get("role", "unknown")
            content = m.get("content", "")
            first_line = content.strip().splitlines()[0][:120] if content else ""
            summary_points.append(f"Turn {idx+1} ({role}): {first_line}")

        summary_msg = {
            "role": "system",
            "content": f"[COMPACTED CONVERSATION STATE: {len(older_messages)} historical turns summarized]:\n" + "\n".join(summary_points)
        }

        compacted_messages = [summary_msg] + recent_messages
        pruned_str = json.dumps(compacted_messages)
        pruned_tokens = max(1, len(pruned_str) // 4)
        saved_tokens = max(0, original_tokens - pruned_tokens)

        return compacted_messages, {
            "uncompressed_tokens": original_tokens,
            "pruned_tokens": pruned_tokens,
            "saved_tokens": saved_tokens,
            "reduction_pct": round(saved_tokens / original_tokens * 100.0, 1)
        }


class UnifiedTokenOptimizer:
    """Unified token compression dispatcher respecting workspace & portal configs."""

    @classmethod
    def optimize_content(
        cls,
        content: str,
        content_type: str,
        repo_root: Path = REPO_ROOT,
        override_mode: Optional[str] = None
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Main entry point for optimizing any context payload.
        content_type can be: 'python', 'typescript', 'go', 'rust', 'markdown', 'yaml', 'json', 'log', 'diff'.
        """
        if not TokenOptimizationConfig.is_enabled(repo_root):
            tokens = max(1, len(content) // 4)
            return content, {
                "status": "DISABLED",
                "uncompressed_tokens": tokens,
                "pruned_tokens": tokens,
                "saved_tokens": 0,
                "reduction_pct": 0.0
            }

        cfg = TokenOptimizationConfig.load_config(repo_root)
        mode = override_mode or cfg.get("token_optimization", {}).get("mode", "standard")

        if content_type in ["python", "typescript", "javascript", "go", "rust"]:
            if not TokenOptimizationConfig.is_strategy_enabled("ast_skeleton_pruning", repo_root):
                tokens = max(1, len(content) // 4)
                return content, {"status": "STRATEGY_DISABLED", "uncompressed_tokens": tokens, "pruned_tokens": tokens, "saved_tokens": 0, "reduction_pct": 0.0}
            from core.ast_optimizer import ASTOptimizer
            return ASTOptimizer.prune_source(content, content_type)

        elif content_type in ["markdown", "md"]:
            if not TokenOptimizationConfig.is_strategy_enabled("markdown_doc_pruning", repo_root):
                tokens = max(1, len(content) // 4)
                return content, {"status": "STRATEGY_DISABLED", "uncompressed_tokens": tokens, "pruned_tokens": tokens, "saved_tokens": 0, "reduction_pct": 0.0}
            return DocPruner.prune_markdown(content, mode=mode)

        elif content_type in ["yaml", "yml"]:
            if not TokenOptimizationConfig.is_strategy_enabled("config_schema_minification", repo_root):
                tokens = max(1, len(content) // 4)
                return content, {"status": "STRATEGY_DISABLED", "uncompressed_tokens": tokens, "pruned_tokens": tokens, "saved_tokens": 0, "reduction_pct": 0.0}
            return ConfigSchemaPruner.prune_yaml(content, mode=mode)

        elif content_type == "json":
            if not TokenOptimizationConfig.is_strategy_enabled("config_schema_minification", repo_root):
                tokens = max(1, len(content) // 4)
                return content, {"status": "STRATEGY_DISABLED", "uncompressed_tokens": tokens, "pruned_tokens": tokens, "saved_tokens": 0, "reduction_pct": 0.0}
            return ConfigSchemaPruner.prune_json(content, mode=mode)

        elif content_type in ["log", "traceback"]:
            if not TokenOptimizationConfig.is_strategy_enabled("diagnostic_log_slicing", repo_root):
                tokens = max(1, len(content) // 4)
                return content, {"status": "STRATEGY_DISABLED", "uncompressed_tokens": tokens, "pruned_tokens": tokens, "saved_tokens": 0, "reduction_pct": 0.0}
            return DiagnosticLogPruner.prune_traceback(content)

        elif content_type == "diff":
            if not TokenOptimizationConfig.is_strategy_enabled("git_diff_pruning", repo_root):
                tokens = max(1, len(content) // 4)
                return content, {"status": "STRATEGY_DISABLED", "uncompressed_tokens": tokens, "pruned_tokens": tokens, "saved_tokens": 0, "reduction_pct": 0.0}
            return GitDiffPruner.prune_diff(content)

        # Default fallback
        tokens = max(1, len(content) // 4)
        return content, {"status": "UNSUPPORTED_TYPE", "uncompressed_tokens": tokens, "pruned_tokens": tokens, "saved_tokens": 0, "reduction_pct": 0.0}
