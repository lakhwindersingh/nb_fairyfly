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
  echo "  build         Build all Docker images (portal, tree-sitter-daemon, test-runner)"
  echo "  up            Start portal & tree-sitter daemon detached and wait for healthy state"
  echo "  down          Stop and remove containers and local networks"
  echo "  status        Check health status of running services"
  echo "  test          Run full test suite (pytest workplace/tests/) inside container"
  echo "  test-portal   Run portal integration tests inside container"
  echo "  gate          Execute 7-stage CI/CD gatekeeper (./.nb/bin/percipience gate) in container"
  echo "  logs          Follow live container logs"
  echo "  shell         Open interactive bash shell in test-runner container"
  echo ""
  exit 1
}

CMD="${1:-}"

case "$CMD" in
  build)
    print_header
    echo "📦 Building all Percipience container images..."
    docker compose -f "$COMPOSE_FILE" build
    echo "✅ Build completed successfully."
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

  down)
    print_header
    echo "🛑 Stopping and cleaning up Percipience containers..."
    docker compose -f "$COMPOSE_FILE" down --remove-orphans
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

  *)
    usage
    ;;
esac
