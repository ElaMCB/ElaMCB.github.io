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
    local status_file="docs/uaa-status.json"
    
    # Get current timestamp - ensure it's executed, not literal
    local timestamp
    timestamp=$(date -u +"%Y-%m-%d %H:%M:%S UTC" 2>/dev/null || echo "N/A")
    
    # Get workflow status from file
    local workflow_status_str="unknown"
    local workflow_last_run="N/A"
    if [ -f "$status_file" ] && command -v jq >/dev/null 2>&1; then
        workflow_status_str=$(jq -r '.workflow_status // "unknown"' "$status_file" 2>/dev/null || echo "unknown")
        workflow_last_run=$(jq -r '.last_updated // "N/A"' "$status_file" 2>/dev/null | sed 's/T/ /' | sed 's/Z/ UTC/' || echo "N/A")
    fi
    
    # Get capability statuses
    local ci_fix_status=$(get_capability_status "ci-fix")
    local link_health_status=$(get_capability_status "link-health")
    local security_status=$(get_capability_status "security")
    
    # Get last run times
    local ci_fix_time=$(get_last_run_time "ci-fix")
    local link_health_time=$(get_last_run_time "link-health")
    local security_time=$(get_last_run_time "security")
    
    # Format last run times
    ci_fix_time=$(echo "$ci_fix_time" | sed 's/T/ /' | sed 's/Z/ UTC/' | sed 's/N\/A/N\/A/')
    link_health_time=$(echo "$link_health_time" | sed 's/T/ /' | sed 's/Z/ UTC/' | sed 's/N\/A/N\/A/')
    security_time=$(echo "$security_time" | sed 's/T/ /' | sed 's/Z/ UTC/' | sed 's/N\/A/N\/A/')
    
    # Get recent activity
    local recent_activity=$(get_recent_activity)
    
    cat <<EOF
## UAA Status Dashboard

**Last Updated:** $timestamp

| Component | Status | Last Run | Details |
|-----------|--------|----------|---------|
| **UAA Workflow** | $(get_status_badge "$workflow_status_str") | $workflow_last_run | [View Runs](https://github.com/${GITHUB_REPOSITORY:-ElaMCB/ElaMCB.github.io}/actions/workflows/unified-autonomous-agent.yml) |
| **CI-Fix Capability** | $(get_status_badge "$ci_fix_status") | $ci_fix_time | [View Status](./docs/uaa-status.json) |
| **Link-Health Capability** | $(get_status_badge "$link_health_status") | $link_health_time | [View Status](./docs/uaa-status.json) |
| **Security Capability** | $(get_status_badge "$security_status") | $security_time | [View Status](./docs/uaa-status.json) |

### Recent Activity
$recent_activity

### Quick Links
- [UAA Success Indicators Guide](./docs/UAA_SUCCESS_INDICATORS.md)
- [UAA Architecture](./docs/UNIFIED_AGENT_ARCHITECTURE.html)
- [Agent README](./agents/README.md)
- [View All Workflow Runs](https://github.com/${GITHUB_REPOSITORY:-ElaMCB/ElaMCB.github.io}/actions/workflows/unified-autonomous-agent.yml)

---
*Dashboard auto-updated by UAA after each run*
EOF
}

# Helper functions
get_status_badge() {
    local status="$1"
    case "$status" in
        success|completed)
            echo "[OK] Success"
            ;;
        failure|failed)
            echo "[FAILED] Failed"
            ;;
        in_progress|queued)
            echo "[RUNNING] Running"
            ;;
        cancelled)
            echo "[CANCELLED] Cancelled"
            ;;
        *)
            echo "[UNKNOWN] Unknown"
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
    
    if [ -f "$status_file" ] && command -v jq >/dev/null 2>&1; then
        local activity=$(jq -r '.recent_activity[]? | "- **\(.time)**: \(.message)"' "$status_file" 2>/dev/null | head -5)
        if [ -n "$activity" ]; then
            echo "$activity"
        else
            echo "- Dashboard will update after first UAA run"
        fi
    else
        echo "- Dashboard will update after first UAA run"
    fi
}

# Main execution
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    generate_dashboard
fi

