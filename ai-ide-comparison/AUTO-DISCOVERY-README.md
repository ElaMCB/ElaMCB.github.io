# AI IDE Auto-Discovery System

Automatically discovers new AI-powered IDEs every week to keep the comparison fresh and up-to-date.

## How It Works

### Automated Weekly Scans

The system runs **every Monday at 9 AM UTC** via GitHub Actions:

1. **Searches Multiple Sources:**
   - GitHub repositories (sorted by stars)
   - Hacker News stories
   - Product Hunt (optional with API key)

2. **Search Keywords:**
   - "AI IDE"
   - "AI code editor"
   - "AI coding assistant"
   - "LLM code editor"
   - "copilot alternative"
   - "cursor alternative"
   - "AI pair programming"

3. **Filters Out Existing IDEs:**
   - Automatically skips already-tracked IDEs
   - Removes duplicates
   - Ranks by popularity (stars + upvotes)

4. **Creates a Pull Request:**
   - Generates markdown report with discoveries
   - Saves JSON data for programmatic access
   - Opens PR with review instructions
   - Tags with `needs-review` label

## Manual Usage

### Run Discovery Locally

```bash
cd ai-ide-comparison
node auto-discover.js
```

This will:
- Search for new AI IDEs
- Generate `discoveries-YYYY-MM-DD.md` report
- Save `discoveries-YYYY-MM-DD.json` data

### Trigger GitHub Action Manually

Go to: **Actions → Weekly AI IDE Discovery → Run workflow**

## Review Process

When a new discovery PR is created:

1. **Review the Report**
   - Check `discoveries-*.md` for full list
   - Prioritize by stars/popularity
   - Look for genuinely new tools (not forks)

2. **Test Promising Candidates**
   - Spend 2-4 hours with each viable IDE
   - Test core features:
     - Autocomplete quality
     - Chat/composer functionality
     - Multi-file editing
     - Codebase understanding
     - Pricing model

3. **Update Comparison Page**
   If an IDE is worth adding:
   
   ```html
   <!-- Add to index.html -->
   <div class="ide-card" data-tier="?" data-pricing="?" data-local="?">
       <div class="tier-badge tier-?">?-TIER</div>
       <div class="ide-icon"><i class="fas fa-?"></i></div>
       <div class="ide-name">IDE Name</div>
       ...
   </div>
   ```

4. **Assign Tier**
   - **S-Tier:** Best-in-class (Cursor, Windsurf level)
   - **A-Tier:** Excellent but with trade-offs
   - **B-Tier:** Good for specific use cases

5. **Update Stats**
   - Increment IDE count in header stats
   - Update comparison table
   - Add to README if significant

## Configuration

### Adjust Search Frequency

Edit `.github/workflows/ide-discovery.yml`:

```yaml
schedule:
  - cron: '0 9 * * 1'  # Monday 9 AM UTC
  # Change to daily: '0 9 * * *'
  # Change to monthly: '0 9 1 * *'
```

### Add More Data Sources

Edit `auto-discover.js` to add sources:

```javascript
const SOURCES = {
    // Add new API endpoints
    reddit: {
        url: 'https://www.reddit.com/r/programming/search.json',
        // ...
    }
};
```

### Exclude Keywords

Prevent false positives:

```javascript
const EXCLUDE_KEYWORDS = [
    'vim plugin',
    'emacs extension',
    'toy project',
    'archived'
];
```

## Benefits

1. **Never Miss New Tools:** Automated monitoring of multiple sources
2. **Stay Current:** Weekly updates ensure freshness
3. **Systematic Review:** Structured process for evaluation
4. **Historical Tracking:** All discoveries saved with timestamps
5. **Community Input:** PRs allow for collaborative review

## Example Output

```markdown
# New AI IDE Discoveries - 2024-12-20

Found 3 potential new AI IDEs:

## 1. SuperCoder AI

- **Description**: Next-gen AI IDE with quantum autocomplete
- **URL**: https://github.com/example/supercoder
- **Source**: GitHub
- **GitHub Stars**: 12,500
- **Language**: TypeScript

## 2. CodeMind

- **Description**: Mind-reading AI pair programmer
- **URL**: https://codemind.ai
- **Source**: Hacker News
- **HN Points**: 847

---

**Next Steps:**
1. Review each IDE manually
2. Test the IDE for 2-4 hours
3. Assign tier (S/A/B)
4. Update comparison page
5. Commit changes
```

## Maintenance

### Weekly Review Time

Budget **30-60 minutes** weekly:
- 10 min: Review discovery report
- 20-40 min: Quick test of 1-2 promising IDEs
- 10 min: Update comparison if warranted

### When to Add an IDE

✅ **Add if:**
- Unique value proposition
- Active development (commits in last 3 months)
- 500+ GitHub stars OR significant community buzz
- Actually usable (not just a demo)
- Different enough from existing options

❌ **Skip if:**
- Fork of existing IDE
- Abandoned project
- Just a wrapper around existing tools
- Pre-alpha/concept only
- Duplicate functionality

## Troubleshooting

### No Discoveries Found

This is normal if:
- AI IDE space is quiet that week
- All new tools were already tracked
- Search APIs are rate-limited

### False Positives

If getting irrelevant results:
1. Refine `SEARCH_KEYWORDS`
2. Add to `EXCLUDE_KEYWORDS`
3. Improve filtering logic in script

### API Rate Limits

GitHub API: 60 requests/hour unauthenticated
- Add `GITHUB_TOKEN` to secrets for 5,000/hour

## Future Enhancements

- [ ] Add Product Hunt API integration
- [ ] Monitor Reddit r/programming, r/coding
- [ ] Track Twitter/X mentions
- [ ] Auto-generate draft IDE cards
- [ ] ML-based relevance scoring
- [ ] Integration test automation

---

**Last Updated:** December 2024  
**Maintained by:** Elena Mereanu  
**Issues:** [Report here](https://github.com/ElaMCB/ElaMCB.github.io/issues)

