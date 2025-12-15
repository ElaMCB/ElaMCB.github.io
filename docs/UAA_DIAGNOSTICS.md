# UAA Diagnostics - How to Query UAA Status

## For AI Assistants / Automated Systems

When UAA fails or you need to check its status, use these methods:

### Method 1: Read Status Files Directly

**Status File:** `docs/uaa-status.json`
- Contains current status of all capabilities
- Updated after each UAA run
- Includes run counts, last success/failure times

**Diagnostic File:** `docs/uaa-diagnostics.json`
- Created only when UAA encounters errors
- Contains detailed error information
- Includes system info, environment variables, capability-specific checks

### Method 2: Use Diagnostic Script

```bash
bash agents/shared/get_diagnostics.sh
```

This script will:
- Display current status from `docs/uaa-status.json`
- Show latest diagnostics if errors occurred
- List recent workflow runs (if `gh` CLI available)

### Method 3: Query GitHub API

```bash
# Get latest workflow run
gh run list --workflow="unified-autonomous-agent.yml" --limit 1

# Get workflow run details
gh run view <run-id> --log

# Get workflow run conclusion
gh run view <run-id> --json conclusion,status
```

### Method 4: Check README Dashboard

The README.md file contains a live dashboard that shows:
- Current status of each capability
- Last run times
- Recent activity
- Links to detailed logs

## Diagnostic Information Structure

### Status File (`docs/uaa-status.json`)
```json
{
  "last_updated": "2025-12-14T12:00:00Z",
  "workflow_status": "success",
  "capabilities": {
    "ci-fix": {
      "status": "success",
      "last_run": "2025-12-14T12:00:00Z",
      "last_success": "2025-12-14T12:00:00Z",
      "last_failure": "N/A",
      "total_runs": 5,
      "success_count": 5,
      "failure_count": 0
    }
  },
  "recent_activity": [
    {
      "time": "2025-12-14T12:00:00Z",
      "capability": "ci-fix",
      "status": "success",
      "message": "CI-Fix completed successfully"
    }
  ]
}
```

### Diagnostic File (`docs/uaa-diagnostics.json`)
```json
{
  "timestamp": "2025-12-14T12:00:00Z",
  "capability": "ci-fix",
  "status": "failure",
  "error_message": "Script execution failed",
  "system_info": {
    "os": "Linux",
    "arch": "x86_64",
    "shell": "/bin/bash",
    "node_version": "v20.0.0",
    "git_version": "git version 2.40.0"
  },
  "environment": {
    "github_repo": "ElaMCB/ElaMCB.github.io",
    "github_ref": "refs/heads/main",
    "github_sha": "abc123...",
    "workflow": "Unified Autonomous Agent"
  },
  "capability_specific": {
    "script_exists": "true",
    "script_executable": "true",
    "shared_utils_exist": "true",
    "config_exists": "true"
  },
  "recent_logs": "Error: ..."
}
```

## Common Issues and Solutions

### Issue: Status shows "unknown"
**Solution:** UAA hasn't run yet. Trigger it manually or wait for scheduled run.

### Issue: Capability shows "failure"
**Solution:** 
1. Check `docs/uaa-diagnostics.json` for error details
2. Review workflow logs in GitHub Actions
3. Verify script permissions: `chmod +x agents/**/*.sh`
4. Check environment variables are set correctly

### Issue: Dashboard not updating
**Solution:**
1. Verify workflow has write permissions
2. Check if README update step completed
3. Review workflow logs for Python script errors
4. Ensure `jq` is installed in workflow

## For AI Assistants: Quick Query Template

When user asks "did UAA run successfully?" or "what's wrong with UAA?":

1. **Read status file:**
   ```bash
   cat docs/uaa-status.json | jq '.'
   ```

2. **Check for diagnostics:**
   ```bash
   if [ -f docs/uaa-diagnostics.json ]; then
     cat docs/uaa-diagnostics.json | jq '.'
   else
     echo "No errors - UAA running successfully"
   fi
   ```

3. **Check latest workflow run:**
   ```bash
   gh run list --workflow="unified-autonomous-agent.yml" --limit 1 --json conclusion,status,url
   ```

4. **Report findings:**
   - If status shows "success" → UAA is working
   - If status shows "failure" → Read diagnostics and report error
   - If status shows "unknown" → UAA hasn't run yet

## Integration with AI Assistants

AI assistants can:
- Read `docs/uaa-status.json` to check current status
- Read `docs/uaa-diagnostics.json` when errors occur
- Use `agents/shared/get_diagnostics.sh` for formatted output
- Query GitHub API for workflow run details
- Parse README dashboard for quick status overview

