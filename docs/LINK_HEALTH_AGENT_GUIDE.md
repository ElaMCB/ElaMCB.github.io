# LHA - Link Health Agent Guide

## Overview

**LHA (Link Health Agent)** is an autonomous agent that monitors your portfolio for broken links, ensuring all internal and external links remain functional.

## What It Does

- **Scans**: Weekly automated scans of all HTML and Markdown files
- **Detects**: Broken links (404s, timeouts, redirects)
- **Categorizes**: Internal vs external broken links
- **Fixes**: Creates PRs with fix reports
- **Alerts**: Creates issues for critical internal broken links

## Features

### Automated Scanning
- Runs every Monday at 9 AM UTC
- Also triggers on HTML/Markdown file changes
- Scans recursively through all files
- Skips social media and email links (known to be valid)

### Link Detection
- Detects HTTP status codes (400+)
- Identifies broken internal links
- Identifies broken external links
- Reports link location (which file contains the broken link)

### Auto-Fix Workflow
1. Scans all links
2. Identifies broken links
3. Creates detailed report
4. Creates PR with report (for review)
5. Creates issue for critical internal broken links

## Configuration

### Schedule
Edit `.github/workflows/link-health-agent.yml`:

```yaml
schedule:
  - cron: '0 9 * * 1'  # Every Monday at 9 AM UTC
```

### Skipped Links
The agent skips these by default:
- GitHub links
- LinkedIn links
- Twitter links
- Email links (mailto:)

To add more skipped patterns, edit the workflow:

```yaml
--skip "https://example.com"
```

## Manual Trigger

You can manually trigger the agent:

1. Go to **Actions** tab
2. Select **LHA - Link Health Agent**
3. Click **Run workflow**

## Output

### Link Health Report
Created at `docs/link-health-report.md`:

```markdown
# Link Health Report - 2025-01-13

## Summary
- Total Links Scanned: 245
- Broken Links Found: 3
- Internal Broken: 1
- External Broken: 2

## Broken Links
[list of broken links with status codes]
```

### Pull Request
When broken links are found, a PR is created with:
- Summary of broken links
- Detailed list of all broken links
- Location of each broken link

### GitHub Issue
For critical internal broken links, an issue is created with:
- Urgency indicator
- List of broken internal links
- Priority flag

## Troubleshooting

### Agent Not Running
- Check workflow is enabled in Actions
- Verify schedule syntax is correct
- Check repository permissions

### False Positives
- Some sites block automated scanners
- Add to skip list if consistently false
- Review manually if unsure

### Too Many Broken Links
- Review the report
- Fix links in batches
- Update skip list for known issues

## Best Practices

1. **Review Weekly**: Check Monday reports
2. **Fix Promptly**: Address internal broken links immediately
3. **Monitor External**: External links may be temporary
4. **Update Skip List**: Add known-good external sites

## Integration

### With Other Agents
- **SA (Security Agent)**: Can check if broken links are security risks
- **CUA (Content Update Agent)**: Can update links when content changes

### With CI/CD
- Can block deployments if critical links are broken
- Can be part of pre-commit hooks

## Customization

### Add Custom Checks
Edit the workflow to add:
- Link response time checks
- Redirect chain detection
- Anchor link validation
- Image link validation

### Change Report Format
Modify the report generation step to customize:
- Report location
- Report format (JSON, HTML, etc.)
- Report content

## Metrics

Track these metrics:
- **Total Links**: Number of links scanned
- **Broken Links**: Number of broken links found
- **Fix Rate**: How quickly links are fixed
- **False Positive Rate**: Accuracy of detection

## Related Resources

- **[Portfolio Agents Roadmap](./PORTFOLIO_AGENTS_ROADMAP.md)** - See all planned agents
- **[Autonomous CI Agent Guide](./AUTONOMOUS_CI_AGENT_GUIDE.html)** - Reference implementation
- **[QA Agentic Workflows Guide](./QA_AGENTIC_WORKFLOWS_GUIDE.md)** - Build your own agents

---

*Last Updated: 2025*  
*LHA ensures your portfolio links are always healthy.*

