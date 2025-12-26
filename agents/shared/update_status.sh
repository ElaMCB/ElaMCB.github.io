#!/bin/bash
# Update UAA Status JSON file after capability execution

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/utils.sh"

CAPABILITY="$1"
STATUS="$2"  # success, failure, skipped
MESSAGE="${3:-}"
OUTPUT_FILE="docs/uaa-status.json"

# Ensure docs directory exists
mkdir -p docs

# Initialize or update status file
if [ ! -f "$OUTPUT_FILE" ]; then
    cat > "$OUTPUT_FILE" <<EOF
{
  "last_updated": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "workflow_status": "unknown",
  "capabilities": {
    "ci-fix": {
      "status": "unknown",
      "last_run": "N/A",
      "last_success": "N/A",
      "last_failure": "N/A",
      "total_runs": 0,
      "success_count": 0,
      "failure_count": 0
    },
    "link-health": {
      "status": "unknown",
      "last_run": "N/A",
      "last_success": "N/A",
      "last_failure": "N/A",
      "total_runs": 0,
      "success_count": 0,
      "failure_count": 0
    },
    "security": {
      "status": "unknown",
      "last_run": "N/A",
      "last_success": "N/A",
      "last_failure": "N/A",
      "total_runs": 0,
      "success_count": 0,
      "failure_count": 0
    }
  },
  "recent_activity": []
}
EOF
fi

# Function to generate diagnostic report
generate_diagnostic_report() {
    local capability="$1"
    local error_msg="$2"
    local diagnostic_file="docs/uaa-diagnostics.json"
    
    cat > "$diagnostic_file" <<EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "capability": "$capability",
  "status": "failure",
  "error_message": "$error_msg",
  "system_info": {
    "os": "$(uname -s)",
    "arch": "$(uname -m)",
    "shell": "$SHELL",
    "node_version": "$(node --version 2>/dev/null || echo 'N/A')",
    "git_version": "$(git --version 2>/dev/null || echo 'N/A')"
  },
  "environment": {
    "github_repo": "${GITHUB_REPOSITORY:-N/A}",
    "github_ref": "${GITHUB_REF:-N/A}",
    "github_sha": "${GITHUB_SHA:-N/A}",
    "workflow": "${GITHUB_WORKFLOW:-N/A}"
  },
  "capability_specific": {
    "script_exists": "$([ -f "agents/capabilities/$capability/$capability.sh" ] && echo 'true' || echo 'false')",
    "script_executable": "$([ -x "agents/capabilities/$capability/$capability.sh" ] && echo 'true' || echo 'false')",
    "shared_utils_exist": "$([ -f "agents/shared/utils.sh" ] && echo 'true' || echo 'false')",
    "config_exists": "$([ -f "agents/shared/config.sh" ] && echo 'true' || echo 'false')"
  },
  "recent_logs": "$(tail -20 /tmp/uaa-${capability}.log 2>/dev/null | jq -Rs . 2>/dev/null || echo 'null')"
}
EOF
    
    log_info "Diagnostic report generated: $diagnostic_file"
}

# Update capability status
if [ -n "$CAPABILITY" ] && [ -n "$STATUS" ]; then
    # Try to ensure jq is available, but don't fail if we can't install it
    if ! command_exists "jq"; then
        log_warning "jq not found, attempting to install..."
        ensure_dependency "jq" "sudo apt-get update && sudo apt-get install -y jq" || {
            log_warning "Could not install jq, will create status file without JSON updates"
        }
    fi
    
    # Get timestamp - ensure it's not empty
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || echo "")
    if [ -z "$timestamp" ]; then
        log_error "Failed to get timestamp, using fallback"
        timestamp="N/A"
    fi
    
    # Update capability status using jq if available, otherwise create simple status
    if command_exists "jq"; then
        jq --arg cap "$CAPABILITY" \
           --arg status "$STATUS" \
           --arg time "$timestamp" \
           --arg msg "$MESSAGE" \
           '.capabilities[$cap].status = $status |
            .capabilities[$cap].last_run = $time |
            .capabilities[$cap].total_runs += 1 |
            (if $status == "success" then
              .capabilities[$cap].last_success = $time |
              .capabilities[$cap].success_count += 1
             elif $status == "failure" then
              .capabilities[$cap].last_failure = $time |
              .capabilities[$cap].failure_count += 1
             else . end) |
            .last_updated = $time |
            .recent_activity = ([{
              "time": $time,
              "capability": $cap,
              "status": $status,
              "message": $msg
            }] + .recent_activity) | .recent_activity = .recent_activity[0:10]' \
           "$OUTPUT_FILE" > "${OUTPUT_FILE}.tmp" 2>/dev/null && mv "${OUTPUT_FILE}.tmp" "$OUTPUT_FILE" || {
            log_warning "Failed to update status with jq, creating basic status"
            # Fallback: create a simple status update
            echo "{\"last_updated\":\"$timestamp\",\"capabilities\":{\"$CAPABILITY\":{\"status\":\"$STATUS\",\"last_run\":\"$timestamp\"}}}" > "$OUTPUT_FILE"
        }
    else
        log_warning "jq not available, creating basic status file"
        echo "{\"last_updated\":\"$timestamp\",\"capabilities\":{\"$CAPABILITY\":{\"status\":\"$STATUS\",\"last_run\":\"$timestamp\"}}}" > "$OUTPUT_FILE"
    fi
    
    log_info "Updated status for $CAPABILITY: $STATUS"
fi

# Generate diagnostic report if failed
if [ "$STATUS" = "failure" ]; then
    generate_diagnostic_report "$CAPABILITY" "$MESSAGE"
fi

