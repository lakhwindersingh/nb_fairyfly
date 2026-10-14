#!/bin/bash
# Pre-commit hook: Validate Merkle DAG chain, semantic parity, and context ledger consistency
# Installed by: .nb/scripts/install_git_hook.sh
# Mode: STRICT (blocks commits on validation failures)

set -e

REPO_ROOT=$(git rev-parse --show-toplevel)
NB_BIN="${REPO_ROOT}/.nb/bin/percipience"

# Color codes for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Function to print validation status
print_status() {
  local status=$1
  local message=$2
  if [ $status -eq 0 ]; then
    echo -e "${GREEN}✅ $message${NC}"
  else
    echo -e "${RED}❌ $message${NC}"
  fi
}

echo "🔐 Running Agentic Guardrail Pre-Commit Validations..."

# 1. Validate Merkle DAG chain for modified context files
echo ""
echo "1️⃣  Validating Merkle DAG chain integrity..."
if $NB_BIN audit --validate-chain-on-commit 2>/dev/null; then
  print_status 0 "Merkle DAG chain is continuous and valid"
else
  print_status 1 "Merkle DAG chain validation failed"
  echo -e "${RED}Error: Commit contains changes that break Merkle chain continuity.${NC}"
  echo "  Run: git reset HEAD <file>  to unstage problematic changes"
  exit 1
fi

# 2. Enforce semantic parity gate for plan modifications
echo ""
echo "2️⃣  Checking for plan modifications requiring semantic parity validation..."
PLAN_FILES=$(git diff --cached --name-only 2>/dev/null | grep -E "\.nb/plan/.*\.md$" || true)
if [ -n "$PLAN_FILES" ]; then
  echo "  Modified plan files detected:"
  echo "$PLAN_FILES" | sed 's/^/    - /'

  if $NB_BIN drift check --fail-if-below 0.95 2>/dev/null; then
    print_status 0 "Plan semantic parity ≥ 0.95 (gate PASSED)"
  else
    print_status 1 "Plan semantic parity < 0.95 (gate FAILED)"
    echo -e "${RED}Error: Plan modifications must maintain semantic parity ≥ 0.95${NC}"
    echo "  Recommendation: Update MANIFEST.yaml hashes and recalculate parity scores"
    exit 1
  fi
else
  echo "  No plan files modified"
fi

# 3. Validate context ledger consistency
echo ""
echo "3️⃣  Validating context ledger schema consistency..."
if $NB_BIN validate --ledger-schema 2>/dev/null; then
  print_status 0 "Context ledger schema is valid"
else
  print_status 1 "Context ledger schema validation failed"
  echo -e "${RED}Error: Context ledger contains schema violations.${NC}"
  echo "  File: .nb/context/ledger/context_ledger.yaml"
  exit 1
fi

# 4. Check for modified master plan files without MANIFEST updates
echo ""
echo "4️⃣  Checking master plan synchronization..."
MASTER_PLAN_MODS=$(git diff --cached --name-only 2>/dev/null | grep -E "\.nb/plan/master/.*\.(concise|detailed|README)\.md$" || true)
MANIFEST_MODS=$(git diff --cached --name-only 2>/dev/null | grep -E "\.nb/plan/master/.*MANIFEST\.yaml$" || true)

if [ -n "$MASTER_PLAN_MODS" ] && [ -z "$MANIFEST_MODS" ]; then
  echo -e "${YELLOW}⚠️  Warning: Master plan files modified but MANIFEST.yaml not updated${NC}"
  echo "  Modified: $MASTER_PLAN_MODS"
  echo "  Please update corresponding MANIFEST.yaml files to reflect changes"
fi

echo ""
echo -e "${GREEN}✅ All pre-commit validations PASSED${NC}"
echo "  Commit is ready to be pushed to CI/CD pipeline"
exit 0
