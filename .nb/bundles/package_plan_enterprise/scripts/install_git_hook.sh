#!/usr/bin/env bash
# Install Percipience Local Pre-Commit Hook
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HOOK_FILE="${REPO_ROOT}/.git/hooks/pre-commit"
STRICT_HOOK="${REPO_ROOT}/.nb/git_hooks/pre-commit.sh"

echo "🔧 Installing Percipience local pre-commit hook..."

mkdir -p "${REPO_ROOT}/.git/hooks" 2>/dev/null || true

if [ -f "${STRICT_HOOK}" ]; then
  # Prefer the canonical strict guardrail hook bundled with the plugin/platform
  cp "${STRICT_HOOK}" "${HOOK_FILE}"
else
  cat << 'EOF' > "${HOOK_FILE}"
#!/usr/bin/env bash
# Percipience Pre-Commit Gatekeeper & Token Savings Metering Hook
set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
PERCIPIENCE="${REPO_ROOT}/.nb/bin/percipience"

if [ -f "${PERCIPIENCE}" ]; then
  echo "🛡️ Running Percipience Local Pre-Commit Gatekeeper..."
  chmod +x "${PERCIPIENCE}"
  "${PERCIPIENCE}" gate
  "${PERCIPIENCE}" tokens summary
else
  echo "⚠️ Percipience CLI not found at ${PERCIPIENCE}. Skipping hook."
fi
EOF
fi

chmod +x "${HOOK_FILE}"
echo "✅ Percipience pre-commit hook installed successfully at: ${HOOK_FILE}"
