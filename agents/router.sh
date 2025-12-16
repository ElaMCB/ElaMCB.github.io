#!/bin/bash
# Unified Agent Router - Orchestrates all agent capabilities

# Don't exit on error - we want to track failures and continue
set +e

# Load shared utilities and config
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source utilities with error handling
UTILS_PATH="$SCRIPT_DIR/shared/utils.sh"
if [ ! -f "$UTILS_PATH" ]; then
    echo "ERROR: utils.sh not found at $UTILS_PATH" >&2
    echo "Script directory: $SCRIPT_DIR" >&2
    echo "Current working directory: $(pwd)" >&2
    ls -la "$SCRIPT_DIR/shared/" >&2 || echo "Cannot list shared directory" >&2
    exit 1
fi

if ! source "$UTILS_PATH" 2>&1; then
    echo "ERROR: Failed to source utils.sh from $UTILS_PATH" >&2
    echo "Script directory: $SCRIPT_DIR" >&2
    echo "Current working directory: $(pwd)" >&2
    exit 1
fi

# Source config with error handling
if ! source "$SCRIPT_DIR/shared/config.sh" 2>&1; then
    log_error "Failed to load config.sh"
    exit 1
fi

log_info "========================================="
log_info "$AGENT_NAME v$AGENT_VERSION"
log_info "========================================="

# Parse command line arguments
CAPABILITY="${1:-all}"
WORKFLOW_EVENT="${2:-}"

log_info "Capability requested: $CAPABILITY"
log_info "Workflow event: $WORKFLOW_EVENT"

# Function to run CI-Fix capability
run_ci_fix() {
    if [ "$ENABLE_CI_FIX" != "true" ]; then
        log_warning "CI-Fix capability is disabled"
        bash "$SCRIPT_DIR/shared/update_status.sh" "ci-fix" "skipped" "Capability disabled"
        return 0
    fi
    
    log_info "Executing CI-Fix capability..."
    if bash "$SCRIPT_DIR/capabilities/ci-fix/ci-fix.sh" "${WORKFLOW_EVENT:-workflow_logs.txt}"; then
        bash "$SCRIPT_DIR/shared/update_status.sh" "ci-fix" "success" "CI-Fix completed successfully"
    else
        local exit_code=$?
        bash "$SCRIPT_DIR/shared/update_status.sh" "ci-fix" "failure" "CI-Fix failed with exit code $exit_code"
        return $exit_code
    fi
}

# Function to run Link-Health capability
run_link_health() {
    if [ "$ENABLE_LINK_HEALTH" != "true" ]; then
        log_warning "Link-Health capability is disabled"
        bash "$SCRIPT_DIR/shared/update_status.sh" "link-health" "skipped" "Capability disabled"
        return 0
    fi
    
    log_info "Executing Link-Health capability..."
    if bash "$SCRIPT_DIR/capabilities/link-health/link-health.sh"; then
        bash "$SCRIPT_DIR/shared/update_status.sh" "link-health" "success" "Link-Health completed successfully"
    else
        local exit_code=$?
        bash "$SCRIPT_DIR/shared/update_status.sh" "link-health" "failure" "Link-Health failed with exit code $exit_code"
        return $exit_code
    fi
}

# Function to run Security capability
run_security() {
    if [ "$ENABLE_SECURITY" != "true" ]; then
        log_warning "Security capability is disabled"
        bash "$SCRIPT_DIR/shared/update_status.sh" "security" "skipped" "Capability disabled"
        return 0
    fi
    
    log_info "Executing Security capability..."
    if bash "$SCRIPT_DIR/capabilities/security/security.sh"; then
        bash "$SCRIPT_DIR/shared/update_status.sh" "security" "success" "Security completed successfully"
    else
        local exit_code=$?
        bash "$SCRIPT_DIR/shared/update_status.sh" "security" "failure" "Security failed with exit code $exit_code"
        return $exit_code
    fi
}

# Main router logic
case "$CAPABILITY" in
    ci-fix|ci)
        run_ci_fix
        ;;
    link-health|lha)
        run_link_health
        ;;
    security|sa)
        run_security
        ;;
    all)
        log_info "Running all enabled capabilities..."
        
        # Track overall success
        OVERALL_SUCCESS=true
        
        # Determine which capabilities to run based on workflow event
        if [ "$WORKFLOW_EVENT" = "workflow_run" ] || [ "$WORKFLOW_EVENT" = "workflow_dispatch" ]; then
            # For workflow events, run CI-Fix
            run_ci_fix || OVERALL_SUCCESS=false
        elif [ "$WORKFLOW_EVENT" = "schedule" ] || [ "$WORKFLOW_EVENT" = "push" ]; then
            # For scheduled/push events, run Link-Health and Security
            run_link_health || OVERALL_SUCCESS=false
            run_security || OVERALL_SUCCESS=false
        else
            # Default: run all
            run_ci_fix || OVERALL_SUCCESS=false
            run_link_health || OVERALL_SUCCESS=false
            run_security || OVERALL_SUCCESS=false
        fi
        
        # Exit with appropriate code
        if [ "$OVERALL_SUCCESS" = "true" ]; then
            log_success "All capabilities completed successfully"
            exit 0
        else
            log_warning "Some capabilities failed, but execution completed"
            exit 1
        fi
        ;;
    *)
        log_error "Unknown capability: $CAPABILITY"
        log_info "Available capabilities: ci-fix, link-health, security, all"
        exit 1
        ;;
esac

# Exit with success if we got here
exit 0

