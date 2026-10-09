#!/usr/bin/env bash
# Percipience SaaS Portal Launcher
# Usage: ./start_portal.sh [port]
# Default port: 3000

set -e

PORT="${1:-${PORTAL_PORT:-3000}}"
HOST="${PORTAL_HOST:-0.0.0.0}"
LOG_LEVEL="${PORTAL_LOG_LEVEL:-info}"

# Set required environment variables
export PYTHONPATH=".:.nb:.nb/core:workplace:workplace/core"
export PERCIPIENCE_DEV_MODE=1
export PERCIPIENCE_TERMINAL_MODE=1

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 Starting Percipience Context Engineering Portal"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Portal Dashboard:     http://127.0.0.1:$PORT/"
echo "🔌 MCP Health Check:     http://127.0.0.1:$PORT/api/health"
echo "📈 Merkle Visualizer:    http://127.0.0.1:$PORT/api/merkle/dag"
echo "🎯 Token Analytics:      http://127.0.0.1:$PORT/api/tokens/summary"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Kill any existing process on the target port
if lsof -ti:$PORT >/dev/null 2>&1; then
    echo "⚠️  Killing existing process on port $PORT..."
    lsof -ti:$PORT | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# Verify server.py exists
if [ ! -f "workplace/portal/server.py" ]; then
    echo "❌ Error: workplace/portal/server.py not found"
    echo "   Please ensure you're running this script from the project root"
    exit 1
fi

# Check if uvicorn is installed
if ! command -v uvicorn &> /dev/null; then
    echo "❌ Error: uvicorn not found"
    echo "   Install with: pip install uvicorn[standard]"
    exit 1
fi

# Start the FastAPI server
echo "🔄 Starting FastAPI server with uvicorn..."
echo ""

cd workplace/portal && uvicorn server:app \
    --host "$HOST" \
    --port "$PORT" \
    --reload \
    --reload-dir . \
    --reload-dir ../core \
    --reload-dir ../../.nb/core \
    --log-level "$LOG_LEVEL"
