#!/bin/bash
# Get UAA Diagnostics - For AI assistant to query UAA status

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DIAGNOSTIC_FILE="docs/uaa-diagnostics.json"
STATUS_FILE="docs/uaa-status.json"

echo "=== UAA Diagnostic Report ==="
echo ""

if [ -f "$STATUS_FILE" ]; then
    echo "Current Status:"
    cat "$STATUS_FILE" | jq '.' 2>/dev/null || cat "$STATUS_FILE"
    echo ""
else
    echo "[WARNING] Status file not found: $STATUS_FILE"
    echo "UAA may not have run yet."
    echo ""
fi

if [ -f "$DIAGNOSTIC_FILE" ]; then
    echo "Latest Diagnostics:"
    cat "$DIAGNOSTIC_FILE" | jq '.' 2>/dev/null || cat "$DIAGNOSTIC_FILE"
    echo ""
else
    echo "[OK] No diagnostic file found - UAA is running successfully or hasn't encountered errors."
    echo ""
fi

# Check for recent workflow runs
if command_exists gh && [ -n "$GITHUB_TOKEN" ]; then
    echo "Recent Workflow Runs:"
    gh run list --workflow="unified-autonomous-agent.yml" --limit 5 --json conclusion,status,createdAt,url \
        --jq '.[] | "\(.createdAt) - \(.status)/\(.conclusion) - \(.url)"' 2>/dev/null || echo "Unable to fetch workflow runs"
fi

