import { test, expect } from '@playwright/test';
import { PortfolioPage } from './pages/PortfolioPage.js';

test.describe('Portfolio Page', () => {
  test('smoke test - critical content loads', { 
    tag: ['@smoke', '@critical', '@fast'] 
  }, async ({ page }) => {
    const portfolioPage = new PortfolioPage(page);
    await portfolioPage.goto();
    await portfolioPage.verifyCriticalContent();
  });

  test('social media links are present', { 
    tag: ['@smoke', '@links'] 
  }, async ({ page }) => {
    const portfolioPage = new PortfolioPage(page);
    await portfolioPage.goto();
    
    const socialLinks = await portfolioPage.getSocialLinks();
    
    if (socialLinks.linkedin) {
      expect(socialLinks.linkedin).toMatch(/linkedin\.com/i);
      console.log(`✓ LinkedIn link found: ${socialLinks.linkedin}`);
    }
    
    if (socialLinks.github) {
      expect(socialLinks.github).toMatch(/github\.com/i);
      console.log(`✓ GitHub link found: ${socialLinks.github}`);
    }
  });
});
