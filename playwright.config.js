import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests', // Directory where tests are located
  timeout: 30000, // 30 second timeout per test
  workers: 2, // Run tests in parallel with 2 workers
  retries: 1, // Retry failed tests once (for flaky network issues)
  use: {
    headless: true,
    viewport: { width: 1280, height: 720 },
    actionTimeout: 10000, // 10 second timeout for actions
    navigationTimeout: 5000, // 5 second timeout for navigations (faster)
  },
});
