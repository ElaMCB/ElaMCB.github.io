import { defineConfig, devices } from '@playwright/test';

/**
 * Advanced Playwright Configuration
 * Optimized for performance, parallel execution, and comprehensive reporting
 */
export default defineConfig({
  testDir: './tests',
  
  // Test execution settings
  timeout: 30000, // 30 second timeout per test
  globalTimeout: 60 * 60 * 1000, // 1 hour for entire test suite
  expect: {
    timeout: 5000, // Timeout for expect() assertions
  },
  
  // Parallel execution optimization
  workers: process.env.CI ? 2 : 4, // More workers locally, fewer in CI
  fullyParallel: true, // Run tests in parallel within files
  retries: process.env.CI ? 2 : 1, // More retries in CI
  
  // Fail fast in CI to save resources
  maxFailures: process.env.CI ? 5 : undefined,
  
  // Reporter configuration
  reporter: [
    ['html', { 
      outputFolder: 'playwright-report', 
      open: 'never',
      attachmentsBaseURL: process.env.CI ? undefined : 'file:///'
    }],
    ['list'], // Terminal output
    ['json', { outputFile: 'test-results/results.json' }], // JSON for processing
    process.env.CI ? ['github'] : ['line'], // CI-specific reporter
  ],
  
  // Global test settings
  use: {
    // Browser settings
    headless: true,
    viewport: { width: 1280, height: 720 },
    
    // Timeout settings
    actionTimeout: 10000,
    navigationTimeout: 10000,
    
    // Performance optimizations
    bypassCSP: false, // Don't bypass CSP for realistic testing
    ignoreHTTPSErrors: false, // Catch SSL issues
    
    // Screenshot and trace settings
    screenshot: {
      mode: 'only-on-failure',
      fullPage: true,
    },
    trace: 'retain-on-failure', // Detailed trace for debugging
    video: 'retain-on-failure', // Record video on failure
    
    // Network settings
    launchOptions: {
      // Optimize browser launch
      args: [
        '--disable-dev-shm-usage', // Overcome limited resource problems
        '--disable-blink-features=AutomationControlled', // More realistic browser
      ],
    },
  },
  
  // Test metadata
  metadata: {
    version: '1.0.0',
    environment: process.env.CI ? 'CI' : 'local',
  },
  
  // Projects for multi-browser testing
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    // Uncomment to test on additional browsers
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },
    // {
    //   name: 'mobile-chrome',
    //   use: { ...devices['Pixel 5'] },
    // },
    // {
    //   name: 'mobile-safari',
    //   use: { ...devices['iPhone 12'] },
    // },
  ],
  
  // Output configuration
  outputDir: 'test-results',
  
  // Web server (if needed for local dev)
  // webServer: {
  //   command: 'npm run start',
  //   port: 3000,
  //   reuseExistingServer: !process.env.CI,
  // },
});
