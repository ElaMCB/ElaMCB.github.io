# Autonomous CI Fix Agent Guide

## Overview

An autonomous agent that monitors your GitHub repository, detects CI/CD failures, analyzes errors, and automatically fixes common issues without human intervention.

## What It Does

- **Monitors**: Watches GitHub Actions workflows for failures
- **Analyzes**: Uses pattern matching and AI to understand errors
- **Fixes**: Automatically applies fixes for common issues
- **Reports**: Creates summaries and issues for complex problems

## Supported Auto-Fixes

### 1. NPM Lock File Sync Issues
**Error**: `npm ci can only install packages when your package.json and package-lock.json are in sync`

**Auto-Fix**: Runs `npm install` to update lock file and commits the change

### 2. Missing Dependencies
**Error**: `Missing: [package] from lock file`

**Auto-Fix**: Installs missing dependencies and updates lock file

### 3. Other Errors
**Error**: Unknown or complex errors

**Action**: Creates a GitHub issue with error details for manual review

## Setup Instructions

### Step 1: Enable the Workflow

The workflow file is already created at `.github/workflows/autonomous-ci-fix-agent.yml`

### Step 2: Configure Permissions

The workflow needs these permissions (already configured):
- `contents: write` - To commit fixes
- `pull-requests: write` - To create PRs (if needed)
- `issues: write` - To create issues for complex errors

### Step 3: Test the Agent

1. **Manual Trigger**: Go to Actions → Autonomous CI Fix Agent → Run workflow
2. **Automatic**: It will trigger automatically when CI workflows fail

## How It Works

### Workflow Triggers

```yaml
on:
  workflow_run:
    workflows: ["CI", "Tests", "Build"]
    types:
      - completed
```

The agent runs when:
- Any workflow named "CI", "Tests", or "Build" completes
- Only if the workflow failed
- Can also be manually triggered

### Error Analysis

The agent uses pattern matching to identify common errors:

```bash
# NPM lock file sync
if grep -q "npm ci.*can only install packages"; then
  fix_action="run_npm_install"
fi

# Missing dependencies
if grep -q "Missing:.*from lock file"; then
  fix_action="run_npm_install"
fi
```

### Auto-Fix Process

1. **Detect Error**: Analyze workflow logs
2. **Identify Type**: Match error patterns
3. **Apply Fix**: Run appropriate fix command
4. **Commit**: Automatically commit the fix
5. **Report**: Create summary or issue

## Enhancing with AI

### Option 1: Use OpenAI API (More Intelligent)

Add this step to analyze errors with GPT:

```yaml
- name: Analyze error with OpenAI
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  run: |
    ERROR_LOG=$(cat workflow_logs.txt)
    
    RESPONSE=$(curl -s https://api.openai.com/v1/chat/completions \
      -H "Authorization: Bearer $OPENAI_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "gpt-4",
        "messages": [{
          "role": "system",
          "content": "You are a CI/CD error analyzer. Analyze the error and suggest a fix."
        }, {
          "role": "user",
          "content": "Error: '"$ERROR_LOG"'"
        }]
      }')
    
    echo "analysis=$RESPONSE" >> $GITHUB_OUTPUT
```

### Option 2: Use Ollama (Free, Local)

If you have a self-hosted runner with Ollama:

```yaml
- name: Analyze with Ollama
  run: |
    ERROR_LOG=$(cat workflow_logs.txt)
    
    ANALYSIS=$(ollama run llama3.2:3b "Analyze this CI error and suggest a fix: $ERROR_LOG")
    
    echo "analysis=$ANALYSIS" >> $GITHUB_OUTPUT
```

### Option 3: Use GitHub Copilot API

```yaml
- name: Analyze with GitHub Copilot
  uses: actions/github-script@v7
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    script: |
      const errorLog = fs.readFileSync('workflow_logs.txt', 'utf8');
      // Use GitHub API to analyze
```

## Customization

### Add More Error Patterns

Edit the workflow to add more patterns:

```yaml
- name: Analyze error with AI
  run: |
    # Add your custom patterns
    if echo "$ERROR_LOG" | grep -q "Your custom error pattern"; then
      echo "error_type=custom_error" >> $GITHUB_OUTPUT
      echo "fix_action=custom_fix" >> $GITHUB_OUTPUT
    fi
```

### Add More Auto-Fixes

Add new fix steps:

```yaml
- name: Auto-fix custom error
  if: steps.analyze.outputs.error_type == 'custom_error'
  run: |
    # Your fix commands here
    npm run fix-custom-issue
    git add .
    git commit -m "🤖 Auto-fix: Custom error"
    git push
```

### Monitor Different Workflows

Change which workflows trigger the agent:

```yaml
on:
  workflow_run:
    workflows: ["Your-Workflow-Name", "Another-Workflow"]
    types:
      - completed
```

## Example: Complete AI-Powered Version

Here's a more advanced version using OpenAI:

```yaml
name: AI-Powered CI Fix Agent

on:
  workflow_run:
    workflows: ["CI"]
    types:
      - completed

jobs:
  ai-fix:
    if: github.event.workflow_run.conclusion == 'failure'
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Get error logs
        id: logs
        run: |
          gh run view ${{ github.event.workflow_run.id }} --log > error.log
          echo "error=$(cat error.log | base64 -w 0)" >> $GITHUB_OUTPUT
      
      - name: AI Analysis
        id: ai
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          ERROR=$(echo "${{ steps.logs.outputs.error }}" | base64 -d)
          
          ANALYSIS=$(curl -s https://api.openai.com/v1/chat/completions \
            -H "Authorization: Bearer $OPENAI_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "model": "gpt-4",
              "messages": [{
                "role": "system",
                "content": "Analyze CI errors and return JSON: {\"error_type\": \"...\", \"fix_commands\": [\"...\"], \"confidence\": 0.9}"
              }, {
                "role": "user",
                "content": "'"$ERROR"'"
              }]
            }' | jq -r '.choices[0].message.content')
          
          echo "analysis=$ANALYSIS" >> $GITHUB_OUTPUT
      
      - name: Apply AI-suggested fix
        if: steps.ai.outputs.analysis != ''
        run: |
          ANALYSIS='${{ steps.ai.outputs.analysis }}'
          FIX_COMMANDS=$(echo "$ANALYSIS" | jq -r '.fix_commands[]')
          
          for cmd in $FIX_COMMANDS; do
            eval "$cmd"
          done
          
          git add .
          git commit -m "🤖 AI Auto-fix: ${{ steps.ai.outputs.analysis | jq -r '.error_type' }}"
          git push
```

## Monitoring & Alerts

### Get Notifications

Add Slack/Discord notifications:

```yaml
- name: Notify on fix
  if: steps.analyze.outputs.error_type != 'no_logs'
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "🤖 Auto-fixed CI error: ${{ steps.analyze.outputs.error_type }}"
      }
```

## Best Practices

1. **Start Simple**: Begin with pattern matching, add AI later
2. **Test Thoroughly**: Test on non-critical branches first
3. **Monitor Results**: Review auto-fixes to improve patterns
4. **Set Boundaries**: Only auto-fix safe, common errors
5. **Document**: Keep track of what the agent fixes

## Troubleshooting

### Agent Not Triggering

- Check workflow names match exactly
- Verify permissions are set correctly
- Check if workflow_run event is supported

### Fixes Not Working

- Review error logs in Actions
- Check if fix commands are correct
- Verify git permissions

### Too Many Auto-Fixes

- Add confidence thresholds
- Require manual approval for certain fixes
- Limit to specific error types

## Cost Considerations

### Free Option (Current)
- Uses GitHub Actions (free for public repos)
- Pattern matching (no API costs)
- Basic error detection

### AI-Powered Option
- OpenAI API: ~$0.01-0.10 per analysis
- Ollama: Free (requires self-hosted runner)
- GitHub Copilot: Included with GitHub subscription

## Next Steps

1. **Enable the workflow** in your repository
2. **Test it** by triggering a known failure
3. **Monitor** the first few auto-fixes
4. **Enhance** with AI if needed
5. **Expand** to more error types

## Related Resources

- [QA Agentic Workflows Guide](./QA_AGENTIC_WORKFLOWS_GUIDE.md) - Build your own agents
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

*This agent autonomously fixes CI failures, saving you time and keeping your builds green.*

