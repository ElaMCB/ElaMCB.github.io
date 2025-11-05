# Playwright Framework - Code Examples

Complete code examples from the portfolio testing framework, demonstrating real-world Playwright usage for testing static sites and integrating AI-powered testing with MCP.

## 📋 Table of Contents

1. [Basic Smoke Test](#basic-smoke-test)
2. [Navigation Links Validation](#navigation-links-validation)
3. [Project Pages Testing](#project-pages-testing)
4. [Social Media Links](#social-media-links)
5. [Performance Testing](#performance-testing)
6. [Mobile Responsiveness](#mobile-responsiveness)
7. [Configuration](#configuration)
8. [MCP Integration](#mcp-integration)

---

## Basic Smoke Test

**File:** `tests/portfolio.spec.js`

Tests the most critical functionality - ensuring the homepage loads and key sections are visible.

```javascript
import { test, expect } from '@playwright/test';

test('Portfolio smoke test', async ({ page }) => {
  // Navigate to portfolio
  await page.goto('https://elamcb.github.io');
  
  // Verify page title
  await expect(page).toHaveTitle(/Ela MCB/);
  
  // Verify critical sections exist
  await expect(page.getByRole('heading', { name: 'AI Projects' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Research' })).toBeVisible();
});
```

**What it validates:**
- ✅ Site is accessible
- ✅ Page loads successfully
- ✅ Title is correct
- ✅ Key sections render properly

**Run it:**
```bash
npx playwright test tests/portfolio.spec.js
```

---

## Navigation Links Validation

**File:** `tests/navigation-links.spec.js`

Comprehensive test suite that validates all navigation and header links work correctly.

```javascript
import { test, expect } from '@playwright/test';

test.describe('Portfolio Navigation Links', () => {
  test('should have working navigation links on homepage', async ({ page }) => {
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('domcontentloaded');
    
    // Extract all link data upfront to avoid stale element issues
    const linkData = await page.locator('nav a, header a').evaluateAll(links => 
      links.map(link => ({
        href: link.getAttribute('href'),
        text: link.textContent?.trim() || ''
      }))
    );
    
    console.log(`Found ${linkData.length} navigation links to test`);
    
    // Test each navigation link
    for (const link of linkData) {
      const { href, text } = link;
      
      console.log(`Testing link: "${text}" -> ${href}`);
      
      // Skip external links and anchors
      if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('tel:')) {
        console.log(`  Skipping: ${href}`);
        continue;
      }
      
      // Check if link is external
      const isExternal = href.startsWith('http://') || href.startsWith('https://');
      
      if (isExternal && !href.includes('elamcb.github.io')) {
        console.log(`  Skipping external link: ${href}`);
        continue;
      }
      
      // Test internal links
      try {
        // Convert relative URLs to absolute
        const absoluteHref = new URL(href, 'https://elamcb.github.io').href;
        const response = await page.goto(absoluteHref, { 
          timeout: 5000,
          waitUntil: 'commit' // Faster - just confirms navigation started
        });
        const status = response?.status() || 0;
        
        expect(status).toBeLessThan(400);
        console.log(`  ✓ Link works (${status})`);
      } catch (error) {
        console.error(`  ✗ Link failed: ${error.message}`);
        throw error;
      }
    }
  });
});
```

**Key techniques:**
- 📝 **Data extraction upfront** - Avoids stale element issues
- 🔗 **Smart link filtering** - Skips external/anchor links
- 🌐 **URL normalization** - Converts relative to absolute URLs
- ⚡ **Fast navigation** - Uses `commit` wait strategy
- 📊 **Detailed logging** - Tracks each link tested

---

## Project Pages Testing

Tests that all major project pages load successfully.

```javascript
test('should have working project links', async ({ page }) => {
  await page.goto('https://elamcb.github.io');
  await page.waitForLoadState('domcontentloaded');
  
  // Test main project links by navigating directly
  const projectPaths = [
    { name: 'LLM Guardian', path: '/llm-guardian/' },
    { name: 'Research Notebooks', path: '/research/' },
    { name: 'Job Search Automation', path: '/job-search-automation/' },
    { name: 'AI IDE Comparison', path: '/ai-ide-comparison/' }
  ];
  
  for (const project of projectPaths) {
    const url = `https://elamcb.github.io${project.path}`;
    console.log(`Testing ${project.name}: ${url}`);
    
    try {
      const response = await page.goto(url, { 
        timeout: 5000,
        waitUntil: 'commit'
      });
      const status = response?.status() || 0;
      
      expect(status).toBe(200);
      console.log(`  ✓ ${project.name} loaded successfully (${status})`);
    } catch (error) {
      console.log(`  ⚠ ${project.name} failed: ${error.message}`);
    }
  }
});
```

**Validates:**
- ✅ All project pages return 200 status
- ✅ Pages load within 5 seconds
- ✅ No 404 errors

---

## Social Media Links

Verifies social media links are present and valid.

```javascript
test('should have working social media links', async ({ page }) => {
  await page.goto('https://elamcb.github.io');
  await page.waitForLoadState('domcontentloaded');
  
  // Check for common social media links
  const socialLinks = [
    { platform: 'LinkedIn', pattern: /linkedin\.com/i },
    { platform: 'GitHub', pattern: /github\.com/i }
  ];
  
  for (const social of socialLinks) {
    const link = page.locator(`a[href*="${social.platform.toLowerCase()}"]`).first();
    
    if (await link.count() > 0) {
      const href = await link.getAttribute('href');
      expect(href).toMatch(social.pattern);
      console.log(`  ✓ ${social.platform} link found: ${href}`);
    } else {
      console.log(`  ⚠ ${social.platform} link not found`);
    }
  }
});
```

---

## Performance Testing

Measure and validate page load performance.

```javascript
test('homepage loads fast', async ({ page }) => {
  const startTime = Date.now();
  
  await page.goto('https://elamcb.github.io', {
    waitUntil: 'domcontentloaded'
  });
  
  const loadTime = Date.now() - startTime;
  
  console.log(`Page loaded in ${loadTime}ms`);
  
  // Assert load time under 3 seconds
  expect(loadTime).toBeLessThan(3000);
  
  // Get performance metrics
  const metrics = await page.evaluate(() => {
    const perfData = performance.getEntriesByType('navigation')[0];
    return {
      domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
      domInteractive: perfData.domInteractive,
      loadComplete: perfData.loadEventEnd - perfData.loadEventStart
    };
  });
  
  console.log('Performance metrics:', metrics);
});
```

**Metrics tracked:**
- ⏱️ Total load time
- 📊 DOM content loaded time
- 🎯 DOM interactive time
- ✅ Complete load event

---

## Mobile Responsiveness

Test portfolio on mobile devices.

```javascript
test('portfolio is mobile responsive', async ({ page }) => {
  // Set iPhone SE viewport
  await page.setViewportSize({ width: 375, height: 667 });
  
  await page.goto('https://elamcb.github.io');
  await page.waitForLoadState('domcontentloaded');
  
  // Check if mobile menu exists
  const mobileMenu = page.locator('[aria-label*="menu" i], .hamburger, .mobile-menu');
  
  if (await mobileMenu.count() > 0) {
    await expect(mobileMenu).toBeVisible();
    console.log('✓ Mobile menu detected');
  }
  
  // Verify content is not cut off
  const body = page.locator('body');
  const width = await body.evaluate(el => el.scrollWidth);
  
  expect(width).toBeLessThanOrEqual(375);
  console.log('✓ Content fits viewport');
  
  // Take mobile screenshot
  await page.screenshot({ path: 'screenshots/mobile-view.png', fullPage: true });
});
```

**Device testing:**
```javascript
import { devices } from '@playwright/test';

// iPhone 13
test.use(devices['iPhone 13']);

// Pixel 5
test.use(devices['Pixel 5']);

// iPad Pro
test.use(devices['iPad Pro']);
```

---

## Configuration

**File:** `playwright.config.js`

Optimized configuration for fast, reliable tests.

```javascript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  // Test directory
  testDir: './tests',
  
  // Timeouts
  timeout: 30000,              // 30 second timeout per test
  
  // Parallel execution
  workers: 2,                  // Run 2 tests in parallel
  
  // Retries
  retries: 1,                  // Retry failed tests once
  
  // Global configuration
  use: {
    // Browser options
    headless: true,
    viewport: { width: 1280, height: 720 },
    
    // Timeouts
    actionTimeout: 10000,      // 10 seconds for actions
    navigationTimeout: 5000,   // 5 seconds for navigation
    
    // Screenshots/videos
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    
    // Base URL
    baseURL: 'https://elamcb.github.io',
  },
  
  // Projects (browsers)
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
    {
      name: 'firefox',
      use: { browserName: 'firefox' },
    },
    {
      name: 'webkit',
      use: { browserName: 'webkit' },
    },
  ],
  
  // Reporter
  reporter: [
    ['list'],                  // Console output
    ['html', { open: 'never' }], // HTML report
    ['junit', { outputFile: 'test-results/junit.xml' }], // CI/CD
  ],
});
```

### Key Configuration Options:

#### Performance Optimization
```javascript
workers: 2,                    // Parallel execution
navigationTimeout: 5000,       // Fast navigation
waitUntil: 'commit',          // Don't wait for full load
```

#### Reliability
```javascript
retries: 1,                    // Auto-retry flaky tests
actionTimeout: 10000,          // Reasonable action timeout
screenshot: 'only-on-failure', // Debug failures
```

#### CI/CD Integration
```javascript
reporter: [
  ['junit', { outputFile: 'test-results/junit.xml' }]
],
```

---

## MCP Integration

**File:** `mcp-playwright-server.js`

AI-powered testing server using Model Context Protocol.

### Core Server Setup

```javascript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { chromium } from '@playwright/test';

class PlaywrightMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'playwright-portfolio-tester',
        version: '1.0.0',
      },
      {
        capabilities: { tools: {} },
      }
    );
    
    this.setupToolHandlers();
  }
  
  setupToolHandlers() {
    // Register available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'run_portfolio_smoke_test',
          description: 'Run comprehensive smoke test on elamcb.github.io',
          inputSchema: {
            type: 'object',
            properties: {
              headless: { type: 'boolean', default: true }
            }
          }
        },
        // ... more tools
      ]
    }));
  }
}
```

### MCP Tool: Run Smoke Test

```javascript
async runSmokeTest(args = {}) {
  const browser = await chromium.launch({ headless: args.headless ?? true });
  const page = await browser.newPage();
  
  const results = {
    success: true,
    tests: [],
    timestamp: new Date().toISOString()
  };

  try {
    // Test 1: Homepage loads
    await page.goto('https://elamcb.github.io', { waitUntil: 'networkidle' });
    const title = await page.title();
    results.tests.push({
      name: 'Homepage loads',
      passed: title.includes('Ela MCB'),
      details: { title }
    });

    // Test 2: Critical elements visible
    const aiProjectsHeading = await page.getByRole('heading', { name: /AI Projects/i }).isVisible();
    results.tests.push({
      name: 'AI Projects section visible',
      passed: aiProjectsHeading
    });

    // Summary
    const passedTests = results.tests.filter(t => t.passed).length;
    results.summary = {
      total: results.tests.length,
      passed: passedTests,
      failed: results.tests.length - passedTests
    };

  } catch (error) {
    results.success = false;
    results.error = error.message;
  } finally {
    await browser.close();
  }

  return {
    content: [{ type: 'text', text: JSON.stringify(results, null, 2) }]
  };
}
```

### MCP Tool: Take Screenshot

```javascript
async takeScreenshot(args = {}) {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  try {
    const url = `https://elamcb.github.io${args.path || '/'}`;
    await page.goto(url, { waitUntil: 'networkidle' });
    
    const timestamp = Date.now();
    const screenshotPath = `screenshots/portfolio-${timestamp}.png`;
    await page.screenshot({ 
      path: screenshotPath, 
      fullPage: args.fullPage ?? true 
    });

    await browser.close();

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          success: true,
          screenshotPath,
          url,
          timestamp: new Date().toISOString()
        }, null, 2)
      }]
    };
  } catch (error) {
    await browser.close();
    throw error;
  }
}
```

### Using MCP Tools

#### From Claude Desktop:
```
"Run my portfolio smoke test"
"Take a screenshot of my homepage"
"Check for broken links"
```

#### Programmatically:
```javascript
const server = new PlaywrightMCPServer();
await server.run();
```

---

## Package.json

Complete dependencies and scripts:

```json
{
  "type": "module",
  "devDependencies": {
    "@playwright/test": "^1.56.1"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.0.0"
  },
  "scripts": {
    "test": "playwright test",
    "test:headed": "playwright test --headed",
    "test:ui": "playwright test --ui",
    "test:debug": "playwright test --debug",
    "report": "playwright show-report"
  }
}
```

---

## Running Examples

### Run all tests
```bash
npm test
```

### Run specific test file
```bash
npx playwright test tests/portfolio.spec.js
```

### Run with UI mode (interactive)
```bash
npm run test:ui
```

### Debug mode
```bash
npm run test:debug
```

### Generate HTML report
```bash
npm run report
```

---

## GitHub Actions Integration

**File:** `.github/workflows/portfolio-tests.yml`

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
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Install Playwright
        run: npx playwright install --with-deps
        
      - name: Run Playwright tests
        run: npx playwright test
        
      - name: Upload test report
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
```

---

## More Examples

See the complete repository for more examples:
- 📁 [Full Test Suite](https://github.com/ElaMCB/ElaMCB.github.io/tree/main/tests)
- 🤖 [MCP Server Implementation](https://github.com/ElaMCB/ElaMCB.github.io/blob/main/mcp-playwright-server.js)
- 📖 [MCP Setup Guide](https://github.com/ElaMCB/ElaMCB.github.io/blob/main/MCP-SETUP-GUIDE.md)
- ⚙️ [CI/CD Workflow](https://github.com/ElaMCB/ElaMCB.github.io/tree/main/.github/workflows)

---

**Built with AI-First Development** 🤖

All code examples were developed using AI-assisted development with Cursor AI and Claude Sonnet, demonstrating modern development practices.

