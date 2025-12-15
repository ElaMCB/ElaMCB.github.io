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

# GitHub API helpers
create_github_issue() {
    local title="$1"
    local body="$2"
    local labels="$3"
    
    if [ -z "$labels" ]; then
        gh issue create --title "$title" --body "$body" || return 1
    else
        gh issue create --title "$title" --body "$body" --label "$labels" || return 1
    fi
}

create_github_pr() {
    local title="$1"
    local body="$2"
    local branch="$3"
    local labels="$4"
    
    if [ -z "$labels" ]; then
        gh pr create --title "$title" --body "$body" --head "$branch" || return 1
    else
        gh pr create --title "$title" --body "$body" --head "$branch" --label "$labels" || return 1
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

