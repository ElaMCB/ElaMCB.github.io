# UAA Success Indicators - How to Know When UAA Runs Successfully

## Quick Check Methods

### 1. GitHub Actions Tab
**Location:** https://github.com/ElaMCB/ElaMCB.github.io/actions

**What to Look For:**
- ✅ Green checkmark = UAA ran successfully
- ❌ Red X = UAA encountered an error
- 🟡 Yellow circle = UAA is currently running
- ⚪ Gray circle = UAA was skipped (no trigger conditions met)

**Workflow Name:** "Unified Autonomous Agent"

### 2. Execution Summary
At the end of each UAA run, you'll see:
```
=========================================
UAA (Unified Autonomous Agent) - Execution Summary
=========================================
Capability: [ci-fix|link-health|security|all]
Workflow Event: [workflow_run|schedule|push|workflow_dispatch]
Status: [success|failure]
=========================================
```

### 3. Capability-Specific Indicators

#### CI-Fix Capability Success:
- ✅ **Auto-fix applied**: New commit appears with message "Auto-fix: Update package-lock.json..."
- ✅ **Issue created**: GitHub issue created for complex errors (check Issues tab)
- ✅ **Logs show**: "CI-Fix capability completed" in workflow logs

#### Link-Health Capability Success:
- ✅ **Report created**: `docs/link-health-report.md` file created/updated
- ✅ **PR created**: Pull request created with title "Fix broken links (X found)"
- ✅ **Issue created**: Critical issue created if internal broken links found
- ✅ **Logs show**: "Link-Health capability completed" in workflow logs

#### Security Capability Success:
- ✅ **Report created**: `docs/security-report.md` file created/updated
- ✅ **Auto-fix applied**: New commit with "Auto-fix npm vulnerabilities" message
- ✅ **Issue created**: Critical security issue if vulnerabilities found
- ✅ **Logs show**: "Security capability completed" in workflow logs

### 4. Email Notifications (if enabled)
GitHub will send email notifications when:
- Workflow fails
- Workflow is cancelled
- Workflow completes (if you have notifications enabled)

### 5. GitHub Notifications
Check the bell icon (🔔) in GitHub for:
- Workflow run completions
- Issues created by UAA
- Pull requests created by UAA

## Expected Run Schedule

### Automatic Triggers:
- **CI-Fix**: Runs when any monitored workflow fails (CI, Tests, Build, LHA, SA)
- **Link-Health**: 
  - Every Monday at 9 AM UTC (scheduled)
  - When HTML/MD files are pushed
- **Security**:
  - Every Monday at 10 AM UTC (scheduled)
  - When package.json/JS/PY files are pushed

### Manual Triggers:
- Go to Actions → "Unified Autonomous Agent" → "Run workflow"
- Select capability: all, ci-fix, link-health, or security

## Troubleshooting

### If UAA Doesn't Run:
1. Check if trigger conditions are met
2. Verify workflow file exists: `.github/workflows/unified-autonomous-agent.yml`
3. Check workflow permissions in repository settings

### If UAA Fails:
1. Check workflow logs in Actions tab
2. Look for error messages in the "Run Unified Agent (UAA)" step
3. Verify scripts are executable: `chmod +x agents/**/*.sh`
4. Check GitHub token permissions

### If No Output Files Created:
- UAA may have run but found no issues (this is success!)
- Check workflow logs to confirm execution
- Look for "capability completed" messages

## Verification Checklist

After UAA runs, verify:
- [ ] Workflow shows green checkmark in Actions tab
- [ ] Execution summary shows correct capability and status
- [ ] No error messages in workflow logs
- [ ] Expected output files created (if issues found)
- [ ] Issues/PRs created (if applicable)
- [ ] Commits pushed (if auto-fixes applied)

## Example Success Log Output

```
[INFO] =========================================
[INFO] UAA (Unified Autonomous Agent) v1.0.0
[INFO] =========================================
[INFO] Capability requested: link-health
[INFO] Workflow event: push
[INFO] Executing Link-Health capability...
[INFO] Scanning for broken links...
[INFO] Scan complete: 0 broken links out of 150 total
[INFO] No broken links found
[SUCCESS] Link-Health capability completed
[SUCCESS] Unified Agent execution completed
```

