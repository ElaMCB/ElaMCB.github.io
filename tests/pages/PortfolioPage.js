import { expect } from '@playwright/test';

/**
 * Page Object Model for Portfolio Homepage
 * Encapsulates page interactions for better maintainability and reusability
 */
export class PortfolioPage {
  constructor(page) {
    this.page = page;
    this.url = 'https://elamcb.github.io';
    
    // Locators - defined once, reused everywhere
    this.navigation = {
      links: page.locator('nav a, header a'),
      home: page.locator('a[href="/"]'),
    };
    
    this.headings = {
      aiProjects: page.getByRole('heading', { name: 'AI Projects' }),
      research: page.getByRole('heading', { name: 'Research' }),
    };
    
    this.socialLinks = {
      linkedin: page.locator('a[href*="linkedin"]').first(),
      github: page.locator('a[href*="github"]').first(),
    };
  }

  /**
   * Navigate to homepage with optimized wait strategy
   */
  async goto() {
    await this.page.goto(this.url, {
      waitUntil: 'domcontentloaded', // Optimized: faster than 'load'
    });
  }

  /**
   * Get all navigation links data in one batch (avoids multiple DOM queries)
   */
  async getNavigationLinks() {
    return await this.navigation.links.evaluateAll(links => 
      links.map(link => ({
        href: link.getAttribute('href'),
        text: link.textContent?.trim() || '',
        isExternal: link.getAttribute('target') === '_blank'
      }))
    );
  }

  /**
   * Check if critical content is visible
   */
  async verifyCriticalContent() {
    await expect(this.page).toHaveTitle(/Ela MCB/);
    await expect(this.headings.aiProjects).toBeVisible();
    await expect(this.headings.research).toBeVisible();
  }

  /**
   * Get social media links
   */
  async getSocialLinks() {
    const links = {};
    
    if (await this.socialLinks.linkedin.count() > 0) {
      links.linkedin = await this.socialLinks.linkedin.getAttribute('href');
    }
    
    if (await this.socialLinks.github.count() > 0) {
      links.github = await this.socialLinks.github.getAttribute('href');
    }
    
    return links;
  }

  /**
   * Navigate to a project page
   */
  async navigateToProject(projectPath) {
    const url = `${this.url}${projectPath}`;
    const response = await this.page.goto(url, {
      timeout: 5000,
      waitUntil: 'commit', // Optimized: just wait for navigation to start
    });
    return response;
  }
}

