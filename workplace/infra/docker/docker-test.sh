#!/usr/bin/env bash
# =============================================================================
# Percipience Enterprise Context Engineering OS - Docker Local Testing Runner
# =============================================================================
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$DIR/docker-compose.yml"

print_header() {
  echo -e "\033[1;36m=====================================================================\033[0m"
  echo -e "\033[1;36m 🐳 Percipience Enterprise Local Docker Test Harness\033[0m"
  echo -e "\033[1;36m=====================================================================\033[0m"
}

usage() {
  print_header
  echo "Usage: $0 [command]"
  echo ""
  echo "Available commands:"
  echo "  build         Build all core Docker images (portal, tree-sitter-daemon, test-runner)"
  echo "  build-runner  Build isolated agent-runner image (Dockerfile.agent_runner)"
  echo "  up            Start portal & tree-sitter daemon detached and wait for healthy state"
  echo "  fleet-up      Start portal, daemon, and simulated fleet runner containers (swarm mode)"
  echo "  down          Stop and remove containers and local networks"
  echo "  status        Check health status of running services"
  echo "  fleet-status  Display live machine fleet, FinOps rollup, and active tasks"
  echo "  simulate-pulse Trigger activity pulse (+50k tokens) and task advancement"
  echo "  test          Run full test suite (pytest workplace/tests/) inside container"
  echo "  test-portal   Run portal integration tests inside container"
  echo "  test-fleet    Run fleet telemetry & FinOps rollup test suite"
  echo "  gate          Execute 7-stage CI/CD gatekeeper (./.nb/bin/percipience gate) in container"
  echo "  logs          Follow live container logs"
  echo "  shell         Open interactive bash shell in test-runner container"
  echo "  shell-runner  Open interactive bash shell in agent-runner container"
  echo ""
  exit 1
}

CMD="${1:-}"

case "$CMD" in
  build)
    print_header
    echo "📦 Building core Percipience container images..."
    docker compose -f "$COMPOSE_FILE" build tree-sitter-daemon portal test-runner
    echo "✅ Build completed successfully."
    ;;

  build-runner)
    print_header
    echo "🤖 Building sandboxed agent-runner image..."
    docker compose -f "$COMPOSE_FILE" build agent-runner
    echo "✅ Agent runner build completed successfully."
    ;;

  up)
    print_header
    echo "🚀 Starting Percipience services (daemon + portal)..."
    docker compose -f "$COMPOSE_FILE" up -d tree-sitter-daemon portal
    
    echo "⏳ Waiting for healthchecks..."
    for i in {1..30}; do
      PORTAL_STATUS=$(docker inspect --format='{{json .State.Health.Status}}' percipience-portal 2>/dev/null || echo "\"starting\"")
      DAEMON_STATUS=$(docker inspect --format='{{json .State.Health.Status}}' percipience-tree-sitter-daemon 2>/dev/null || echo "\"starting\"")
      
      if [[ "$PORTAL_STATUS" == "\"healthy\"" && "$DAEMON_STATUS" == "\"healthy\"" ]]; then
        echo -e "\033[1;32m✅ All services are healthy!\033[0m"
        echo "   • Portal Gateway: http://localhost:3000"
        echo "   • AST Daemon:     http://localhost:8585/health"
        exit 0
      fi
      sleep 1
    done
    echo "⚠️ Warning: Services took longer than expected to become healthy. Check logs with '$0 logs'."
    ;;

  fleet-up)
    print_header
    echo "🚀 Starting Percipience services with simulated Fleet Swarm containers..."
    docker compose -f "$COMPOSE_FILE" --profile fleet up -d tree-sitter-daemon portal fleet-agent-1 fleet-agent-2

    echo "⏳ Waiting for healthchecks..."
    for i in {1..30}; do
      PORTAL_STATUS=$(docker inspect --format='{{json .State.Health.Status}}' percipience-portal 2>/dev/null || echo "\"starting\"")
      DAEMON_STATUS=$(docker inspect --format='{{json .State.Health.Status}}' percipience-tree-sitter-daemon 2>/dev/null || echo "\"starting\"")

      if [[ "$PORTAL_STATUS" == "\"healthy\"" && "$DAEMON_STATUS" == "\"healthy\"" ]]; then
        echo -e "\033[1;32m✅ Portal and Fleet Agents are running!\033[0m"
        echo "   • Portal Gateway: http://localhost:3000 (Tab 16: Fleet & FinOps)"
        echo "   • AST Daemon:     http://localhost:8585/health"
        echo "   • Fleet Agent 1:  Connected to http://portal:3000 (simulating proj_docker_swarm)"
        echo "   • Fleet Agent 2:  Connected to http://portal:3000 (simulating proj_billing)"
        echo "   • Check status:   $0 fleet-status"
        exit 0
      fi
      sleep 1
    done
    echo "⚠️ Warning: Services took longer than expected to become healthy. Check logs with '$0 logs'."
    ;;

  down)
    print_header
    echo "🛑 Stopping and cleaning up Percipience containers..."
    docker compose -f "$COMPOSE_FILE" --profile fleet --profile test --profile agent down --remove-orphans
    echo "✅ Cleaned up."
    ;;

  status)
    print_header
    echo "🔍 Querying service health endpoints..."
    echo -n "   • Tree-Sitter Daemon (8585): "
    curl -s http://127.0.0.1:8585/health || echo "UNREACHABLE"
    echo ""
    echo -n "   • Portal Gateway (3000):     "
    curl -s http://127.0.0.1:3000/api/health || echo "UNREACHABLE"
    echo ""
    ;;

  fleet-status)
    print_header
    echo "🖥️ Live Fleet Machines & FinOps Accounting:"
    MACHINES_JSON=$(curl -s http://127.0.0.1:3000/api/fleet/machines || echo "{}")
    ROLLUP_JSON=$(curl -s http://127.0.0.1:3000/api/fleet/finops-rollup || echo "{}")
    echo "$MACHINES_JSON" | python3 -c '
import sys, json
try:
    data = json.load(sys.stdin)
    machines = data.get("machines", [])
    print(f"   • Total Registered Nodes: {len(machines)}")
    for m in machines:
        st = m.get("health_status", "UNKNOWN")
        host = m.get("hostname", "unknown")
        mid = m.get("machine_id", "")
        task = m.get("active_task", {}).get("task_name", "Idle")
        pct = m.get("active_task", {}).get("progress_pct", 0)
        tok = m.get("finops", {}).get("tokens_saved", 0)
        gross = m.get("finops", {}).get("gross_savings_usd", 0.0)
        print(f"     [{st:10}] {host:25} | Task: {task} ({pct:.0f}%) | Tokens: {tok:,} (${gross:.4f})")
except Exception as e:
    print(f"   Could not fetch machines: {e}")
'
    echo ""
    echo "💰 Enterprise FinOps Rollup:"
    echo "$ROLLUP_JSON" | python3 -c '
import sys, json
try:
    data = json.load(sys.stdin)
    s = data.get("rollup", {}).get("summary", {})
    print(f"   • Active Nodes:           {s.get(\"active_machines_count\", 0)} / {s.get(\"total_machines_count\", 0)}")
    print(f"   • Total Tokens Saved:     {s.get(\"total_tokens_saved\", 0):,}")
    print(f"   • Enterprise Gross:       ${s.get(\"enterprise_gross_savings_usd\", 0.0):.2f}")
    print(f"   • 15% Percipience Fee:    ${s.get(\"percipience_rev_share_fee_usd\", 0.0):.2f}")
    print(f"   • 85% Customer Net:       ${s.get(\"customer_net_retained_usd\", 0.0):.2f}")
except Exception as e:
    print(f"   Could not fetch FinOps rollup: {e}")
'
    ;;

  simulate-pulse)
    print_header
    echo "⚡ Injecting activity pulse (+50k tokens & milestone advancement)..."
    RESP=$(curl -s -X POST "http://127.0.0.1:3000/api/fleet/simulate?tokens=50000&advance=true" || echo "FAILED")
    echo "$RESP" | python3 -c '
import sys, json
try:
    d = json.load(sys.stdin)
    m = d.get("machine", {})
    print(f"✅ Injected into {m.get(\"machine_id\")}: Task \"{m.get(\"active_task\", {}).get(\"task_name\")}\" ({m.get(\"active_task\", {}).get(\"progress_pct\")}%).")
    print(f"   Gross Savings: ${m.get(\"finops\", {}).get(\"gross_savings_usd\", 0.0):.4f} (Tokens: {m.get(\"finops\", {}).get(\"tokens_saved\", 0):,})")
except Exception as e:
    print(f"Response: {sys.stdin.read()}")
'
    ;;

  test)
    print_header
    echo "🧪 Running full test suite in containerized test-runner..."
    docker compose -f "$COMPOSE_FILE" run --rm test-runner pytest workplace/tests/ -v --durations=10
    ;;

  test-portal)
    print_header
    echo "🧪 Running portal & swarm integration test suite in container..."
    docker compose -f "$COMPOSE_FILE" run --rm test-runner pytest \
      workplace/tests/test_portal_swarm_governance.py \
      workplace/tests/test_portal_commercial_provisioning.py \
      workplace/tests/test_portal_observability_auth.py -v
    ;;

  test-fleet)
    print_header
    echo "🧪 Running fleet telemetry & FinOps rollup test suite..."
    docker compose -f "$COMPOSE_FILE" run --rm test-runner pytest workplace/tests/test_fleet_telemetry_finops.py -v
    ;;

  gate)
    print_header
    echo "🛡️ Executing 7-Stage Percipience Gatekeeper in container..."
    docker compose -f "$COMPOSE_FILE" run --rm test-runner ./.nb/bin/percipience gate
    ;;

  logs)
    docker compose -f "$COMPOSE_FILE" logs -f
    ;;

  shell)
    print_header
    echo "🐚 Opening shell inside test-runner container..."
    docker compose -f "$COMPOSE_FILE" run --rm --entrypoint /bin/bash test-runner
    ;;

  shell-runner)
    print_header
    echo "🤖 Opening shell inside agent-runner container..."
    docker compose -f "$COMPOSE_FILE" run --rm --entrypoint /bin/bash agent-runner
    ;;

  *)
    usage
    ;;
esac
