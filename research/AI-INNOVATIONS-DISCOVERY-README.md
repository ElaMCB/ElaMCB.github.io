# AI Innovations Discovery for QA Testing

Automatically discovers new AI innovations applicable to QA testing every week to keep track of cutting-edge tools, frameworks, and methodologies.

## How It Works

### Automated Weekly Scans

The system runs **every Monday at 10 AM UTC** via GitHub Actions (after the IDE discovery at 9 AM):

1. **Searches Multiple Sources:**
   - GitHub repositories (sorted by stars and recent updates)
   - Hacker News stories (last 7 days)
   - Filters for testing/QA relevance

2. **Search Keywords:**
   - AI testing innovation
   - LLM testing framework
   - AI quality assurance
   - Automated test generation AI
   - AI test automation
   - ML testing tools
   - AI debugging assistant
   - Test generation AI
   - Intelligent testing
   - AI test coverage
   - Agentic testing
   - MCP testing
   - AI test maintenance
   - Self-healing tests
   - Context-aware testing

3. **Categorizes Innovations:**
   - Test Generation
   - Test Execution
   - Test Maintenance
   - Test Debugging
   - Test Coverage
   - AI Agents
   - MCP Integration
   - LLM Testing
   - General

4. **Filters Out Existing:**
   - Automatically skips already-tracked tools (Playwright, Selenium, etc.)
   - Removes duplicates
   - Ranks by relevance and popularity

5. **Creates Discovery Files:**
   - Generates markdown report with detailed descriptions
   - Saves JSON data for programmatic access
   - Creates GitHub issue for review
   - Tags with `needs-review` label

## Manual Usage

### Run Discovery Locally

```bash
node research/ai-innovations-discover.js
```

This will:
- Search for new AI innovations in QA/testing
- Generate `research/discoveries/innovations-YYYY-MM-DD.md` report
- Save `research/discoveries/innovations-YYYY-MM-DD.json` data
- Save `research/discoveries/innovations-YYYY-MM-DD-simple.json` for easy loading

### Trigger GitHub Action Manually

Go to: **Actions → Weekly AI Innovations Discovery for QA Testing → Run workflow**

## Review Process

When a new discovery issue is created:

1. **Review the Report**
   - Check `research/discoveries/innovations-*.md` for full list
   - Review by category for organized evaluation
   - Prioritize by stars/popularity and relevance

2. **Evaluate QA Applicability**
   - Assess potential integration with existing testing workflows
   - Identify use cases in your testing context
   - Consider ROI and implementation effort

3. **Test Promising Innovations**
   - Create proof-of-concept projects
   - Document learnings and best practices
   - Share insights with the QA community

4. **Update Documentation**
   - Add successful innovations to your testing toolkit
   - Document integration patterns
   - Share findings in blog posts or research papers

5. **Close the Issue**
   - Mark as reviewed when complete
   - Tag with `reviewed` label
   - Archive useful findings

## Viewing Discoveries

### On Your Portfolio

Visit: **https://elamcb.github.io/research/ai-innovations.html**

The page displays:
- Total innovations discovered
- Last scan date
- Filterable by category
- Detailed cards with descriptions and QA applications
- Direct links to source repositories/articles

### Research Index

The discovery system is featured on the main research page with a dedicated card linking to the innovations page.

## File Structure

```
research/
├── ai-innovations-discover.js      # Discovery script
├── ai-innovations.html              # Display page
├── AI-INNOVATIONS-DISCOVERY-README.md
└── discoveries/
    ├── .gitkeep
    ├── innovations-YYYY-MM-DD.md          # Markdown report
    ├── innovations-YYYY-MM-DD.json       # Full JSON data
    └── innovations-YYYY-MM-DD-simple.json # Simplified array format
```

## Customization

### Add More Keywords

Edit `research/ai-innovations-discover.js`:

```javascript
const SEARCH_KEYWORDS = [
    'your-new-keyword',
    // ... existing keywords
];
```

### Add More Categories

Update the `CATEGORIES` object and `qaApplications` mapping:

```javascript
const CATEGORIES = {
    'your-category': ['keyword1', 'keyword2'],
    // ... existing categories
};
```

### Change Schedule

Edit `.github/workflows/ai-innovations-discovery.yml`:

```yaml
schedule:
  - cron: '0 10 * * 1'  # Monday 10 AM UTC
```

## Integration with Other Systems

This discovery system complements:
- **AI IDE Comparison**: Tracks tools for developers
- **Research Papers**: Documents findings and applications
- **Testing Frameworks**: Integrates discovered tools into workflows

## Contributing

Found a great AI innovation for QA testing? Add it to `EXISTING_INNOVATIONS` to avoid duplicates, or submit a PR to improve the discovery algorithm!

## Notes

- GitHub API has rate limits (60 requests/hour unauthenticated)
- The script includes 2-second delays between searches
- Hacker News search filters for posts with 5+ points
- All discoveries are automatically saved and version-controlled

