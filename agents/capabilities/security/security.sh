#!/bin/bash
# Security Capability - Scans for vulnerabilities and exposed secrets

# Don't exit on error - let the router handle error tracking
set +e

# Load shared utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../../shared/utils.sh"
source "$SCRIPT_DIR/../../shared/config.sh"

CAPABILITY_NAME="Security"
LOG_FILE="security-$(date +%Y%m%d-%H%M%S).log"

log_info "Starting $CAPABILITY_NAME capability..."

# Function to run npm audit
run_npm_audit() {
    log_info "Running npm security audit..."
    
    npm audit --json > npm-audit-results.json 2>&1 || true
    
    if [ -f npm-audit-results.json ]; then
        ensure_dependency "jq" "sudo apt-get update && sudo apt-get install -y jq"
        
        local vulnerabilities=$(cat npm-audit-results.json | jq '.vulnerabilities | length' 2>/dev/null || echo "0")
        local critical=$(cat npm-audit-results.json | jq '[.vulnerabilities[] | select(.severity == "critical")] | length' 2>/dev/null || echo "0")
        local high=$(cat npm-audit-results.json | jq '[.vulnerabilities[] | select(.severity == "high")] | length' 2>/dev/null || echo "0")
        local moderate=$(cat npm-audit-results.json | jq '[.vulnerabilities[] | select(.severity == "moderate")] | length' 2>/dev/null || echo "0")
        
        local output_file="${GITHUB_OUTPUT:-/tmp/agent_outputs.txt}"
        echo "vulnerabilities=$vulnerabilities" >> "$output_file"
        echo "critical=$critical" >> "$output_file"
        echo "high=$high" >> "$output_file"
        echo "moderate=$moderate" >> "$output_file"
        
        # Extract vulnerability details
        cat npm-audit-results.json | jq -r '.vulnerabilities | to_entries[] | "\(.key): \(.value.severity) - \(.value.title)"' > vulnerabilities.txt 2>/dev/null || echo "" > vulnerabilities.txt
        
        log_info "Audit complete: $vulnerabilities vulnerabilities ($critical critical, $high high, $moderate moderate)"
    else
        log_warning "No audit results file generated"
        local output_file="${GITHUB_OUTPUT:-/tmp/agent_outputs.txt}"
        echo "vulnerabilities=0" >> "$output_file"
        echo "critical=0" >> "$output_file"
        echo "high=0" >> "$output_file"
        echo "moderate=0" >> "$output_file"
        echo "" > vulnerabilities.txt
    fi
}

# Function to scan for exposed secrets
scan_secrets() {
    log_info "Scanning for exposed secrets..."
    
    # Common secret patterns
    local secret_patterns=(
        "AKIA[0-9A-Z]{16}"  # AWS Access Key
        "sk_live_[0-9a-zA-Z]{32}"  # Stripe
        "ghp_[0-9a-zA-Z]{36}"  # GitHub Personal Token
        "xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[0-9a-zA-Z]{24,32}"  # Slack
        "AIza[0-9A-Za-z\\-_]{35}"  # Google API Key
    )
    
    local secrets_found=0
    local secret_details=""
    
    for pattern in "${secret_patterns[@]}"; do
        local matches=$(grep -r -E "$pattern" . --exclude-dir=node_modules --exclude-dir=.git --exclude="*.json" 2>/dev/null | wc -l || echo "0")
        if [ "$matches" -gt "0" ]; then
            secrets_found=$((secrets_found + matches))
            secret_details+="Pattern $pattern: $matches matches\n"
        fi
    done
    
    local output_file="${GITHUB_OUTPUT:-/tmp/agent_outputs.txt}"
    echo "secrets_found=$secrets_found" >> "$output_file"
    {
        echo "secret_details<<EOF"
        echo -e "$secret_details"
        echo "EOF"
    } >> "$output_file"
    
    if [ "$secrets_found" -gt "0" ]; then
        log_warning "Found $secrets_found potential exposed secrets!"
    else
        log_info "No exposed secrets detected"
    fi
}

# Function to auto-fix vulnerabilities
auto_fix_vulnerabilities() {
    local critical="$1"
    local high="$2"
    
    if [ "$critical" -gt "0" ] || [ "$high" -gt "0" ]; then
        log_warning "Critical or high severity vulnerabilities found - skipping auto-fix"
        return 1
    fi
    
    log_info "Attempting to auto-fix moderate/low severity vulnerabilities..."
    
    npm audit fix --force || npm audit fix || true
    
    if [ -n "$(git status --porcelain package-lock.json)" ]; then
        commit_and_push "Auto-fix npm vulnerabilities (moderate/low severity)" "package-lock.json"
        log_success "Vulnerabilities fixed and committed"
    else
        log_info "No changes to package-lock.json"
    fi
}

# Function to create security report
create_security_report() {
    local vulnerabilities="$1"
    local critical="$2"
    local high="$3"
    local moderate="$4"
    local secrets_found="$5"
    local secret_details="$6"
    
    cat > docs/security-report.md <<EOF
# Security Report - $(date +%Y-%m-%d)

## Summary
- **Total Vulnerabilities**: $vulnerabilities
- **Critical**: $critical
- **High**: $high
- **Moderate**: $moderate
- **Exposed Secrets**: $secrets_found

## Vulnerabilities

\`\`\`
$(cat vulnerabilities.txt 2>/dev/null || echo "No vulnerabilities found")
\`\`\`

$(if [ "$secrets_found" -gt "0" ]; then
    echo "## Exposed Secrets"
    echo ""
    echo "⚠️ **CRITICAL**: Potential secrets detected in codebase!"
    echo ""
    echo "\`\`\`"
    echo "$secret_details"
    echo "\`\`\`"
fi)

## Recommendations

$(if [ "$critical" -gt "0" ]; then echo "1. **URGENT**: Fix critical vulnerabilities immediately"; fi)
$(if [ "$high" -gt "0" ]; then echo "2. **HIGH PRIORITY**: Address high severity vulnerabilities"; fi)
$(if [ "$secrets_found" -gt "0" ]; then echo "3. **CRITICAL**: Remove exposed secrets and rotate credentials"; fi)

---
*Generated by $AGENT_NAME - $CAPABILITY_NAME capability*
EOF
    
    log_info "Security report created"
}

# Function to create critical security issue
create_critical_issue() {
    local critical_issues="$1"
    local high_issues="$2"
    local critical="$3"
    local high="$4"
    local moderate="$5"
    local total="$6"
    local secrets_found="$7"
    local secret_details="$8"
    
    local title="CRITICAL - $critical_issues critical security issues detected"
    local body="## Critical Security Alert

**Critical Issues**: $critical_issues
**High Issues**: $high_issues

## Vulnerabilities

- **Critical**: $critical
- **High**: $high
- **Moderate**: $moderate
- **Total**: $total

$(if [ "$secrets_found" -gt "0" ]; then
    echo "## ⚠️ EXPOSED SECRETS DETECTED"
    echo ""
    echo "**Secrets Found**: $secrets_found"
    echo ""
    echo "\`\`\`"
    echo "$secret_details"
    echo "\`\`\`"
    echo ""
    echo "**ACTION REQUIRED**: Remove exposed secrets immediately and rotate all credentials!"
fi)

## Vulnerability Details

\`\`\`
$(cat vulnerabilities.txt 2>/dev/null || echo "No details available")
\`\`\`

## Immediate Actions Required

1. Review all critical vulnerabilities
2. Update dependencies with security patches
3. $(if [ "$secrets_found" -gt "0" ]; then echo "Remove exposed secrets and rotate credentials"; else echo "Review high severity issues"; fi)
4. Run \`npm audit fix\` for auto-fixable issues

---
*Generated by $AGENT_NAME - $CAPABILITY_NAME capability*"
    
    create_github_issue "$title" "$body" "security,critical,automated"
    log_info "Created critical security issue"
}

# Main execution
main() {
    run_npm_audit
    scan_secrets
    
    local output_file="${GITHUB_OUTPUT:-/tmp/agent_outputs.txt}"
    local vulnerabilities=$(grep '^vulnerabilities=' "$output_file" 2>/dev/null | cut -d'=' -f2 || echo "0")
    local critical=$(grep '^critical=' "$output_file" 2>/dev/null | cut -d'=' -f2 || echo "0")
    local high=$(grep '^high=' "$output_file" 2>/dev/null | cut -d'=' -f2 || echo "0")
    local moderate=$(grep '^moderate=' "$output_file" 2>/dev/null | cut -d'=' -f2 || echo "0")
    local secrets_found=$(grep '^secrets_found=' "$output_file" 2>/dev/null | cut -d'=' -f2 || echo "0")
    local secret_details=$(grep -A 100 '^secret_details<<EOF' "$output_file" 2>/dev/null | grep -v '^secret_details<<EOF' | grep -v '^EOF$' || echo "")
    
    # Calculate critical issues
    local critical_issues=$critical
    if [ "$secrets_found" -gt "0" ]; then
        critical_issues=$((critical_issues + 1))
    fi
    local high_issues=$high
    
    # Create report
    create_security_report "$vulnerabilities" "$critical" "$high" "$moderate" "$secrets_found" "$secret_details"
    
    # Auto-fix if appropriate
    if [ "$SECURITY_AUTO_FIX_MODERATE" = "true" ] && [ "$critical" -eq "0" ] && [ "$high" -eq "0" ]; then
        auto_fix_vulnerabilities "$critical" "$high"
    fi
    
    # Create critical issue if needed
    if [ "$critical_issues" -gt "0" ] || [ "$high_issues" -gt "0" ] || [ "$secrets_found" -gt "0" ]; then
        create_critical_issue "$critical_issues" "$high_issues" "$critical" "$high" "$moderate" "$vulnerabilities" "$secrets_found" "$secret_details"
    else
        log_success "Security scan passed! No vulnerabilities or security issues detected."
    fi
    
    log_success "$CAPABILITY_NAME capability completed"
}

# Run if executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi

