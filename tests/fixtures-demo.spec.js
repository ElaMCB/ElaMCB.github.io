import { test, expect } from './fixtures/portfolio-fixtures.js';

/**
 * Demo tests showcasing custom fixtures
 * Demonstrates how fixtures simplify test setup and improve reusability
 */

test.describe('Fixture Examples', () => {
  test('using loadedPortfolioPage fixture', async ({ loadedPortfolioPage }) => {
    // Page is already loaded thanks to the fixture!
    await loadedPortfolioPage.verifyCriticalContent();
    console.log('✓ Used pre-loaded portfolio page fixture');
  });

  test('using mobile viewport fixture', async ({ mobilePage }) => {
    // Page is already set to mobile size
    await mobilePage.goto('https://elamcb.github.io');
    
    const viewportSize = mobilePage.viewportSize();
    expect(viewportSize.width).toBe(375);
    console.log(`✓ Mobile viewport: ${viewportSize.width}x${viewportSize.height}`);
  });

  test('using performance monitor fixture', async ({ page, performanceMonitor }) => {
    await page.goto('https://elamcb.github.io');
    
    await performanceMonitor.mark('content-loaded');
    
    // Do some test actions
    await page.waitForLoadState('networkidle');
    await performanceMonitor.mark('network-idle');
    
    // Measure time between marks
    const duration = await performanceMonitor.measure(
      'load-to-idle',
      'content-loaded',
      'network-idle'
    );
    
    console.log(`✓ Time to network idle: ${duration.toFixed(2)}ms`);
    expect(duration).toBeLessThan(5000);
  });

  test('using console collector fixture', async ({ page, consoleCollector }) => {
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('domcontentloaded');
    
    // Console messages are automatically collected
    // After test, fixture will log any errors or warnings
    
    console.log(`✓ Collected ${consoleCollector.log.length} console logs`);
  });

  test('using network monitor fixture', async ({ page, networkMonitor }) => {
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('networkidle');
    
    // Get network statistics
    const totalRequests = networkMonitor.getRequestCount();
    const imageRequests = networkMonitor.getRequestsByType('image');
    const scriptRequests = networkMonitor.getRequestsByType('script');
    
    console.log(`✓ Images loaded: ${imageRequests.length}`);
    console.log(`✓ Scripts loaded: ${scriptRequests.length}`);
    
    expect(totalRequests).toBeGreaterThan(0);
    expect(networkMonitor.getFailedRequests().length).toBe(0);
  });

  test('combining multiple fixtures', async ({ 
    loadedPortfolioPage, 
    performanceMonitor, 
    consoleCollector,
    networkMonitor 
  }) => {
    // Multiple fixtures work together seamlessly!
    
    await performanceMonitor.mark('test-action-start');
    
    const socialLinks = await loadedPortfolioPage.getSocialLinks();
    
    await performanceMonitor.mark('test-action-end');
    const duration = await performanceMonitor.measure(
      'social-links-fetch',
      'test-action-start',
      'test-action-end'
    );
    
    console.log(`✓ Social links retrieved in ${duration.toFixed(2)}ms`);
    console.log(`✓ Console errors: ${consoleCollector.error.length}`);
    console.log(`✓ Network requests: ${networkMonitor.getRequestCount()}`);
    
    expect(Object.keys(socialLinks).length).toBeGreaterThan(0);
  });
});

