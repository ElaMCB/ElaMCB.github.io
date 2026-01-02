#!/bin/bash

# Script to create a GitHub Release for research tools
# Usage: ./scripts/create-research-release.sh [tool-name] [version] [description]

set -e

TOOL_NAME="${1:-AutoTriage: Manual Test Assessment Tool}"
VERSION="${2:-v1.0.0}"
DESCRIPTION="${3:-Professional framework for assessing manual regression tests and calculating business value.}"

# Convert tool name to tag format (lowercase, replace spaces with hyphens)
TAG_NAME=$(echo "$TOOL_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
TAG_NAME="${TAG_NAME}-${VERSION}"

REPO="ElaMCB/ElaMCB.github.io"
RELEASE_TITLE="${TOOL_NAME} - ${VERSION}"

# Release notes template
RELEASE_NOTES=$(cat <<EOF
## ${TOOL_NAME}

${DESCRIPTION}

### Features
- Technical feasibility analysis
- Business value calculation
- ROI analysis and prioritization
- 4-tier automation priority system

### Files Included
- \`research/notebooks/autotriage-manual-test-assessment.html\` - Interactive tool
- \`research/notebooks/autotriage-manual-test-assessment.ipynb\` - Jupyter notebook source

### View Research
- [View on Research Page](https://elamcb.github.io/research/)
- [View Source Code](https://github.com/ElaMCB/ElaMCB.github.io/tree/main/research/notebooks)

### Publication Date
Published: September 2025
EOF
)

echo "Creating release: ${RELEASE_TITLE}"
echo "Tag: ${TAG_NAME}"
echo ""

# Check if GITHUB_TOKEN is set
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN environment variable is not set"
    echo "Please set it with: export GITHUB_TOKEN=your_token_here"
    echo "Or create a Personal Access Token at: https://github.com/settings/tokens"
    exit 1
fi

# Create the release
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/${REPO}/releases" \
  -d "{
    \"tag_name\": \"${TAG_NAME}\",
    \"name\": \"${RELEASE_TITLE}\",
    \"body\": $(echo "$RELEASE_NOTES" | jq -Rs .),
    \"draft\": false,
    \"prerelease\": false
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 201 ]; then
    RELEASE_ID=$(echo "$BODY" | jq -r '.id')
    UPLOAD_URL=$(echo "$BODY" | jq -r '.upload_url' | sed 's/{?name,label}//')
    
    echo "✅ Release created successfully!"
    echo "Release ID: ${RELEASE_ID}"
    echo "Release URL: $(echo "$BODY" | jq -r '.html_url')"
    echo ""
    echo "To upload files, use:"
    echo "  curl -X POST \\"
    echo "    -H \"Authorization: token \${GITHUB_TOKEN}\" \\"
    echo "    -H \"Content-Type: application/octet-stream\" \\"
    echo "    --data-binary @research/notebooks/autotriage-manual-test-assessment.html \\"
    echo "    \"${UPLOAD_URL}?name=autotriage-manual-test-assessment.html\""
else
    echo "❌ Failed to create release"
    echo "HTTP Code: ${HTTP_CODE}"
    echo "Response: ${BODY}"
    exit 1
fi

