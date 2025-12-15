#!/bin/bash
# Unified Agent Router - Orchestrates all agent capabilities

set -e

# Load shared utilities and config
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/shared/utils.sh"
source "$SCRIPT_DIR/shared/config.sh"

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
        return 0
    fi
    
    log_info "Executing CI-Fix capability..."
    bash "$SCRIPT_DIR/capabilities/ci-fix/ci-fix.sh" "${WORKFLOW_EVENT:-workflow_logs.txt}"
}

# Function to run Link-Health capability
run_link_health() {
    if [ "$ENABLE_LINK_HEALTH" != "true" ]; then
        log_warning "Link-Health capability is disabled"
        return 0
    fi
    
    log_info "Executing Link-Health capability..."
    bash "$SCRIPT_DIR/capabilities/link-health/link-health.sh"
}

# Function to run Security capability
run_security() {
    if [ "$ENABLE_SECURITY" != "true" ]; then
        log_warning "Security capability is disabled"
        return 0
    fi
    
    log_info "Executing Security capability..."
    bash "$SCRIPT_DIR/capabilities/security/security.sh"
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
        
        # Determine which capabilities to run based on workflow event
        if [ "$WORKFLOW_EVENT" = "workflow_run" ] || [ "$WORKFLOW_EVENT" = "workflow_dispatch" ]; then
            # For workflow events, run CI-Fix
            run_ci_fix
        elif [ "$WORKFLOW_EVENT" = "schedule" ] || [ "$WORKFLOW_EVENT" = "push" ]; then
            # For scheduled/push events, run Link-Health and Security
            run_link_health
            run_security
        else
            # Default: run all
            run_ci_fix
            run_link_health
            run_security
        fi
        ;;
    *)
        log_error "Unknown capability: $CAPABILITY"
        log_info "Available capabilities: ci-fix, link-health, security, all"
        exit 1
        ;;
esac

log_success "Unified Agent execution completed"

