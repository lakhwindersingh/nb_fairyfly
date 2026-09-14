#!/usr/bin/env bash
# Starts the Percipience SaaS Portal locally
PORT=${1:-3000}
echo "Starting Percipience Cloud SaaS Portal on port ${PORT}..."
python3 workplace/portal/server.py "${PORT}"
