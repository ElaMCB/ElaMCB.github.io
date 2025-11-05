# Playwright Testing Framework for Portfolio

## Overview

This is a production-ready Playwright testing framework that validates the [elamcb.github.io](https://elamcb.github.io) portfolio. It demonstrates best practices for testing static sites, with AI-powered testing capabilities through Model Context Protocol (MCP) integration.

## 🎯 What This Tests

This framework validates my portfolio through comprehensive automated tests:

- ✅ **Smoke Tests** - Critical elements and page loads
- ✅ **Navigation Tests** - All internal and project links
- ✅ **Social Media Links** - LinkedIn, GitHub integration
- ✅ **Performance** - Load time monitoring
- ✅ **Cross-Browser** - Chromium, Firefox, WebKit support

## 🚀 Quick Start

### Prerequisites

```bash
node >= 18.0.0
npm >= 9.0.0
```

### Installation

```bash
# Clone the repository
git clone https://github.com/ElaMCB/ElaMCB.github.io.git
cd ElaMCB.github.io

# Install dependencies
npm install

# Install Playwright browsers
npx playwright install --with-deps
```

### Running Tests

```bash
# Run all tests
npx playwright test

# Run specific test file
npx playwright test tests/portfolio.spec.js

# Run tests in headed mode (see browser)
npx playwright test --headed

# Run tests with UI mode (interactive)
npx playwright test --ui

# Generate HTML report
npx playwright test --reporter=html
```

## 📁 Project Structure

```
ElaMCB.github.io/
├── tests/
│   ├── portfolio.spec.js           # Smoke tests for critical elements
│   └── navigation-links.spec.js    # Navigation and link validation
├── playwright.config.js            # Playwright configuration
├── mcp-playwright-server.js        # MCP server for AI-powered testing
├── MCP-SETUP-GUIDE.md             # Guide for MCP integration
└── package.json                    # Dependencies
```

## 🧪 Test Suites

### 1. Portfolio Smoke Test (`portfolio.spec.js`)

Validates critical functionality:

```javascript
import { test, expect } from '@playwright/test';

test('Portfolio smoke test', async ({ page }) => {
  await page.goto('https://elamcb.github.io');
  
  // Verify critical elements
  await expect(page).toHaveTitle(/Ela MCB/);
  await expect(page.getByRole('heading', { name: 'AI Projects' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Research' })).toBeVisible();
});
```

**What it tests:**
- Homepage loads successfully
- Page title is correct
- Critical sections are visible (AI Projects, Research)

### 2. Navigation Links Test (`navigation-links.spec.js`)

Comprehensive link validation:

**Tests include:**
- ✅ All navigation/header links work
- ✅ Project pages load (LLM Guardian, Research, Job Search, AI IDE Comparison)
- ✅ Social media links are valid (LinkedIn, GitHub)
- ✅ Internal links return 200 status codes

```javascript
test('should have working project links', async ({ page }) => {
  const projectPaths = [
    { name: 'LLM Guardian', path: '/llm-guardian/' },
    { name: 'Research Notebooks', path: '/research/' },
    { name: 'Job Search Automation', path: '/job-search-automation/' },
    { name: 'AI IDE Comparison', path: '/ai-ide-comparison/' }
  ];
  
  for (const project of projectPaths) {
    const url = `https://elamcb.github.io${project.path}`;
    const response = await page.goto(url);
    expect(response?.status()).toBe(200);
  }
});
```

## ⚙️ Configuration

### Playwright Config (`playwright.config.js`)

Optimized for speed and reliability:

```javascript
export default defineConfig({
  testDir: './tests',
  timeout: 30000,           // 30 second timeout per test
  workers: 2,               // Parallel execution
  retries: 1,               // Retry failed tests once
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    actionTimeout: 10000,
    navigationTimeout: 5000, // Fast navigation
  },
});
```

**Key Features:**
- **Parallel Execution**: 2 workers for faster test runs
- **Auto-Retry**: Handles flaky network issues
- **Optimized Timeouts**: Balanced between speed and reliability
- **Multiple Browsers**: Chromium, Firefox, WebKit support

## 🤖 AI-Powered Testing with MCP

This framework includes a **Model Context Protocol (MCP)** server that enables AI assistants to run tests, take screenshots, and analyze results.

### MCP Tools Available:

1. **`run_portfolio_smoke_test`** - Execute smoke tests
2. **`screenshot_portfolio`** - Capture page screenshots
3. **`check_broken_links`** - Validate all links
4. **`test_mobile_responsive`** - Mobile device testing
5. **`measure_performance`** - Performance metrics

### Example MCP Usage:

```bash
# Start MCP server
node mcp-playwright-server.js
```

Then in Claude Desktop or compatible AI assistant:
```
"Run my portfolio smoke test"
"Take a screenshot of my homepage"
"Check for broken links"
```

See [MCP-SETUP-GUIDE.md](../MCP-SETUP-GUIDE.md) for complete setup instructions.

## 🔄 CI/CD Integration

### GitHub Actions

Tests run automatically on:
- ✅ Every push to `main` branch
- ✅ Every pull request to `main`

**Workflow:** `.github/workflows/portfolio-tests.yml`

```yaml
name: Portfolio Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node.js
        uses: actions/setup-node@v3
      - name: Install dependencies
        run: npm ci
      - name: Install Playwright
        run: npx playwright install --with-deps
      - name: Run tests
        run: npx playwright test
```

**View Results:** 
- Badge: ![Tests](https://github.com/ElaMCB/ElaMCB.github.io/actions/workflows/portfolio-tests.yml/badge.svg)
- Workflow: https://github.com/ElaMCB/ElaMCB.github.io/actions

## 📊 Test Results & Reporting

### Console Output

```bash
Running 4 tests using 2 workers

  ✓  tests/portfolio.spec.js:3:1 › Portfolio smoke test (2.4s)
  ✓  tests/navigation-links.spec.js:4:3 › should have working navigation links (3.3s)
  ✓  tests/navigation-links.spec.js:56:3 › should have working project links (1.8s)
  ✓  tests/navigation-links.spec.js:91:3 › should have working social media links (2.2s)

  4 passed (9.7s)
```

### HTML Report

```bash
# Generate and open HTML report
npx playwright test --reporter=html
npx playwright show-report
```

## 🎯 Best Practices Demonstrated

### 1. **Fast Test Execution**
- Parallel workers (2x)
- Optimized wait strategies (`commit` vs `networkidle`)
- Reduced timeouts where safe

### 2. **Reliability**
- Auto-retry for flaky tests
- Proper wait conditions
- Stable element selection

### 3. **Maintainability**
- ES modules throughout
- Clear test structure
- Descriptive test names
- Good logging

### 4. **Real-World Testing**
- Tests against live site (https://elamcb.github.io)
- Validates actual user flows
- Catches real broken links

### 5. **AI Integration**
- MCP server for AI-powered testing
- Demonstrates future of QA automation
- Production-ready implementation

## 📈 Performance Metrics

Current test suite performance:

| Metric | Value |
|--------|-------|
| **Total Tests** | 4 |
| **Execution Time** | ~10 seconds |
| **Success Rate** | 100% |
| **Browser Coverage** | Chromium, Firefox, WebKit |
| **Parallel Workers** | 2 |

## 🔧 Troubleshooting

### Tests failing locally?

```bash
# Clear Playwright cache
npx playwright install --force

# Run in debug mode
npx playwright test --debug

# Check specific test
npx playwright test tests/portfolio.spec.js --headed
```

### Timeout issues?

Increase timeouts in `playwright.config.js`:
```javascript
timeout: 60000, // Increase to 60 seconds
```

### Need screenshots on failure?

Add to `playwright.config.js`:
```javascript
use: {
  screenshot: 'only-on-failure',
  video: 'retain-on-failure',
}
```

## 🚀 Advanced Usage

### Custom Test Examples

#### Performance Testing
```javascript
test('homepage loads fast', async ({ page }) => {
  const startTime = Date.now();
  await page.goto('https://elamcb.github.io');
  const loadTime = Date.now() - startTime;
  
  expect(loadTime).toBeLessThan(3000); // Under 3 seconds
});
```

#### Mobile Testing
```javascript
test('mobile responsive', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
  await page.goto('https://elamcb.github.io');
  
  await expect(page.locator('.mobile-menu')).toBeVisible();
});
```

#### Visual Regression
```bash
# Take baseline screenshot
npx playwright test --update-snapshots

# Compare against baseline
npx playwright test
```

## 📚 Learning Resources

- [Playwright Documentation](https://playwright.dev)
- [MCP Protocol](https://modelcontextprotocol.io)
- [My Research on MCP Testing](../research/notebooks/mcp-software-testing.html)
- [GitHub Actions Workflows](https://docs.github.com/en/actions)

## 🤝 Contributing

This is my personal portfolio, but feel free to:
- ⭐ Star the repo if you find it useful
- 🐛 Report issues you find
- 💡 Suggest improvements
- 🔗 Share with others learning Playwright

## 📝 License

MIT License - Feel free to use this as a template for your own portfolio testing!

## 🔗 Links

- **Live Portfolio:** https://elamcb.github.io
- **GitHub Repo:** https://github.com/ElaMCB/ElaMCB.github.io
- **CI/CD Workflow:** [View Actions](https://github.com/ElaMCB/ElaMCB.github.io/actions)
- **MCP Setup Guide:** [MCP-SETUP-GUIDE.md](../MCP-SETUP-GUIDE.md)

---

**Built with AI-First Development Practices**

This testing framework was developed using AI-assisted development with Cursor AI and Claude Sonnet, demonstrating 3x faster test creation and maintenance.

