#!/bin/bash
# Configuration file for unified agent

# Agent metadata
AGENT_NAME="Unified Autonomous Agent"
AGENT_VERSION="1.0.0"

# Capability settings
ENABLE_CI_FIX=true
ENABLE_LINK_HEALTH=true
ENABLE_SECURITY=true

# CI Fix settings
CI_FIX_MONITORED_WORKFLOWS=("CI" "Tests" "Build" "LHA - Link Health Agent" "SA - Security Agent")
CI_FIX_AUTO_COMMIT=true

# Link Health settings
LINK_HEALTH_SCHEDULE="0 9 * * 1"  # Every Monday at 9 AM UTC
LINK_HEALTH_SKIP_DOMAINS=("github.com" "linkedin.com" "twitter.com" "mailto:")

# Security settings
SECURITY_SCHEDULE="0 10 * * 1"  # Every Monday at 10 AM UTC
SECURITY_AUTO_FIX_MODERATE=true
SECURITY_AUTO_FIX_LOW=true

# GitHub settings
GITHUB_REPO="${GITHUB_REPOSITORY}"
GITHUB_TOKEN="${GITHUB_TOKEN}"

# Output settings
VERBOSE=false
DRY_RUN=false

