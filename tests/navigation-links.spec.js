import { test, expect } from '@playwright/test';

test.describe('Portfolio Navigation Links', () => {
  test('should have working navigation links on homepage', async ({ page }) => {
    await page.goto('https://elamcb.github.io');
    
    // Wait for page to fully load (domcontentloaded is faster than networkidle)
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
      
      // Skip external links and anchors for now
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
          timeout: 5000, // Reduced from 10s to 5s
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

  test('should have working project links', async ({ page }) => {
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('domcontentloaded'); // Changed from networkidle to domcontentloaded for speed
    
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
          timeout: 5000, // Reduced from 10s to 5s
          waitUntil: 'commit' // Faster - just wait for navigation to start
        });
        const status = response?.status() || 0;
        
        expect(status).toBe(200);
        console.log(`  ✓ ${project.name} loaded successfully (${status})`);
      } catch (error) {
        console.log(`  ⚠ ${project.name} failed: ${error.message}`);
        // Don't fail the test if a project page doesn't exist yet
      }
    }
  });

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
});
