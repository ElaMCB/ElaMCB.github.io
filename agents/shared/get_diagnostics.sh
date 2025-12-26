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

# Check for recent workflow runs (using GitHub REST API via curl, no GitHub CLI needed)
if [ -n "$GITHUB_TOKEN" ] && [ -n "$GITHUB_REPOSITORY" ]; then
    echo "Recent Workflow Runs:"
    local owner_repo="${GITHUB_REPOSITORY}"
    local workflow_file="unified-autonomous-agent.yml"
    local api_url="https://api.github.com/repos/${owner_repo}/actions/workflows/${workflow_file}/runs?per_page=5"
    
    local response
    response=$(curl -s -H "Authorization: Bearer $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        "$api_url" 2>/dev/null)
    
    if command_exists jq; then
        echo "$response" | jq -r '.workflow_runs[]? | "\(.created_at) - \(.status)/\(.conclusion) - \(.html_url)"' 2>/dev/null || echo "Unable to fetch workflow runs"
    else
        echo "Unable to parse workflow runs (jq not available)"
    fi
fi

