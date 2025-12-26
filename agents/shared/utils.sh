#!/bin/bash
# Shared utilities for unified agent capabilities

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# GitHub API helpers (using REST API via curl, no GitHub CLI needed)
create_github_issue() {
    local title="$1"
    local body="$2"
    local labels="$3"
    
    if [ -z "$GITHUB_TOKEN" ] || [ -z "$GITHUB_REPOSITORY" ]; then
        log_error "GITHUB_TOKEN and GITHUB_REPOSITORY must be set"
        return 1
    fi
    
    local owner_repo="${GITHUB_REPOSITORY}"
    local api_url="https://api.github.com/repos/${owner_repo}/issues"
    
    # Build JSON payload (use jq if available for proper escaping)
    local json_body
    local labels_array=""
    
    # Convert comma-separated labels to JSON array format
    if [ -n "$labels" ]; then
        # Convert "label1,label2" to ["label1","label2"]
        labels_array=$(echo "$labels" | sed 's/,/","/g' | sed 's/^/"/' | sed 's/$/"/')
    fi
    
    if command_exists jq; then
        # Use jq for proper JSON escaping
        if [ -n "$labels" ]; then
            # Build labels array with jq
            local labels_json=$(echo "$labels" | tr ',' '\n' | jq -R . | jq -s . 2>/dev/null)
            json_body=$(jq -n \
                --arg title "$title" \
                --arg body "$body" \
                --argjson labels "$labels_json" \
                '{title: $title, body: $body, labels: $labels}' 2>/dev/null)
        else
            json_body=$(jq -n --arg title "$title" --arg body "$body" '{title: $title, body: $body}' 2>/dev/null)
        fi
    fi
    
    # Fallback if jq failed or not available
    if [ -z "$json_body" ]; then
        # Manual JSON escaping (basic - may fail with complex strings)
        local title_escaped=$(echo "$title" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')
        local body_escaped=$(echo "$body" | sed 's/\\/\\\\/g' | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')
        if [ -n "$labels" ]; then
            json_body="{\"title\":\"$title_escaped\",\"body\":\"$body_escaped\",\"labels\":[$labels_array]}"
        else
            json_body="{\"title\":\"$title_escaped\",\"body\":\"$body_escaped\"}"
        fi
    fi
    
    # Create issue via API
    local response
    response=$(curl -s -w "\n%{http_code}" -X POST "$api_url" \
        -H "Authorization: Bearer $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -H "Content-Type: application/json" \
        -d "$json_body" 2>/dev/null)
    
    local http_code=$(echo "$response" | tail -n1)
    local body_response=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -eq 201 ]; then
        log_success "GitHub issue created successfully"
        return 0
    else
        log_error "Failed to create GitHub issue (HTTP $http_code): $body_response"
        return 1
    fi
}

create_github_pr() {
    local title="$1"
    local body="$2"
    local branch="$3"
    local labels="$4"
    
    if [ -z "$GITHUB_TOKEN" ] || [ -z "$GITHUB_REPOSITORY" ]; then
        log_error "GITHUB_TOKEN and GITHUB_REPOSITORY must be set"
        return 1
    fi
    
    local owner_repo="${GITHUB_REPOSITORY}"
    local default_branch="${GITHUB_REF_NAME:-main}"
    local api_url="https://api.github.com/repos/${owner_repo}/pulls"
    
    # Build JSON payload (handle jq availability)
    local json_body
    if command_exists jq; then
        json_body=$(jq -n \
            --arg title "$title" \
            --arg body "$body" \
            --arg head "$branch" \
            --arg base "$default_branch" \
            '{title: $title, body: $body, head: $head, base: $base}' 2>/dev/null || \
            echo "{\"title\":\"$(echo "$title" | sed 's/"/\\"/g')\",\"body\":\"$(echo "$body" | sed 's/"/\\"/g' | tr '\n' ' ')\",\"head\":\"$branch\",\"base\":\"$default_branch\"}")
    else
        # Fallback: manual JSON escaping (basic)
        local title_escaped=$(echo "$title" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')
        local body_escaped=$(echo "$body" | sed 's/"/\\"/g' | sed ':a;N;$!ba;s/\n/\\n/g')
        json_body="{\"title\":\"$title_escaped\",\"body\":\"$body_escaped\",\"head\":\"$branch\",\"base\":\"$default_branch\"}"
    fi
    
    # Create PR via API
    local response
    response=$(curl -s -w "\n%{http_code}" -X POST "$api_url" \
        -H "Authorization: Bearer $GITHUB_TOKEN" \
        -H "Accept: application/vnd.github.v3+json" \
        -H "Content-Type: application/json" \
        -d "$json_body" 2>/dev/null)
    
    local http_code=$(echo "$response" | tail -n1)
    local body_response=$(echo "$response" | sed '$d')
    
    if [ "$http_code" -eq 201 ]; then
        log_success "GitHub PR created successfully"
        
        # Add labels if provided
        if [ -n "$labels" ]; then
            local pr_number
            if command_exists jq; then
                pr_number=$(echo "$body_response" | jq -r '.number' 2>/dev/null)
            else
                # Basic extraction without jq
                pr_number=$(echo "$body_response" | grep -o '"number":[0-9]*' | grep -o '[0-9]*' | head -1)
            fi
            
            if [ -n "$pr_number" ] && [ "$pr_number" != "null" ] && [ "$pr_number" != "" ]; then
                local labels_array=$(echo "$labels" | sed 's/,/","/g' | sed 's/^/"/' | sed 's/$/"/')
                local labels_payload="{\"labels\": [$labels_array]}"
                
                curl -s -X POST "https://api.github.com/repos/${owner_repo}/issues/${pr_number}/labels" \
                    -H "Authorization: Bearer $GITHUB_TOKEN" \
                    -H "Accept: application/vnd.github.v3+json" \
                    -H "Content-Type: application/json" \
                    -d "$labels_payload" >/dev/null 2>&1 || log_warning "Failed to add labels to PR"
            fi
        fi
        
        return 0
    else
        # Check if error is because PR already exists (422)
        if [ "$http_code" -eq 422 ]; then
            log_warning "PR may already exist or branch not found"
            return 0
        fi
        log_error "Failed to create GitHub PR (HTTP $http_code): $body_response"
        return 1
    fi
}

# Git helpers
setup_git() {
    git config user.name "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
}

commit_and_push() {
    local message="$1"
    local files="$2"
    
    setup_git
    git add $files
    git commit -m "$message" || return 1
    
    # Use GITHUB_REF_NAME if available (GitHub Actions), otherwise use current branch
    local branch="${GITHUB_REF_NAME:-$(git rev-parse --abbrev-ref HEAD)}"
    git push origin HEAD:"$branch" || return 1
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install dependencies if needed
ensure_dependency() {
    local cmd="$1"
    local install_cmd="$2"
    
    if ! command_exists "$cmd"; then
        log_info "Installing $cmd..."
        eval "$install_cmd" || {
            log_error "Failed to install $cmd"
            return 1
        }
    fi
}

