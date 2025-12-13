# SA - Security Agent Guide

## Overview

**SA (Security Agent)** is an autonomous agent that continuously monitors your portfolio for security vulnerabilities, exposed secrets, and security best practices.

## What It Does

- **Scans Dependencies**: Checks npm packages for known vulnerabilities
- **Detects Secrets**: Scans codebase for exposed API keys, tokens, credentials
- **Monitors Security**: Tracks security posture over time
- **Auto-Fixes**: Automatically fixes non-breaking security issues
- **Alerts**: Creates critical issues for urgent security problems

## Features

### Dependency Vulnerability Scanning
- Runs `npm audit` weekly
- Categorizes by severity (Critical, High, Moderate, Low)
- Tracks vulnerability trends
- Suggests fixes

### Secret Detection
Scans for common secret patterns:
- AWS Access Keys
- GitHub Personal Tokens
- Stripe API Keys
- Slack Tokens
- Google API Keys
- And more...

### Auto-Fix Capabilities
- Automatically fixes moderate/low severity vulnerabilities
- Updates package-lock.json
- Creates PRs for review
- Only fixes non-breaking changes

### Security Reporting
- Weekly security reports
- Vulnerability details
- Fix recommendations
- Security trend analysis

## Configuration

### Schedule
Edit `.github/workflows/security-agent.yml`:

```yaml
schedule:
  - cron: '0 10 * * 1'  # Every Monday at 10 AM UTC
```

### Secret Patterns
Add custom secret patterns:

```yaml
SECRET_PATTERNS=(
  "YOUR_CUSTOM_PATTERN"
)
```

### Auto-Fix Behavior
Control what gets auto-fixed:

```yaml
# Only auto-fix if no critical/high issues
if: steps.npm-audit.outputs.critical == '0' && steps.npm-audit.outputs.high == '0'
```

## Manual Trigger

You can manually trigger the agent:

1. Go to **Actions** tab
2. Select **SA - Security Agent**
3. Click **Run workflow**

## Output

### Security Report
Created at `docs/security-report.md`:

```markdown
# Security Report - 2025-01-13

## Summary
- Total Vulnerabilities: 5
- Critical: 0
- High: 2
- Moderate: 3
- Exposed Secrets: 0

## Vulnerabilities
[detailed list of vulnerabilities]
```

### GitHub Issue (Critical)
For critical security issues:
- Urgency indicator
- Vulnerability details
- Immediate action steps
- Security label

### Pull Request (Fixes)
For auto-fixable issues:
- Security fixes applied
- Updated package-lock.json
- Review required

## Security Best Practices

### Dependency Management
- Keep dependencies updated
- Review security advisories
- Use `npm audit` regularly
- Consider automated dependency updates

### Secret Management
- Never commit secrets to git
- Use environment variables
- Use GitHub Secrets for CI/CD
- Rotate credentials regularly
- Use secret scanning tools

### Security Headers
- Configure security headers
- Use HTTPS
- Implement CSP (Content Security Policy)
- Set secure cookies

## Troubleshooting

### False Positives (Secrets)
- Some patterns may match non-secrets
- Review matches manually
- Add to exclusion list if needed
- Use more specific patterns

### Auto-Fix Failures
- Some fixes may break functionality
- Review PRs before merging
- Test after applying fixes
- Rollback if needed

### Too Many Vulnerabilities
- Prioritize critical/high
- Fix in batches
- Update dependencies regularly
- Consider alternative packages

## Integration

### With Other Agents
- **CIF-AA**: Can trigger on security-related CI failures
- **DUA**: Works together for dependency updates
- **LHA**: Can check if vulnerabilities affect links

### With GitHub Security
- Uses GitHub Security features
- Integrates with Dependabot
- Uses GitHub Security Advisories

## Customization

### Add Security Checks
Edit the workflow to add:
- OWASP Top 10 checks
- Security header validation
- SSL/TLS configuration checks
- Content Security Policy validation

### Custom Secret Patterns
Add patterns for your stack:
- Database connection strings
- API keys specific to your services
- Custom authentication tokens

## Metrics

Track these metrics:
- **Vulnerability Count**: Total vulnerabilities
- **Critical Issues**: Number of critical vulnerabilities
- **Fix Rate**: How quickly vulnerabilities are fixed
- **Secret Detection**: Number of secrets found (should be 0)

## Alert Levels

### Critical
- Exposed secrets detected
- Critical dependency vulnerabilities
- Immediate action required

### High
- High severity vulnerabilities
- Security configuration issues
- Fix within 24-48 hours

### Moderate
- Moderate severity issues
- Best practice violations
- Fix within 1 week

## Related Resources

- **[Portfolio Agents Roadmap](./PORTFOLIO_AGENTS_ROADMAP.md)** - See all planned agents
- **[Autonomous CI Agent Guide](./AUTONOMOUS_CI_AGENT_GUIDE.html)** - Reference implementation
- **[QA Agentic Workflows Guide](./QA_AGENTIC_WORKFLOWS_GUIDE.html)** - Build your own agents
- **[npm audit documentation](https://docs.npmjs.com/cli/v8/commands/npm-audit)**
- **[GitHub Security Best Practices](https://docs.github.com/en/code-security)**

---

*Last Updated: 2025*  
*SA keeps your portfolio secure and your secrets safe.*

