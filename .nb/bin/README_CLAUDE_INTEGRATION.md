# Integrating Percipience with Claude Prompt Processing

## Overview

This guide explains how to integrate Percipience token optimization into your Claude API workflows to reduce prompt token usage and API costs automatically.

## Integration Methods

### Method 1: Pre-Process Prompts with CLI (Recommended for Scripts)

Use Percipience CLI to optimize context before sending to Claude:

```bash
#!/bin/bash
# Example: optimize_and_prompt.sh

# 1. Optimize source files before including in prompt
.nb/bin/percipience tokens optimize --file workplace/modules/mod_example/src/handler.py --mode standard > /tmp/optimized_context.txt

# 2. Build prompt with optimized context
cat > /tmp/claude_prompt.txt <<EOF
Please review the following code:

$(cat /tmp/optimized_context.txt)

Focus on architectural patterns and suggest improvements.
EOF

# 3. Send to Claude API
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d @- <<PAYLOAD
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 4096,
  "messages": [{
    "role": "user",
    "content": "$(cat /tmp/claude_prompt.txt | jq -Rs .)"
  }]
}
PAYLOAD

# 4. Track savings
.nb/bin/percipience tokens track --file workplace/modules/mod_example/src/handler.py --pr CLI_PROMPT_001
```

### Method 2: Python API Integration (Recommended for Applications)

Integrate Percipience directly into your Python application:

```python
#!/usr/bin/env python3
"""
claude_prompt_optimizer.py
Optimizes prompts before sending to Claude API
"""

import os
import sys
from pathlib import Path
from anthropic import Anthropic

# Add Percipience to path
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / ".nb"))
sys.path.insert(0, str(REPO_ROOT / ".nb" / "core"))

from core.token_optimizer_suite import UnifiedTokenOptimizer
from core.token_tracker import TokenTracker

class ClaudePromptOptimizer:
    """Optimizes prompts before sending to Claude API"""
    
    def __init__(self, workspace_root: Path, optimization_mode: str = "standard"):
        self.workspace_root = workspace_root
        self.optimization_mode = optimization_mode
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    def optimize_file_context(self, file_path: Path, content_type: str = "python") -> tuple[str, dict]:
        """
        Optimize a file's content for inclusion in prompt
        
        Args:
            file_path: Path to file to optimize
            content_type: File type (python, typescript, markdown, etc.)
        
        Returns:
            Tuple of (optimized_content, stats_dict)
        """
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        
        # Optimize using Percipience
        optimized, stats = UnifiedTokenOptimizer.optimize_content(
            content=content,
            content_type=content_type,
            workspace_root=self.workspace_root,
            override_mode=self.optimization_mode
        )
        
        return optimized, stats
    
    def build_prompt_with_context(self, instruction: str, files: list[tuple[Path, str]]) -> tuple[str, dict]:
        """
        Build optimized prompt with multiple file contexts
        
        Args:
            instruction: User instruction/question
            files: List of (file_path, content_type) tuples
        
        Returns:
            Tuple of (full_prompt, aggregate_stats)
        """
        optimized_contexts = []
        total_original = 0
        total_optimized = 0
        
        for file_path, content_type in files:
            optimized, stats = self.optimize_file_context(file_path, content_type)
            
            optimized_contexts.append(f"""
### File: {file_path.relative_to(self.workspace_root)}

```{content_type}
{optimized}
```
""")
            
            total_original += stats.get("uncompressed_tokens", 0)
            total_optimized += stats.get("pruned_tokens", 0)
        
        full_prompt = f"""{instruction}

## Context Files

{"".join(optimized_contexts)}
"""
        
        aggregate_stats = {
            "files_included": len(files),
            "original_tokens": total_original,
            "optimized_tokens": total_optimized,
            "tokens_saved": total_original - total_optimized,
            "reduction_pct": ((total_original - total_optimized) / total_original * 100) if total_original > 0 else 0
        }
        
        return full_prompt, aggregate_stats
    
    def send_optimized_prompt(
        self, 
        instruction: str, 
        files: list[tuple[Path, str]],
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 4096,
        session_id: str = "INTERACTIVE"
    ) -> dict:
        """
        Optimize prompt and send to Claude API
        
        Args:
            instruction: User instruction
            files: Files to include as context
            model: Claude model to use
            max_tokens: Max tokens in response
            session_id: Session/PR identifier for tracking
        
        Returns:
            Response dict with content and metrics
        """
        # Build optimized prompt
        prompt, stats = self.build_prompt_with_context(instruction, files)
        
        print(f"📊 Token Optimization Stats:")
        print(f"   Files: {stats['files_included']}")
        print(f"   Original Tokens: {stats['original_tokens']:,}")
        print(f"   Optimized Tokens: {stats['optimized_tokens']:,}")
        print(f"   Tokens Saved: {stats['tokens_saved']:,} ({stats['reduction_pct']:.1f}%)")
        
        # Send to Claude
        message = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        # Track savings in Percipience ledger
        for file_path, _ in files:
            try:
                rel_path = str(file_path.relative_to(self.workspace_root))
                TokenTracker.record_event(
                    repo_root=self.workspace_root,
                    file_path=rel_path,
                    uncompressed_tokens=stats['original_tokens'] // len(files),
                    pruned_tokens=stats['optimized_tokens'] // len(files),
                    session_or_pr=session_id,
                    model_id=model
                )
            except Exception as e:
                print(f"⚠️  Could not track savings for {file_path}: {e}")
        
        return {
            "response": message.content[0].text,
            "usage": {
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens
            },
            "optimization_stats": stats,
            "model": model
        }


# Example usage
if __name__ == "__main__":
    workspace = Path("/Users/lakhwinder/PycharmProjects/nb_beehive")
    optimizer = ClaudePromptOptimizer(workspace, optimization_mode="standard")
    
    # Files to include in prompt
    files_to_analyze = [
        (workspace / "workplace/modules/mod_example/src/handler.py", "python"),
        (workspace / "workplace/modules/mod_example/src/validator.py", "python"),
        (workspace / "workplace/modules/mod_example/README.md", "markdown")
    ]
    
    # Send optimized prompt to Claude
    result = optimizer.send_optimized_prompt(
        instruction="Review this module for architectural improvements and potential bugs.",
        files=files_to_analyze,
        session_id="REVIEW_001"
    )
    
    print("\n🤖 Claude Response:")
    print(result["response"])
    print(f"\n📈 API Usage:")
    print(f"   Input Tokens: {result['usage']['input_tokens']:,}")
    print(f"   Output Tokens: {result['usage']['output_tokens']:,}")
```

### Method 3: Pre-Commit Hook Integration

Automatically optimize files before they're committed:

```bash
#!/bin/bash
# .git/hooks/pre-commit
# Optimize files before commit and track savings

echo "🔍 Running Percipience token optimization scan..."

# Get staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

# Optimize each staged file
for FILE in $STAGED_FILES; do
    if [[ $FILE == *.py ]] || [[ $FILE == *.ts ]] || [[ $FILE == *.js ]]; then
        echo "   Optimizing: $FILE"
        .nb/bin/percipience tokens track --file "$FILE" --pr "PRE_COMMIT_$(date +%Y%m%d)"
    fi
done

# Scan workspace and generate report
.nb/bin/percipience tokens scan --dir workplace --pr "COMMIT_$(git rev-parse --short HEAD)" > /dev/null 2>&1

echo "✅ Token optimization scan complete"
exit 0
```

### Method 4: GitHub Actions CI/CD Integration

Optimize prompts in CI/CD pipelines:

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review with Token Optimization

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  claude-review:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install anthropic pyyaml tiktoken
      
      - name: Enable Percipience token optimization
        run: |
          .nb/bin/percipience tokens enable
          .nb/bin/percipience tokens set-mode aggressive
      
      - name: Scan PR changes and optimize
        run: |
          .nb/bin/percipience tokens scan --dir . --pr "PR-${{ github.event.pull_request.number }}"
      
      - name: Run Claude review with optimized context
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python3 scripts/claude_review_pr.py \
            --pr-number "${{ github.event.pull_request.number }}" \
            --optimize-context
      
      - name: Generate token savings report
        run: |
          .nb/bin/percipience tokens report --output reports/pr_${{ github.event.pull_request.number }}_savings.md
      
      - name: Upload savings report
        uses: actions/upload-artifact@v3
        with:
          name: token-savings-report
          path: reports/pr_${{ github.event.pull_request.number }}_savings.md
```

## Advanced Integration Patterns

### Pattern 1: Multi-File Context Optimization

```python
from pathlib import Path
from core.token_optimizer_suite import UnifiedTokenOptimizer

def optimize_multi_file_context(workspace_root: Path, files: list[Path], mode: str = "standard") -> str:
    """Optimize multiple files into single context block"""
    
    optimized_blocks = []
    
    for file_path in files:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        ext = file_path.suffix.lstrip(".")
        
        type_map = {
            "py": "python", "ts": "typescript", "js": "javascript",
            "go": "go", "rs": "rust", "md": "markdown"
        }
        content_type = type_map.get(ext, "python")
        
        optimized, stats = UnifiedTokenOptimizer.optimize_content(
            content=content,
            content_type=content_type,
            workspace_root=workspace_root,
            override_mode=mode
        )
        
        optimized_blocks.append(f"### {file_path.name}\n\n```{content_type}\n{optimized}\n```\n")
    
    return "\n".join(optimized_blocks)
```

### Pattern 2: Streaming Optimization

```python
def optimize_streaming_context(workspace_root: Path, file_stream: list[Path], mode: str = "standard"):
    """Optimize files in streaming fashion for large codebases"""
    
    for file_path in file_stream:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        ext = file_path.suffix.lstrip(".")
        content_type = {"py": "python", "ts": "typescript"}.get(ext, "python")
        
        optimized, stats = UnifiedTokenOptimizer.optimize_content(
            content=content,
            content_type=content_type,
            workspace_root=workspace_root,
            override_mode=mode
        )
        
        # Yield optimized content for streaming to Claude
        yield {
            "file": str(file_path),
            "content": optimized,
            "stats": stats
        }
```

### Pattern 3: Adaptive Optimization

```python
def adaptive_optimize(workspace_root: Path, file_path: Path, target_token_budget: int) -> str:
    """Adaptively optimize until target token budget is met"""
    
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    content_type = "python"  # Detect from extension
    
    modes = ["conservative", "standard", "aggressive", "extreme"]
    
    for mode in modes:
        optimized, stats = UnifiedTokenOptimizer.optimize_content(
            content=content,
            content_type=content_type,
            workspace_root=workspace_root,
            override_mode=mode
        )
        
        if stats.get("pruned_tokens", 0) <= target_token_budget:
            print(f"✅ Target budget met with mode: {mode}")
            return optimized
    
    print(f"⚠️  Could not meet target budget {target_token_budget}, using extreme mode")
    return optimized
```

## Configuration for Claude Integration

### 1. Create Claude-Specific Config

```yaml
# workspace/config/claude_integration_config.yaml
claude_integration:
  default_optimization_mode: standard
  
  # Optimization by prompt type
  prompt_types:
    code_review:
      mode: aggressive
      strategies:
        - ast_skeleton_pruning
        - git_diff_pruning
    
    documentation_generation:
      mode: conservative
      strategies:
        - markdown_doc_pruning
    
    bug_analysis:
      mode: standard
      strategies:
        - ast_skeleton_pruning
        - diagnostic_log_slicing
    
    architecture_review:
      mode: conservative
      strategies:
        - ast_skeleton_pruning
  
  # Model-specific settings
  models:
    claude-3-5-sonnet-20241022:
      max_context_tokens: 200000
      target_reduction_pct: 40
    
    claude-3-opus-20240229:
      max_context_tokens: 200000
      target_reduction_pct: 30
    
    claude-3-haiku-20240307:
      max_context_tokens: 200000
      target_reduction_pct: 50
  
  # Auto-tracking
  tracking:
    enabled: true
    session_prefix: "CLAUDE_API"
    ledger_path: ".nb/context/ledger/claude_api_ledger.yaml"
```

### 2. Environment Variables

```bash
# .env
ANTHROPIC_API_KEY=your_api_key_here
PERCIPIENCE_TOKEN_MODE=standard
PERCIPIENCE_TRACKING_ENABLED=true
PERCIPIENCE_WORKSPACE_ROOT=/Users/lakhwinder/PycharmProjects/nb_beehive
```

### 3. Load Configuration in Code

```python
import yaml
from pathlib import Path

def load_claude_integration_config(workspace_root: Path) -> dict:
    """Load Claude integration configuration"""
    config_path = workspace_root / "workspace/config/claude_integration_config.yaml"
    
    if config_path.exists():
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    
    # Default configuration
    return {
        "claude_integration": {
            "default_optimization_mode": "standard",
            "tracking": {"enabled": True}
        }
    }
```

## Complete Example: Claude Chat with Optimization

```python
#!/usr/bin/env python3
"""
claude_chat_optimized.py
Interactive Claude chat with automatic token optimization
"""

import os
import sys
from pathlib import Path
from anthropic import Anthropic

# Setup paths
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / ".nb"))
sys.path.insert(0, str(REPO_ROOT / ".nb" / "core"))

from core.token_optimizer_suite import UnifiedTokenOptimizer
from core.token_tracker import TokenTracker

class OptimizedClaudeChat:
    def __init__(self, workspace_root: Path, mode: str = "standard"):
        self.workspace_root = workspace_root
        self.mode = mode
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        self.conversation_history = []
    
    def add_file_context(self, file_paths: list[Path]) -> str:
        """Add optimized file context to conversation"""
        contexts = []
        
        for file_path in file_paths:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            ext = file_path.suffix.lstrip(".")
            content_type = {
                "py": "python", "ts": "typescript", "js": "javascript",
                "go": "go", "rs": "rust", "md": "markdown"
            }.get(ext, "python")
            
            optimized, stats = UnifiedTokenOptimizer.optimize_content(
                content=content,
                content_type=content_type,
                workspace_root=self.workspace_root,
                override_mode=self.mode
            )
            
            contexts.append(f"""
File: {file_path.relative_to(self.workspace_root)}

```{content_type}
{optimized}
```
""")
            
            # Track savings
            try:
                rel_path = str(file_path.relative_to(self.workspace_root))
                TokenTracker.record_event(
                    repo_root=self.workspace_root,
                    file_path=rel_path,
                    uncompressed_tokens=stats.get("uncompressed_tokens", 0),
                    pruned_tokens=stats.get("pruned_tokens", 0),
                    session_or_pr="CLAUDE_CHAT",
                    model_id="claude-3-5-sonnet-20241022"
                )
            except Exception:
                pass
        
        return "\n".join(contexts)
    
    def chat(self, user_message: str, include_files: list[Path] = None) -> str:
        """Send message to Claude with optional file context"""
        
        # Build full message
        if include_files:
            file_context = self.add_file_context(include_files)
            full_message = f"{user_message}\n\n## Context:\n{file_context}"
        else:
            full_message = user_message
        
        # Add to conversation
        self.conversation_history.append({
            "role": "user",
            "content": full_message
        })
        
        # Send to Claude
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        
        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        print(f"📊 API Usage: {response.usage.input_tokens:,} in / {response.usage.output_tokens:,} out")
        
        return assistant_message


# Interactive usage
if __name__ == "__main__":
    workspace = Path("/Users/lakhwinder/PycharmProjects/nb_beehive")
    chat = OptimizedClaudeChat(workspace, mode="standard")
    
    print("🤖 Claude Chat (with Token Optimization)")
    print("Commands: /add <file> | /quit | <message>")
    print("-" * 60)
    
    current_files = []
    
    while True:
        user_input = input("\n👤 You: ").strip()
        
        if user_input == "/quit":
            break
        
        if user_input.startswith("/add "):
            file_path = workspace / user_input[5:].strip()
            if file_path.exists():
                current_files.append(file_path)
                print(f"✅ Added: {file_path.name}")
            else:
                print(f"❌ File not found: {file_path}")
            continue
        
        if user_input.startswith("/clear"):
            current_files = []
            print("✅ Cleared file context")
            continue
        
        response = chat.chat(user_input, include_files=current_files if current_files else None)
        print(f"\n🤖 Claude: {response}")
```

## Measuring Effectiveness

### Track Savings Over Time

```bash
# Weekly report
.nb/bin/percipience tokens summary

# Generate monthly report
.nb/bin/percipience tokens report --output reports/$(date +%Y-%m)_claude_savings.md
```

### Compare Optimized vs Unoptimized

```python
def compare_optimization_impact(workspace_root: Path, file_path: Path):
    """Compare optimized vs unoptimized prompts"""
    content = file_path.read_text(encoding="utf-8")
    
    # Unoptimized
    unopt_stats = {"tokens": len(content.split())}
    
    # Optimized
    optimized, opt_stats = UnifiedTokenOptimizer.optimize_content(
        content=content,
        content_type="python",
        workspace_root=workspace_root,
        override_mode="standard"
    )
    
    print(f"Comparison for {file_path.name}:")
    print(f"  Unoptimized: {opt_stats['uncompressed_tokens']:,} tokens")
    print(f"  Optimized: {opt_stats['pruned_tokens']:,} tokens")
    print(f"  Savings: {opt_stats['saved_tokens']:,} tokens ({opt_stats['reduction_pct']}%)")
    print(f"  Cost Savings: ${opt_stats.get('gross_savings_usd', 0):.4f}")
```

## Best Practices

1. **Always track savings** - Use session IDs consistently
2. **Choose appropriate mode** - Conservative for critical analysis, aggressive for routine reviews
3. **Test optimization** - Verify optimized prompts still provide necessary context
4. **Monitor quality** - Ensure optimization doesn't degrade Claude's responses
5. **Use adaptive optimization** - Adjust mode based on prompt complexity

## Troubleshooting

### Claude Returns "Insufficient Context" Error

```bash
# Reduce optimization intensity
.nb/bin/percipience tokens set-mode conservative

# Or disable specific strategies
.nb/bin/percipience tokens set-strategy ast_skeleton_pruning off
```

### Token Counts Don't Match Expectations

```bash
# Check actual optimization stats
.nb/bin/percipience tokens optimize --file yourfile.py

# Verify ledger is recording correctly
cat .nb/context/ledger/token_savings_ledger.yaml
```

## Next Steps

1. Enable token optimization: `.nb/bin/percipience tokens enable`
2. Set appropriate mode: `.nb/bin/percipience tokens set-mode standard`
3. Integrate into your Claude workflows using examples above
4. Monitor savings: `.nb/bin/percipience tokens summary`
5. Generate regular reports: `.nb/bin/percipience tokens report`
