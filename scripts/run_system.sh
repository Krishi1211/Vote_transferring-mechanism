#!/bin/bash

echo "================================================"
echo "  Secure Vote-Transfer System - Startup"
echo "================================================"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$PROJECT_ROOT"

echo "[1/3] Starting Voting Node (Backend)..."
cd server/voting_node
python3 app.py &
VOTING_PID=$!

sleep 2

echo "[2/3] Starting Observer Node (Dashboard)..."
cd ../observer_node
python3 display_server.py &
OBSERVER_PID=$!

sleep 2

echo "[3/3] Opening web interfaces..."
echo ""
echo "================================================"
echo "  System is running!"
echo "================================================"
echo ""
echo "  [1] Voter Booth:    http://localhost:5000"
echo "  [2] Admin Dashboard: http://localhost:5001"
echo ""
echo "  Process IDs:"
echo "    Voting Node: $VOTING_PID"
echo "    Observer Node: $OBSERVER_PID"
echo ""
echo "  Press Ctrl+C to stop all services"
echo "================================================"
echo ""

# Open browsers (platform-specific)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open http://localhost:5000
    sleep 1
    open http://localhost:5001
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open http://localhost:5000 2>/dev/null
    sleep 1
    xdg-open http://localhost:5001 2>/dev/null
fi

# Wait for Ctrl+C
trap "kill $VOTING_PID $OBSERVER_PID; exit" INT
wait
