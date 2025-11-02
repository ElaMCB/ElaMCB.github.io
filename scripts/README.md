# Portfolio Scripts

Utility scripts for maintaining and validating the portfolio.

## Link Checker

**File**: `check-links.js`  
**Purpose**: Validates all external links in markdown files before deployment

### Usage

```bash
# Run link checker
node scripts/check-links.js
```

### Features

- **Recursive scanning**: Finds all `.md` files in the repository
- **External link validation**: Checks HTTP/HTTPS URLs for accessibility
- **Smart filtering**: Skips relative links and anchors (they're local)
- **Detailed reporting**: Shows broken links by file with error details
- **Exit codes**: Returns error code 1 if broken links found (useful for CI)

### Example Output

```
🔍 Starting link check...
Found 15 markdown files
Found 47 total links

🌐 Checking URLs...
Checking: https://github.com/ElaMCB/ElaMCB.github.io/issues ✅
Checking: https://github.com/ElaMCB/ElaMCB.github.io/discussions ❌ (404)
Checking: https://linkedin.com/in/elenamereanu ✅

📊 Results Summary:
✅ Working: 45
❌ Broken: 2
⏰ Timeout: 0
⏭️ Skipped: 12

🚨 Issues Found:

📄 README.md:
  ❌ Discussions -> https://github.com/ElaMCB/ElaMCB.github.io/discussions
     Status: error (404)
```

### Integration with Workflow

Add to your development routine:

```bash
# Before committing changes
git add .
node scripts/check-links.js  # Check links first
git commit -m "Your changes"
git push
```

### CI Integration

Add to `.github/workflows/deploy.yml`:

```yaml
- name: Check Links
  run: node scripts/check-links.js
```

This will prevent deployment if broken links are detected.

## Future Scripts

Additional utility scripts can be added here:

- **`validate-html.js`**: HTML validation for the live site
- **`optimize-images.js`**: Image compression and optimization  
- **`generate-sitemap.js`**: Automatic sitemap generation
- **`check-performance.js`**: Lighthouse performance testing

---

**Pro Tip**: Run `node scripts/check-links.js` before every push to catch broken links early!



