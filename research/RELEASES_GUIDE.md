# Research Tool Releases via GitHub Releases

This guide explains how to publish research tools and notebooks via GitHub Releases instead of RSS feeds.

## Why GitHub Releases?

- ✅ **Native to GitHub** - No external services needed
- ✅ **Version Control** - Track versions and changelogs
- ✅ **Downloadable Assets** - Attach notebooks, tools, and files
- ✅ **Developer-Friendly** - Standard workflow developers expect
- ✅ **Automated** - Can be triggered via GitHub Actions

## How to Create a Release - Step by Step

### Step-by-Step Guide

1. **Go to Releases Page**
   - Navigate to: https://github.com/ElaMCB/ElaMCB.github.io
   - Click **Releases** (on the right sidebar)
   - Click **Create a new release** (or "Draft a new release")

2. **Choose or Create Tag**
   - **Option A**: Create a new tag (recommended for first release)
     - Type: `autotriage-v1.0.0` or `rag-testing-v1.0.0`
     - Use format: `[tool-name]-v[version]` or `[tool-name]-[YYYY.MM]`
   - **Option B**: Choose existing tag (if updating a release)

3. **Release Title**
   - Format: `[Research Name] - [Version]`
   - Examples:
     - `AutoTriage: Manual Test Assessment Tool - v1.0.0`
     - `RAG in Software Testing - v1.0.0`
     - `CI/CD Test Optimization Tool - 2025.10`

4. **Release Notes / Description**
   ```
   ## [Research Tool Name]
   
   [Brief description of what this research tool does]
   
   ### Features
   - Feature 1
   - Feature 2
   - Feature 3
   
   ### Files Included
   - `research/notebooks/tool-name.html` - Interactive notebook
   - `research/notebooks/tool-name.ipynb` - Jupyter notebook source
   
   ### View Research
   - [View on Research Page](https://elamcb.github.io/research/)
   - [View Source Code](https://github.com/ElaMCB/ElaMCB.github.io/tree/main/research/notebooks)
   
   ### Publication Date
   Published: [Month Year, e.g., "October 2025"]
   ```

5. **Attach Files**
   - Drag and drop files OR click to select
   - Include:
     - `.html` file (interactive version)
     - `.ipynb` file (Jupyter notebook)
     - Any other relevant files (data, configs, etc.)
   - Files should be in `research/notebooks/` directory

6. **Settings**
   - ✅ **Set as the latest release**: Check this (unless it's a pre-release)
   - ⬜ **Set as a pre-release**: Uncheck (unless it's beta/alpha)

7. **Click "Publish release"**

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

## Tag Naming Conventions

### Recommended Formats:

1. **Semantic Versioning** (Recommended):
   - `tool-name-v1.0.0` (first release)
   - `tool-name-v1.1.0` (minor update)
   - `tool-name-v2.0.0` (major update)

2. **Date-Based** (Alternative):
   - `tool-name-2025.10` (October 2025)
   - `tool-name-2025.12` (December 2025)

3. **Examples**:
   - `autotriage-v1.0.0`
   - `rag-testing-v1.0.0`
   - `mcp-testing-v1.0.0`
   - `ci-optimization-v1.0.0`

### Pre-release Tags (for beta/alpha):
- `tool-name-v1.0.0-alpha`
- `tool-name-v1.0.0-beta`

## Best Practices

1. **Naming**: Use descriptive release titles that match your research
2. **Versioning**: Use semantic versioning (v1.0.0) or date-based (2025.01)
3. **Files**: Include both HTML and notebook (.ipynb) versions when available
4. **Descriptions**: Add brief descriptions of what's included
5. **Tags**: Use consistent naming format for easy tracking
6. **Release Notes**: Use markdown formatting for better readability

## Example Release - Complete Form

### Example 1: AutoTriage Tool

**Tag**: `autotriage-v1.0.0`  
**Release Title**: `AutoTriage: Manual Test Assessment Tool - v1.0.0`

**Release Notes**:
```markdown
## AutoTriage: Manual Test Assessment Tool

Professional framework for assessing manual regression tests and calculating business value. Analyzes technical feasibility, business impact, and ROI to generate 4-tier automation priorities.

### Features
- Technical feasibility analysis
- Business value calculation
- ROI analysis and prioritization
- 4-tier automation priority system

### Files Included
- `research/notebooks/autotriage-manual-test-assessment.html` - Interactive tool
- `research/notebooks/autotriage-manual-test-assessment.ipynb` - Jupyter notebook source

### View Research
- [View on Research Page](https://elamcb.github.io/research/)
- [View Source Code](https://github.com/ElaMCB/ElaMCB.github.io/tree/main/research/notebooks)

### Publication Date
Published: September 2025
```

**Files to Attach**:
- `research/notebooks/autotriage-manual-test-assessment.html`
- `research/notebooks/autotriage-manual-test-assessment.ipynb`

**Settings**:
- ✅ Set as the latest release
- ⬜ Set as a pre-release (unchecked)

---

### Example 2: RAG Testing Research

**Tag**: `rag-testing-v1.0.0`  
**Release Title**: `RAG in Software Testing - v1.0.0`

**Release Notes**:
```markdown
## RAG in Software Testing

Exploring applications of Retrieval Augmented Generation in software testing, including test case generation, coverage analysis, and testing strategy recommendations.

### Key Topics
- Test case generation using RAG
- Coverage analysis automation
- Testing strategy recommendations

### Files Included
- `research/notebooks/rag-testing-applications.html` - Research notebook
- `research/notebooks/rag-testing-applications.ipynb` - Source code

### View Research
- [View on Research Page](https://elamcb.github.io/research/)
- [View Source Code](https://github.com/ElaMCB/ElaMCB.github.io/tree/main/research/notebooks)

### Publication Date
Published: December 2025
```

**Files to Attach**:
- `research/notebooks/rag-testing-applications.html`
- `research/notebooks/rag-testing-applications.ipynb`

## Viewing Releases

- **On Research Page**: See recent releases in the "Research Tool Releases" section
- **GitHub**: https://github.com/ElaMCB/ElaMCB.github.io/releases
- **API**: https://api.github.com/repos/ElaMCB/ElaMCB.github.io/releases

