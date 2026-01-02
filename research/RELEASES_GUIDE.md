# Research Tool Releases via GitHub Releases

This guide explains how to publish research tools and notebooks via GitHub Releases instead of RSS feeds.

## Why GitHub Releases?

- ✅ **Native to GitHub** - No external services needed
- ✅ **Version Control** - Track versions and changelogs
- ✅ **Downloadable Assets** - Attach notebooks, tools, and files
- ✅ **Developer-Friendly** - Standard workflow developers expect
- ✅ **Automated** - Can be triggered via GitHub Actions

## How to Create a Release

### Option 1: Manual Release (Recommended for now)

1. Go to your repository: https://github.com/ElaMCB/ElaMCB.github.io
2. Click **Releases** → **Create a new release**
3. Fill in:
   - **Tag version**: e.g., `autotriage-v1.0.0` or `2025.01`
   - **Release title**: e.g., "AutoTriage: Manual Test Assessment Tool"
   - **Description**: Brief description of the research tool
4. **Attach files**: Drag and drop your `.ipynb`, `.html`, or other files
5. Click **Publish release**

### Option 2: Automated Release (via GitHub Actions)

1. Go to **Actions** → **Research Tool Releases**
2. Click **Run workflow**
3. Fill in the form:
   - **Research name**: e.g., "AutoTriage Manual Test Assessment Tool"
   - **Version**: e.g., `v1.0.0` or `2025.01`
   - **Description**: Release description
   - **Files**: Comma-separated paths like `research/notebooks/tool.html,research/notebooks/tool.ipynb`
4. Click **Run workflow**

## What Gets Displayed

The research page automatically fetches and displays:
- Recent releases (filtered for research-related)
- Release tags and versions
- Publication dates
- Download counts
- Links to full release pages

## Best Practices

1. **Naming**: Use descriptive release titles that match your research
2. **Versioning**: Use semantic versioning (v1.0.0) or date-based (2025.01)
3. **Files**: Include both HTML and notebook (.ipynb) versions when available
4. **Descriptions**: Add brief descriptions of what's included
5. **Tags**: Use tags like `research`, `tool`, `notebook` in release names for filtering

## Example Release

**Tag**: `autotriage-v1.0.0`  
**Title**: AutoTriage: Manual Test Assessment Tool - v1.0.0  
**Description**: Professional framework for assessing manual regression tests and calculating business value.  
**Files**: 
- `research/notebooks/autotriage-manual-test-assessment.html`
- `research/notebooks/autotriage-manual-test-assessment.ipynb`

## Viewing Releases

- **On Research Page**: See recent releases in the "Research Tool Releases" section
- **GitHub**: https://github.com/ElaMCB/ElaMCB.github.io/releases
- **API**: https://api.github.com/repos/ElaMCB/ElaMCB.github.io/releases

