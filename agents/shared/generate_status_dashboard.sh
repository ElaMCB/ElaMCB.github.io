#!/bin/bash
# Generate UAA Status Dashboard for README

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/utils.sh"

# Get latest workflow run status
get_workflow_status() {
    local workflow_name="$1"
    
    # Try to get from GitHub API if available
    if command_exists gh && [ -n "$GITHUB_TOKEN" ]; then
        gh api repos/$GITHUB_REPOSITORY/actions/workflows/unified-autonomous-agent.yml/runs \
            --jq '.workflow_runs[0] | {status: .status, conclusion: .conclusion, created_at: .created_at, html_url: .html_url}' 2>/dev/null || echo '{"status":"unknown","conclusion":"unknown"}'
    else
        echo '{"status":"unknown","conclusion":"unknown"}'
    fi
}

# Get capability-specific status
get_capability_status() {
    local capability="$1"
    local status_file="docs/uaa-status.json"
    
    if [ -f "$status_file" ]; then
        jq -r ".capabilities.$capability.status // \"unknown\"" "$status_file" 2>/dev/null || echo "unknown"
    else
        echo "unknown"
    fi
}

# Generate dashboard markdown
generate_dashboard() {
    local workflow_status=$(get_workflow_status "unified-autonomous-agent")
    local ci_fix_status=$(get_capability_status "ci-fix")
    local link_health_status=$(get_capability_status "link-health")
    local security_status=$(get_capability_status "security")
    
    cat <<EOF
## UAA Status Dashboard

**Last Updated:** $(date -u +"%Y-%m-%d %H:%M:%S UTC")

| Component | Status | Last Run | Details |
|-----------|--------|----------|---------|
| **UAA Workflow** | $(get_status_badge "$(echo "$workflow_status" | jq -r '.conclusion // "unknown"')") | $(echo "$workflow_status" | jq -r '.created_at // "N/A"') | [View Run]($(echo "$workflow_status" | jq -r '.html_url // "#"')) |
| **CI-Fix Capability** | $(get_status_badge "$ci_fix_status") | $(get_last_run_time "ci-fix") | [View Logs](./docs/uaa-status.json#ci-fix) |
| **Link-Health Capability** | $(get_status_badge "$link_health_status") | $(get_last_run_time "link-health") | [View Logs](./docs/uaa-status.json#link-health) |
| **Security Capability** | $(get_status_badge "$security_status") | $(get_last_run_time "security") | [View Logs](./docs/uaa-status.json#security) |

### Recent Activity
$(get_recent_activity)

### Quick Links
- [UAA Success Indicators Guide](./docs/UAA_SUCCESS_INDICATORS.md)
- [UAA Architecture](./docs/UNIFIED_AGENT_ARCHITECTURE.html)
- [Agent README](./agents/README.md)
- [View All Workflow Runs](https://github.com/$GITHUB_REPOSITORY/actions/workflows/unified-autonomous-agent.yml)

---
*Dashboard auto-updated by UAA after each run*
EOF
}

# Helper functions
get_status_badge() {
    local status="$1"
    case "$status" in
        success|completed)
            echo "✅ Success"
            ;;
        failure|failed)
            echo "❌ Failed"
            ;;
        in_progress|queued)
            echo "🟡 Running"
            ;;
        cancelled)
            echo "⚪ Cancelled"
            ;;
        *)
            echo "⚪ Unknown"
            ;;
    esac
}

get_last_run_time() {
    local capability="$1"
    local status_file="docs/uaa-status.json"
    
    if [ -f "$status_file" ]; then
        jq -r ".capabilities.$capability.last_run // \"N/A\"" "$status_file" 2>/dev/null || echo "N/A"
    else
        echo "N/A"
    fi
}

get_recent_activity() {
    local status_file="docs/uaa-status.json"
    
    if [ -f "$status_file" ]; then
        jq -r '.recent_activity[] | "- **\(.time)**: \(.message)"' "$status_file" 2>/dev/null | head -5 || echo "- No recent activity"
    else
        echo "- No recent activity"
    fi
}

# Main execution
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    generate_dashboard
fi

