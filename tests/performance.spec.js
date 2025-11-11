import { test, expect } from '@playwright/test';

test.describe('Performance Metrics', () => {
  test('should meet Core Web Vitals thresholds', { 
    tag: ['@performance', '@slow', '@metrics'] 
  }, async ({ page }) => {
    // Navigate and collect performance metrics
    await page.goto('https://elamcb.github.io');
    
    // Wait for page to be fully loaded
    await page.waitForLoadState('load');
    
    // Collect Core Web Vitals using PerformanceObserver
    const metrics = await page.evaluate(() => {
      return new Promise((resolve) => {
        const metrics = {};
        
        // Largest Contentful Paint (LCP)
        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1];
          metrics.LCP = lastEntry.renderTime || lastEntry.loadTime;
        }).observe({ entryTypes: ['largest-contentful-paint'] });
        
        // First Input Delay (FID) - simulated via event timing
        new PerformanceObserver((list) => {
          const entries = list.getEntries();
          entries.forEach((entry) => {
            if (entry.processingStart && entry.startTime) {
              metrics.FID = entry.processingStart - entry.startTime;
            }
          });
        }).observe({ entryTypes: ['first-input'] });
        
        // Cumulative Layout Shift (CLS)
        let clsScore = 0;
        new PerformanceObserver((list) => {
          list.getEntries().forEach((entry) => {
            if (!entry.hadRecentInput) {
              clsScore += entry.value;
            }
          });
          metrics.CLS = clsScore;
        }).observe({ entryTypes: ['layout-shift'] });
        
        // Get Navigation Timing metrics
        const navigation = performance.getEntriesByType('navigation')[0];
        if (navigation) {
          metrics.TTFB = navigation.responseStart - navigation.requestStart; // Time to First Byte
          metrics.DOMContentLoaded = navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart;
          metrics.LoadComplete = navigation.loadEventEnd - navigation.loadEventStart;
        }
        
        // Get Paint Timing
        const paintEntries = performance.getEntriesByType('paint');
        paintEntries.forEach((entry) => {
          if (entry.name === 'first-paint') {
            metrics.FP = entry.startTime;
          }
          if (entry.name === 'first-contentful-paint') {
            metrics.FCP = entry.startTime;
          }
        });
        
        // Wait a bit for metrics to settle
        setTimeout(() => resolve(metrics), 2000);
      });
    });
    
    console.log('📊 Performance Metrics:');
    console.log(`  First Paint (FP): ${metrics.FP?.toFixed(2)}ms`);
    console.log(`  First Contentful Paint (FCP): ${metrics.FCP?.toFixed(2)}ms`);
    console.log(`  Largest Contentful Paint (LCP): ${metrics.LCP?.toFixed(2)}ms`);
    console.log(`  Time to First Byte (TTFB): ${metrics.TTFB?.toFixed(2)}ms`);
    console.log(`  Cumulative Layout Shift (CLS): ${metrics.CLS?.toFixed(4)}`);
    console.log(`  DOM Content Loaded: ${metrics.DOMContentLoaded?.toFixed(2)}ms`);
    
    // Assert Core Web Vitals thresholds (Google's "Good" thresholds)
    if (metrics.LCP) {
      expect(metrics.LCP).toBeLessThan(2500); // LCP should be < 2.5s
      console.log(`  ✓ LCP is good (< 2.5s)`);
    }
    
    if (metrics.FCP) {
      expect(metrics.FCP).toBeLessThan(1800); // FCP should be < 1.8s
      console.log(`  ✓ FCP is good (< 1.8s)`);
    }
    
    if (metrics.CLS !== undefined) {
      expect(metrics.CLS).toBeLessThan(0.1); // CLS should be < 0.1
      console.log(`  ✓ CLS is good (< 0.1)`);
    }
    
    if (metrics.TTFB) {
      expect(metrics.TTFB).toBeLessThan(600); // TTFB should be < 600ms
      console.log(`  ✓ TTFB is good (< 600ms)`);
    }
  });

  test('should track page load time', { 
    tag: ['@performance', '@fast'] 
  }, async ({ page }) => {
    const startTime = Date.now();
    
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('load');
    
    const loadTime = Date.now() - startTime;
    
    console.log(`⏱️  Total page load time: ${loadTime}ms`);
    
    // Assert reasonable load time
    expect(loadTime).toBeLessThan(3000); // Should load in under 3 seconds
    console.log(`  ✓ Page loaded quickly (< 3s)`);
  });

  test('should measure resource loading performance', { 
    tag: ['@performance', '@metrics'] 
  }, async ({ page }) => {
    await page.goto('https://elamcb.github.io');
    
    // Get resource timing data
    const resourceMetrics = await page.evaluate(() => {
      const resources = performance.getEntriesByType('resource');
      
      const stats = {
        totalResources: resources.length,
        byType: {},
        slowest: [],
        totalTransferSize: 0
      };
      
      resources.forEach((resource) => {
        // Group by type
        const type = resource.initiatorType || 'other';
        if (!stats.byType[type]) {
          stats.byType[type] = { count: 0, totalDuration: 0 };
        }
        stats.byType[type].count++;
        stats.byType[type].totalDuration += resource.duration;
        
        // Track transfer size if available
        if (resource.transferSize) {
          stats.totalTransferSize += resource.transferSize;
        }
        
        // Track slowest resources
        stats.slowest.push({
          name: resource.name.split('/').pop(),
          duration: resource.duration,
          type: type
        });
      });
      
      // Sort and keep top 5 slowest
      stats.slowest.sort((a, b) => b.duration - a.duration);
      stats.slowest = stats.slowest.slice(0, 5);
      
      return stats;
    });
    
    console.log('📦 Resource Loading Metrics:');
    console.log(`  Total resources: ${resourceMetrics.totalResources}`);
    console.log(`  Total transfer size: ${(resourceMetrics.totalTransferSize / 1024).toFixed(2)} KB`);
    console.log(`  Resources by type:`);
    
    Object.entries(resourceMetrics.byType).forEach(([type, data]) => {
      console.log(`    ${type}: ${data.count} (avg: ${(data.totalDuration / data.count).toFixed(2)}ms)`);
    });
    
    console.log(`  Slowest resources:`);
    resourceMetrics.slowest.forEach((resource, i) => {
      console.log(`    ${i + 1}. ${resource.name} (${resource.type}): ${resource.duration.toFixed(2)}ms`);
    });
    
    // Assert reasonable resource count
    expect(resourceMetrics.totalResources).toBeLessThan(100); // Not too many resources
    console.log(`  ✓ Resource count is reasonable`);
  });
});

