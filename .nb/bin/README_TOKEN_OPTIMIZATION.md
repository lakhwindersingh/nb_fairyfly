# Percipience Token Optimization Guide

## Overview

The Percipience CLI provides comprehensive token optimization capabilities to reduce context token usage and API costs when working with Large Language Models (LLMs). This document explains how to configure and use token optimization features effectively.

## Quick Start

### Enable Token Optimization

```bash
# Enable token optimization globally
.nb/bin/percipience tokens enable

# Check current status
.nb/bin/percipience tokens status

# View cumulative savings
.nb/bin/percipience tokens summary
```

## Configuration

### Token Optimization Modes

The system supports five optimization intensity levels:

| Mode | Description | Use Case | Reduction Target |
|------|-------------|----------|------------------|
| **disabled** | No optimization applied | Debugging, full context needed | 0% |
| **conservative** | Minimal pruning, maximum safety | Production, critical operations | 10-20% |
| **standard** | Balanced optimization (recommended) | Daily development, CI/CD | 30-50% |
| **aggressive** | Heavy pruning, AST-based stripping | Cost optimization, large codebases | 50-70% |
| **extreme** | Maximum compression | Research, experimentation | 70-85% |

### Set Optimization Mode

```bash
# Set to standard mode (recommended)
.nb/bin/percipience tokens set-mode standard

# Set to aggressive mode for maximum savings
.nb/bin/percipience tokens set-mode aggressive

# Disable optimization
.nb/bin/percipience tokens set-mode disabled
```

## Optimization Strategies

### Available Strategies

The token optimizer employs six distinct strategies:

1. **AST Skeleton Pruning** (`ast_skeleton_pruning`)
   - Removes function bodies, preserving signatures
   - Strips implementation details while maintaining structure
   - Best for: Python, TypeScript, JavaScript, Go, Rust

2. **Markdown Doc Pruning** (`markdown_doc_pruning`)
   - Compresses documentation files
   - Removes redundant whitespace and formatting
   - Best for: README.md, documentation files

3. **Config Schema Minification** (`config_schema_minification`)
   - Minifies JSON/YAML configuration files
   - Removes comments and unnecessary whitespace
   - Best for: JSON, YAML, TOML configuration

4. **Diagnostic Log Slicing** (`diagnostic_log_slicing`)
   - Extracts relevant error context from logs
   - Removes verbose timestamps and redundant entries
   - Best for: Error traces, stack traces, log files

5. **Git Diff Pruning** (`git_diff_pruning`)
   - Optimizes git diff output
   - Focuses on changed lines with minimal context
   - Best for: PR reviews, change analysis

6. **Conversation Memory Compaction** (`conversation_memory_compaction`)
   - Compresses conversation history
   - Maintains semantic meaning with reduced verbosity
   - Best for: Chat history, interaction logs

### Enable/Disable Specific Strategies

```bash
# Enable a specific strategy
.nb/bin/percipience tokens set-strategy ast_skeleton_pruning on

# Disable a specific strategy
.nb/bin/percipience tokens set-strategy markdown_doc_pruning off

# Check current strategy configuration
.nb/bin/percipience tokens status
```

## Usage Examples

### Optimize Individual Files

```bash
# Optimize a single Python file
.nb/bin/percipience tokens optimize --file workplace/modules/mod_example/src/handler.py

# Optimize with specific mode override
.nb/bin/percipience tokens optimize --file src/main.py --mode aggressive

# Optimize a markdown file
.nb/bin/percipience tokens optimize --file README.md
```

### Track Token Savings

```bash
# Track savings for a specific file
.nb/bin/percipience tokens track --file workplace/modules/mod_example/src/handler.py --pr PR-123

# Track with custom model pricing
.nb/bin/percipience tokens track --file src/main.py --model claude-3-5-sonnet-20241022
```

### Scan Entire Directories

```bash
# Scan workplace directory and track all savings
.nb/bin/percipience tokens scan --dir workplace --pr PR-123

# Scan specific module directory
.nb/bin/percipience tokens scan --dir workplace/modules/mod_portal_marketing

# Scan with custom model
.nb/bin/percipience tokens scan --dir .nb/core --model claude-3-5-sonnet-20241022
```

### Generate Reports

```bash
# Generate markdown report
.nb/bin/percipience tokens report

# Generate report to custom location
.nb/bin/percipience tokens report --output docs/token_savings.md

# View summary in terminal
.nb/bin/percipience tokens summary
```

## Integration with CI/CD

### PR Gatekeeper Integration

Token optimization is automatically integrated into the PR gatekeeper workflow:

```bash
# Run full PR gate verification (includes token tracking)
.nb/bin/percipience gate
```

The gate command automatically:
1. Scans all changed files with AST pruning
2. Calculates token savings
3. Records metrics to ledger
4. Generates savings report
5. Seals Merkle block with optimization metadata

### Autonomous CI/CD Integration

```bash
# Run autonomous CI/CD with token optimization
.nb/bin/percipience cicd run

# Run without optimization (for debugging)
.nb/bin/percipience cicd run --no-optimize
```

## Configuration Files

### Location

Token optimization configuration is stored in:
```
workspace/config/token_optimization_config.yaml
```

### Example Configuration

```yaml
token_optimization:
  enabled: true
  mode: standard  # conservative | standard | aggressive | extreme
  
  strategies:
    ast_skeleton_pruning: true
    markdown_doc_pruning: true
    config_schema_minification: true
    diagnostic_log_slicing: true
    git_diff_pruning: true
    conversation_memory_compaction: true
  
  pricing:
    input_token_cost_per_million: 3.00    # USD per 1M input tokens
    output_token_cost_per_million: 15.00  # USD per 1M output tokens
    revenue_share_pct: 15.0               # Performance fee percentage
  
  targets:
    max_file_size_bytes: 1048576          # 1MB file size limit
    max_tokens_per_file: 100000           # Token limit per file
    min_reduction_threshold_pct: 5.0      # Minimum reduction to track
```

### Manual Configuration Edit

```bash
# Edit configuration file directly
vim workspace/config/token_optimization_config.yaml

# Or using nano
nano workspace/config/token_optimization_config.yaml
```

## Token Savings Ledger

### Ledger Location

All token savings events are recorded in:
```
.nb/context/ledger/token_savings_ledger.yaml
```

### Ledger Structure

```yaml
token_savings_ledger:
  version: "1.0"
  created_at: "2024-01-15T10:30:00Z"
  
  summary:
    total_events: 142
    total_uncompressed_tokens: 2450000
    total_pruned_tokens: 1225000
    total_tokens_saved: 1225000
    average_reduction_pct: 50.0
    total_gross_savings_usd: 3.675
    total_rev_share_fee_usd: 0.551
    total_net_savings_usd: 3.124
  
  events:
    - event_id: "EVT_20240115_103045_001"
      timestamp: "2024-01-15T10:30:45Z"
      file_path: "workplace/modules/mod_example/src/handler.py"
      language: "python"
      uncompressed_tokens: 15420
      pruned_tokens: 7710
      tokens_saved: 7710
      reduction_percentage: 50.0
      session_or_pr: "PR-123"
      model_id: "claude-3-5-sonnet-20241022"
      gross_savings_usd: 0.0231
      net_savings_usd: 0.0196
```

## Performance Metrics

### Expected Reductions by File Type

| File Type | Conservative | Standard | Aggressive | Extreme |
|-----------|--------------|----------|------------|---------|
| Python (.py) | 15-25% | 35-50% | 55-70% | 75-85% |
| TypeScript (.ts) | 10-20% | 30-45% | 50-65% | 70-80% |
| JavaScript (.js) | 10-20% | 30-45% | 50-65% | 70-80% |
| Go (.go) | 20-30% | 40-55% | 60-75% | 80-90% |
| Rust (.rs) | 15-25% | 35-50% | 55-70% | 75-85% |
| Markdown (.md) | 5-15% | 15-30% | 30-50% | 50-70% |
| JSON/YAML | 10-20% | 25-40% | 45-60% | 65-80% |

### Cost Savings Example

For a typical workspace with 100,000 lines of Python code:

```
Baseline Tokens: 2,500,000 tokens
Mode: standard (50% reduction)
Tokens Saved: 1,250,000 tokens

Input Cost Savings: $3.75 USD (@ $3/M tokens)
Output Cost Savings: $18.75 USD (@ $15/M tokens)
Total Gross Savings: $22.50 USD per full context pass

Monthly Savings (100 CI/CD runs): $2,250 USD
Annual Savings: $27,000 USD
```

## Best Practices

### 1. Start Conservative

```bash
# Begin with conservative mode
.nb/bin/percipience tokens set-mode conservative

# Monitor results
.nb/bin/percipience tokens summary

# Gradually increase to standard
.nb/bin/percipience tokens set-mode standard
```

### 2. Enable Selectively by File Type

```bash
# Enable AST pruning for code files only
.nb/bin/percipience tokens set-strategy ast_skeleton_pruning on

# Disable markdown pruning if docs are critical
.nb/bin/percipience tokens set-strategy markdown_doc_pruning off
```

### 3. Track Savings per PR

```bash
# Always tag scans with PR number
.nb/bin/percipience tokens scan --dir workplace --pr PR-456

# Review savings before merge
.nb/bin/percipience tokens report
```

### 4. Monitor Effectiveness

```bash
# Check status regularly
.nb/bin/percipience tokens status

# Review cumulative savings
.nb/bin/percipience tokens summary

# Generate detailed reports
.nb/bin/percipience tokens report --output reports/$(date +%Y-%m-%d)_savings.md
```

### 5. Audit Configuration

```bash
# Validate current configuration
.nb/bin/percipience tokens status

# Test optimization on sample file before enabling globally
.nb/bin/percipience tokens optimize --file test_file.py --mode standard
```

## Troubleshooting

### Token Optimization Not Working

```bash
# Check if optimization is enabled
.nb/bin/percipience tokens status

# Enable if disabled
.nb/bin/percipience tokens enable

# Verify mode is not disabled
.nb/bin/percipience tokens set-mode standard
```

### Lower Than Expected Savings

```bash
# Check active strategies
.nb/bin/percipience tokens status

# Increase optimization intensity
.nb/bin/percipience tokens set-mode aggressive

# Ensure strategies are enabled
.nb/bin/percipience tokens set-strategy ast_skeleton_pruning on
```

### Configuration Not Persisting

```bash
# Verify config file exists
ls -la workspace/config/token_optimization_config.yaml

# Check file permissions
chmod 644 workspace/config/token_optimization_config.yaml

# Recreate config directory if missing
mkdir -p workspace/config
```

### Ledger Not Recording Events

```bash
# Verify ledger directory exists
ls -la .nb/context/ledger/

# Create ledger directory if missing
mkdir -p .nb/context/ledger

# Check write permissions
chmod 755 .nb/context/ledger
```

## Advanced Usage

### Custom Pricing Models

Edit `workspace/config/token_optimization_config.yaml`:

```yaml
token_optimization:
  pricing:
    input_token_cost_per_million: 3.00    # Adjust for your model
    output_token_cost_per_million: 15.00  # Adjust for your model
    revenue_share_pct: 15.0               # Performance fee
```

### Tree-Sitter Daemon Integration

For maximum performance, use the native Tree-Sitter daemon:

```bash
# Check daemon status
.nb/bin/percipience daemon status

# High-speed AST pruning via daemon
.nb/bin/percipience daemon prune --file workplace/modules/mod_example/src/handler.py
```

### Integration with Diagnostic Re-Prompting

Token optimization is automatically applied during self-healing:

```bash
# Diagnostic re-prompting with optimized context
.nb/bin/percipience reprompt --module mod_portal_marketing --failure-type CONTRACT_VIOLATION
```

## API Reference

### Configuration API

```python
from core.token_optimizer_suite import TokenOptimizationConfig

# Load configuration
config = TokenOptimizationConfig.load_config(workspace_root)

# Enable optimization
TokenOptimizationConfig.set_enabled(True, workspace_root)

# Set mode
TokenOptimizationConfig.set_mode("standard", workspace_root)

# Set strategy
TokenOptimizationConfig.set_strategy("ast_skeleton_pruning", True, workspace_root)
```

### Optimization API

```python
from core.token_optimizer_suite import UnifiedTokenOptimizer

# Optimize content
pruned, stats = UnifiedTokenOptimizer.optimize_content(
    content=source_code,
    content_type="python",
    workspace_root=workspace_root,
    override_mode="standard"
)

# Access stats
print(f"Saved: {stats['saved_tokens']} tokens ({stats['reduction_pct']}%)")
```

### Tracking API

```python
from core.token_tracker import TokenTracker

# Track single event
event = TokenTracker.record_event(
    repo_root=workspace_root,
    file_path="src/main.py",
    uncompressed_tokens=15000,
    pruned_tokens=7500,
    session_or_pr="PR-123",
    model_id="claude-3-5-sonnet-20241022"
)

# Scan directory
results = TokenTracker.scan_and_track_repo(
    repo_root=workspace_root,
    target_dir="workplace",
    session_or_pr="CI-456"
)
```

## Support & Resources

### Documentation

- Main CLI Documentation: `.nb/bin/README.md`
- Token Optimization Guide: `.nb/bin/README_TOKEN_OPTIMIZATION.md` (this file)
- Architecture Plans: `.nb/plan/`

### Command Help

```bash
# General help
.nb/bin/percipience --help

# Token subcommand help
.nb/bin/percipience tokens --help

# Specific action help
.nb/bin/percipience tokens optimize --help
```

### Configuration Templates

Default configuration templates are located in:
```
.nb/config/token_optimization_config.yaml.template
```

## Changelog

### Version 1.0.0 (Current)
- Initial release
- Six optimization strategies
- Five intensity modes
- Automated CI/CD integration
- Comprehensive ledger tracking
- Financial metrics and reporting
