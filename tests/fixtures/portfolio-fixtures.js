import { test as base } from '@playwright/test';
import { PortfolioPage } from '../pages/PortfolioPage.js';

/**
 * Custom Test Fixtures
 * Provides reusable setup and teardown logic for tests
 * Showcases advanced Playwright features and optimization
 */

export const test = base.extend({
  /**
   * Automatically initialized PortfolioPage for every test
   * Usage: async ({ portfolioPage }) => { ... }
   */
  portfolioPage: async ({ page }, use) => {
    const portfolioPage = new PortfolioPage(page);
    await use(portfolioPage);
    // Cleanup happens automatically after test
  },

  /**
   * Pre-loaded homepage - navigates before each test
   * Usage: async ({ loadedPortfolioPage }) => { ... }
   */
  loadedPortfolioPage: async ({ page }, use) => {
    const portfolioPage = new PortfolioPage(page);
    await portfolioPage.goto();
    await use(portfolioPage);
  },

  /**
   * Authenticated context (placeholder for future auth needs)
   * Can be expanded when authentication is added
   */
  authenticatedPage: async ({ page }, use) => {
    // Add authentication logic here when needed
    // For now, just pass through the regular page
    await use(page);
  },

  /**
   * Mobile viewport fixture
   * Usage: async ({ mobilePage }) => { ... }
   */
  mobilePage: async ({ page }, use) => {
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
    await use(page);
  },

  /**
   * Tablet viewport fixture
   * Usage: async ({ tabletPage }) => { ... }
   */
  tabletPage: async ({ page }, use) => {
    await page.setViewportSize({ width: 768, height: 1024 }); // iPad
    await use(page);
  },

  /**
   * Desktop viewport fixture (large screen)
   * Usage: async ({ desktopPage }) => { ... }
   */
  desktopPage: async ({ page }, use) => {
    await page.setViewportSize({ width: 1920, height: 1080 }); // Full HD
    await use(page);
  },

  /**
   * Performance monitoring fixture
   * Automatically tracks and logs performance metrics for tests
   */
  performanceMonitor: async ({ page }, use) => {
    const metrics = {};
    
    // Start performance monitoring
    await page.evaluate(() => {
      window.performanceMarks = [];
      performance.mark('test-start');
    });
    
    // Provide API to tests
    const monitor = {
      mark: async (name) => {
        await page.evaluate((markName) => {
          performance.mark(markName);
          window.performanceMarks.push(markName);
        }, name);
      },
      
      measure: async (name, startMark, endMark) => {
        return await page.evaluate(({ measureName, start, end }) => {
          performance.measure(measureName, start, end);
          const measure = performance.getEntriesByName(measureName)[0];
          return measure.duration;
        }, { measureName: name, start: startMark, end: endMark });
      },
      
      getMetrics: async () => {
        return await page.evaluate(() => {
          const measures = performance.getEntriesByType('measure');
          return measures.map(m => ({
            name: m.name,
            duration: m.duration
          }));
        });
      }
    };
    
    await use(monitor);
    
    // Log metrics after test
    const finalMetrics = await monitor.getMetrics();
    if (finalMetrics.length > 0) {
      console.log('\n  📊 Performance Measurements:');
      finalMetrics.forEach(m => {
        console.log(`    ${m.name}: ${m.duration.toFixed(2)}ms`);
      });
    }
  },

  /**
   * Screenshot helper with automatic naming
   * Takes screenshots in a consistent location
   */
  screenshotHelper: async ({ page }, use, testInfo) => {
    const helper = {
      capture: async (name) => {
        const screenshotPath = `screenshots/${testInfo.title}-${name}.png`;
        await page.screenshot({ 
          path: screenshotPath,
          fullPage: true 
        });
        console.log(`  📸 Screenshot saved: ${screenshotPath}`);
        return screenshotPath;
      }
    };
    
    await use(helper);
  },

  /**
   * Console message collector
   * Captures and provides access to all console messages during test
   */
  consoleCollector: async ({ page }, use) => {
    const messages = {
      log: [],
      error: [],
      warning: [],
      info: []
    };
    
    page.on('console', (msg) => {
      const type = msg.type();
      const text = msg.text();
      
      if (type === 'error') messages.error.push(text);
      else if (type === 'warning') messages.warning.push(text);
      else if (type === 'info') messages.info.push(text);
      else messages.log.push(text);
    });
    
    await use(messages);
    
    // Log summary after test
    if (messages.error.length > 0) {
      console.log(`\n  ⚠️  Console Errors (${messages.error.length}):`);
      messages.error.forEach(err => console.log(`    ${err}`));
    }
    if (messages.warning.length > 0) {
      console.log(`\n  ⚠️  Console Warnings (${messages.warning.length}):`);
      messages.warning.forEach(warn => console.log(`    ${warn}`));
    }
  },

  /**
   * Network request interceptor and logger
   * Tracks all network requests during test execution
   */
  networkMonitor: async ({ page }, use) => {
    const requests = [];
    const failedRequests = [];
    
    page.on('request', (request) => {
      requests.push({
        url: request.url(),
        method: request.method(),
        resourceType: request.resourceType()
      });
    });
    
    page.on('requestfailed', (request) => {
      failedRequests.push({
        url: request.url(),
        failure: request.failure()
      });
    });
    
    const monitor = {
      getRequests: () => requests,
      getFailedRequests: () => failedRequests,
      getRequestsByType: (type) => requests.filter(r => r.resourceType === type),
      getRequestCount: () => requests.length
    };
    
    await use(monitor);
    
    // Log summary
    console.log(`\n  🌐 Network Activity:`);
    console.log(`    Total requests: ${requests.length}`);
    if (failedRequests.length > 0) {
      console.log(`    Failed requests: ${failedRequests.length}`);
      failedRequests.forEach(req => {
        console.log(`      ${req.url} - ${req.failure?.errorText}`);
      });
    }
  }
});

export { expect } from '@playwright/test';

