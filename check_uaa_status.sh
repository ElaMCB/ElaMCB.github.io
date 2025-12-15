#!/bin/bash
# Quick UAA Status Check - For AI assistants

echo "=== UAA Status Check ==="
echo ""

# Check local status files
if [ -f "docs/uaa-status.json" ]; then
    echo "Status File Found:"
    if command -v jq >/dev/null 2>&1; then
        jq '.' docs/uaa-status.json
    else
        cat docs/uaa-status.json
    fi
    echo ""
else
    echo "[INFO] Status file not found locally (may not be committed to repo)"
    echo ""
fi

# Check diagnostics
if [ -f "docs/uaa-diagnostics.json" ]; then
    echo "Diagnostics Found:"
    if command -v jq >/dev/null 2>&1; then
        jq '.' docs/uaa-diagnostics.json
    else
        cat docs/uaa-diagnostics.json
    fi
    echo ""
fi

# Check latest workflow run via GitHub API if available
if command -v gh >/dev/null 2>&1 && [ -n "$GITHUB_TOKEN" ]; then
    echo "Latest Workflow Runs:"
    gh run list --workflow="unified-autonomous-agent.yml" --limit 3 --json conclusion,status,createdAt,url,displayTitle \
        --jq '.[] | "\(.createdAt) | \(.status)/\(.conclusion) | \(.displayTitle) | \(.url)"' 2>/dev/null || echo "Unable to fetch"
else
    echo "[INFO] GitHub CLI not available - check https://github.com/ElaMCB/ElaMCB.github.io/actions/workflows/unified-autonomous-agent.yml"
fi

echo ""
echo "=== End Status Check ==="
