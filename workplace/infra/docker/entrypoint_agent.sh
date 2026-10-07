#!/usr/bin/env bash
# =============================================================================
# Percipience Docker Agent Runner Entrypoint
# Initializes safe git worktree environment, verifies credentials, and executes
# sandboxed LLM CLI derivation commands (claude, aider, or custom agents).
# =============================================================================
set -e

# Configure Git safe directories for mounted volumes
git config --global --add safe.directory /workspace 2>/dev/null || true
git config --global --add safe.directory /repo 2>/dev/null || true
git config --global --add safe.directory "*" 2>/dev/null || true

# Set default git identity if not configured
if [ -z "$(git config --global user.name || true)" ]; then
    git config --global user.name "Percipience Agent Runner"
    git config --global user.email "agent@percipience.internal"
fi

# Print banner in interactive mode
if [ -t 0 ] && [ "$#" -eq 0 ]; then
    echo "====================================================================="
    echo " 🤖 Percipience Autonomous Agent Runner Sandbox"
    echo "    Worktree:   $(pwd)"
    echo "    Python:     $(python3 --version 2>&1)"
    echo "    Node.js:    $(node --version 2>&1)"
    echo "    Claude CLI: $(claude --version 2>/dev/null || echo 'Installed')"
    echo "====================================================================="
fi

# Mock or Simulation Mode handler for automated hermetic testing
if [ "${PERCIPIENCE_SIMULATION:-0}" = "1" ] || [ "${MOCK_LLM:-0}" = "1" ]; then
    if [ "$1" = "claude" ] || [ "$1" = "aider" ]; then
        echo "[MOCK_LLM] Simulation mode active. Intercepting '$1' command."
        if [ -n "${TARGET_FILE:-}" ] && [ -n "${SYNTHESIZED_CODE:-}" ]; then
            mkdir -p "$(dirname "$TARGET_FILE")"
            echo "$SYNTHESIZED_CODE" > "$TARGET_FILE"
            echo "[MOCK_LLM] Synthesized code written to: $TARGET_FILE"
        fi
        exit 0
    fi
fi

# Execute passed command or drop to interactive shell
if [ "$#" -gt 0 ]; then
    exec "$@"
else
    exec bash
fi
