import { test, expect } from '@playwright/test';

/**
 * Visual Regression Testing
 * Captures screenshots and compares them to baseline images
 * Run with: npx playwright test --update-snapshots (to update baselines)
 */

test.describe('Visual Regression Tests', () => {
  test('homepage should match visual baseline', { 
    tag: ['@visual', '@slow'] 
  }, async ({ page }) => {
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('networkidle'); // Wait for all content to load
    
    // Take full page screenshot and compare
    await expect(page).toHaveScreenshot('homepage-full.png', {
      fullPage: true,
      animations: 'disabled', // Disable animations for consistent screenshots
    });
    
    console.log('✓ Homepage visual baseline matched');
  });

  test('homepage above the fold should match baseline', { 
    tag: ['@visual', '@fast'] 
  }, async ({ page }) => {
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('domcontentloaded');
    
    // Capture just the viewport (above the fold)
    await expect(page).toHaveScreenshot('homepage-viewport.png', {
      fullPage: false,
      animations: 'disabled',
    });
    
    console.log('✓ Above-the-fold visual baseline matched');
  });

  test('responsive design - mobile view', { 
    tag: ['@visual', '@responsive', '@mobile'] 
  }, async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('domcontentloaded');
    
    await expect(page).toHaveScreenshot('homepage-mobile.png', {
      fullPage: true,
      animations: 'disabled',
    });
    
    console.log('✓ Mobile view visual baseline matched');
  });

  test('responsive design - tablet view', { 
    tag: ['@visual', '@responsive', '@tablet'] 
  }, async ({ page }) => {
    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 }); // iPad
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('domcontentloaded');
    
    await expect(page).toHaveScreenshot('homepage-tablet.png', {
      fullPage: true,
      animations: 'disabled',
    });
    
    console.log('✓ Tablet view visual baseline matched');
  });

  test('navigation component matches baseline', { 
    tag: ['@visual', '@component'] 
  }, async ({ page }) => {
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('domcontentloaded');
    
    // Capture specific component
    const nav = page.locator('nav, header').first();
    await expect(nav).toHaveScreenshot('navigation-component.png', {
      animations: 'disabled',
    });
    
    console.log('✓ Navigation component visual baseline matched');
  });

  test('dark mode renders correctly', { 
    tag: ['@visual', '@darkmode'] 
  }, async ({ page }) => {
    await page.goto('https://elamcb.github.io');
    
    // Emulate dark color scheme
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.waitForLoadState('domcontentloaded');
    
    await expect(page).toHaveScreenshot('homepage-dark-mode.png', {
      fullPage: true,
      animations: 'disabled',
    });
    
    console.log('✓ Dark mode visual baseline matched');
  });

  test('print layout matches baseline', { 
    tag: ['@visual', '@print'] 
  }, async ({ page }) => {
    await page.goto('https://elamcb.github.io');
    
    // Emulate print media
    await page.emulateMedia({ media: 'print' });
    await page.waitForLoadState('domcontentloaded');
    
    await expect(page).toHaveScreenshot('homepage-print.png', {
      fullPage: true,
      animations: 'disabled',
    });
    
    console.log('✓ Print layout visual baseline matched');
  });
});

