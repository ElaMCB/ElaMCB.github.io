#!/usr/bin/env node

/**
 * MCP Server for Playwright Portfolio Testing
 * Allows AI assistants to run tests on elamcb.github.io
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { chromium } from '@playwright/test';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';

const PORTFOLIO_URL = 'https://elamcb.github.io';

class PlaywrightMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'playwright-portfolio-tester',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    
    // Error handling
    this.server.onerror = (error) => console.error('[MCP Error]', error);
    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  setupToolHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'run_portfolio_smoke_test',
          description: 'Run comprehensive smoke test on elamcb.github.io portfolio',
          inputSchema: {
            type: 'object',
            properties: {
              headless: {
                type: 'boolean',
                description: 'Run browser in headless mode',
                default: true
              }
            }
          }
        },
        {
          name: 'screenshot_portfolio',
          description: 'Take screenshot of portfolio page for visual testing',
          inputSchema: {
            type: 'object',
            properties: {
              path: {
                type: 'string',
                description: 'URL path to screenshot (e.g., "/", "/llm-guardian/", "/research/")',
                default: '/'
              },
              fullPage: {
                type: 'boolean',
                description: 'Capture full scrollable page',
                default: true
              }
            },
            required: ['path']
          }
        },
        {
          name: 'check_broken_links',
          description: 'Check for broken links on portfolio pages',
          inputSchema: {
            type: 'object',
            properties: {
              path: {
                type: 'string',
                description: 'URL path to check links (e.g., "/", "/llm-guardian/")',
                default: '/'
              }
            }
          }
        },
        {
          name: 'test_mobile_responsive',
          description: 'Test portfolio responsiveness on mobile devices',
          inputSchema: {
            type: 'object',
            properties: {
              device: {
                type: 'string',
                description: 'Device to emulate (iPhone 13, Pixel 5, etc)',
                default: 'iPhone 13'
              }
            }
          }
        },
        {
          name: 'measure_performance',
          description: 'Measure page load performance metrics',
          inputSchema: {
            type: 'object',
            properties: {
              path: {
                type: 'string',
                description: 'URL path to measure',
                default: '/'
              }
            }
          }
        }
      ]
    }));

    // Handle tool execution
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      try {
        switch (request.params.name) {
          case 'run_portfolio_smoke_test':
            return await this.runSmokeTest(request.params.arguments);
          case 'screenshot_portfolio':
            return await this.takeScreenshot(request.params.arguments);
          case 'check_broken_links':
            return await this.checkBrokenLinks(request.params.arguments);
          case 'test_mobile_responsive':
            return await this.testMobileResponsive(request.params.arguments);
          case 'measure_performance':
            return await this.measurePerformance(request.params.arguments);
          default:
            throw new Error(`Unknown tool: ${request.params.name}`);
        }
      } catch (error) {
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              success: false,
              error: error.message,
              stack: error.stack
            }, null, 2)
          }],
          isError: true
        };
      }
    });
  }

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
      await page.goto(PORTFOLIO_URL, { waitUntil: 'networkidle' });
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
        passed: aiProjectsHeading,
        details: { visible: aiProjectsHeading }
      });

      const researchHeading = await page.getByRole('heading', { name: /Research/i }).isVisible();
      results.tests.push({
        name: 'Research section visible',
        passed: researchHeading,
        details: { visible: researchHeading }
      });

      // Test 3: Navigation exists
      const navExists = await page.locator('nav').count() > 0;
      results.tests.push({
        name: 'Navigation exists',
        passed: navExists,
        details: { count: await page.locator('nav').count() }
      });

      // Test 4: Links are clickable
      const links = await page.locator('a').count();
      results.tests.push({
        name: 'Links present',
        passed: links > 0,
        details: { linkCount: links }
      });

      // Summary
      const passedTests = results.tests.filter(t => t.passed).length;
      results.summary = {
        total: results.tests.length,
        passed: passedTests,
        failed: results.tests.length - passedTests,
        success: passedTests === results.tests.length
      };

    } catch (error) {
      results.success = false;
      results.error = error.message;
    } finally {
      await browser.close();
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(results, null, 2)
      }]
    };
  }

  async takeScreenshot(args = {}) {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    
    try {
      const url = `${PORTFOLIO_URL}${args.path || '/'}`;
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

  async checkBrokenLinks(args = {}) {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    
    try {
      const url = `${PORTFOLIO_URL}${args.path || '/'}`;
      await page.goto(url, { waitUntil: 'networkidle' });

      // Get all links
      const links = await page.$$eval('a[href]', anchors => 
        anchors.map(a => ({
          href: a.href,
          text: a.textContent.trim()
        }))
      );

      const results = {
        total: links.length,
        working: 0,
        broken: 0,
        links: []
      };

      // Check each link (limit to first 20 to avoid timeout)
      for (const link of links.slice(0, 20)) {
        try {
          const response = await page.goto(link.href, { 
            waitUntil: 'domcontentloaded',
            timeout: 5000 
          });
          
          const status = response?.status() || 0;
          const working = status >= 200 && status < 400;
          
          results.links.push({
            url: link.href,
            text: link.text,
            status,
            working
          });

          if (working) results.working++;
          else results.broken++;
        } catch (error) {
          results.links.push({
            url: link.href,
            text: link.text,
            error: error.message,
            working: false
          });
          results.broken++;
        }
      }

      await browser.close();

      return {
        content: [{
          type: 'text',
          text: JSON.stringify(results, null, 2)
        }]
      };
    } catch (error) {
      await browser.close();
      throw error;
    }
  }

  async testMobileResponsive(args = {}) {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({
      ...chromium.devices[args.device || 'iPhone 13']
    });
    const page = await context.newPage();
    
    try {
      await page.goto(PORTFOLIO_URL, { waitUntil: 'networkidle' });
      
      const viewport = page.viewportSize();
      const screenshot = `screenshots/mobile-${Date.now()}.png`;
      await page.screenshot({ path: screenshot });

      const results = {
        success: true,
        device: args.device || 'iPhone 13',
        viewport,
        screenshot,
        tests: []
      };

      // Check if hamburger menu exists for mobile
      const hasHamburger = await page.locator('[aria-label*="menu" i], .hamburger, .mobile-menu-toggle').count() > 0;
      results.tests.push({
        name: 'Mobile menu present',
        passed: hasHamburger || viewport.width > 768
      });

      // Check text is readable (not too small)
      const bodyFontSize = await page.evaluate(() => {
        return window.getComputedStyle(document.body).fontSize;
      });
      results.tests.push({
        name: 'Font size readable',
        passed: parseInt(bodyFontSize) >= 14,
        details: { fontSize: bodyFontSize }
      });

      await browser.close();

      return {
        content: [{
          type: 'text',
          text: JSON.stringify(results, null, 2)
        }]
      };
    } catch (error) {
      await browser.close();
      throw error;
    }
  }

  async measurePerformance(args = {}) {
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    
    try {
      const url = `${PORTFOLIO_URL}${args.path || '/'}`;
      
      const startTime = Date.now();
      await page.goto(url, { waitUntil: 'networkidle' });
      const loadTime = Date.now() - startTime;

      const metrics = await page.evaluate(() => {
        const perfData = performance.getEntriesByType('navigation')[0];
        return {
          domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
          domInteractive: perfData.domInteractive,
          loadComplete: perfData.loadEventEnd - perfData.loadEventStart
        };
      });

      await browser.close();

      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: true,
            url,
            loadTime: `${loadTime}ms`,
            metrics,
            performance: loadTime < 3000 ? 'EXCELLENT' : loadTime < 5000 ? 'GOOD' : 'NEEDS_IMPROVEMENT'
          }, null, 2)
        }]
      };
    } catch (error) {
      await browser.close();
      throw error;
    }
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('MCP Playwright Server running on stdio');
  }
}

// Start server
const server = new PlaywrightMCPServer();
server.run().catch(console.error);

