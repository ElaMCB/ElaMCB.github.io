#!/bin/bash
# Quick UAA Status Check Script

echo "=== UAA Status Check ==="
echo ""

# Check if status files exist
echo "Status Files:"
if [ -f "docs/uaa-status.json" ]; then
    echo "  [OK] uaa-status.json exists"
    echo "  Content:"
    cat docs/uaa-status.json | jq '.' 2>/dev/null || cat docs/uaa-status.json
else
    echo "  [MISSING] uaa-status.json NOT FOUND - UAA hasn't run yet"
fi
echo ""

if [ -f "docs/uaa-diagnostics.json" ]; then
    echo "  [WARNING] uaa-diagnostics.json exists (errors occurred)"
    echo "  Content:"
    cat docs/uaa-diagnostics.json | jq '.' 2>/dev/null || cat docs/uaa-diagnostics.json
else
    echo "  [OK] No diagnostic file (no errors or UAA hasn't run)"
fi
echo ""

# Check workflow file
echo "Workflow File:"
if [ -f ".github/workflows/unified-autonomous-agent.yml" ]; then
    echo "  [OK] Workflow file exists"
    # Check for common syntax issues
    if grep -q "GITHUB_REF_NAME" ".github/workflows/unified-autonomous-agent.yml"; then
        echo "  [OK] GITHUB_REF_NAME is configured"
    else
        echo "  [WARNING] GITHUB_REF_NAME might be missing"
    fi
else
    echo "  [ERROR] Workflow file NOT FOUND"
fi
echo ""

# Check agent scripts
echo "Agent Scripts:"
for script in "agents/router.sh" "agents/shared/utils.sh" "agents/shared/config.sh" "agents/shared/update_status.sh"; do
    if [ -f "$script" ]; then
        echo "  [OK] $script exists"
    else
        echo "  [ERROR] $script NOT FOUND"
    fi
done
echo ""

# Check recent commits
echo "Recent Commits:"
git log --oneline -5 | head -5
echo ""

# Check for github-actions commits
echo "GitHub Actions Commits:"
if git log --all --author="github-actions" --oneline -5 | grep -q .; then
    git log --all --author="github-actions" --oneline -5
    echo "  [OK] UAA has made commits"
else
    echo "  [WARNING] No commits from github-actions bot yet"
    echo "  This means UAA hasn't run or hasn't completed successfully"
fi
echo ""

echo "=== Recommendations ==="
echo "1. Check GitHub Actions: https://github.com/ElaMCB/ElaMCB.github.io/actions"
echo "2. Look for 'Unified Autonomous Agent' workflow"
echo "3. If no runs exist, manually trigger it from Actions tab"
echo "4. If runs exist but failed, check the logs for errors"

