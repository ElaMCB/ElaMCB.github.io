import { test, expect } from '@playwright/test';

test('Portfolio smoke test', async ({ page }) => {
  await page.goto('https://elamcb.github.io');
  
  // Verify critical elements
  await expect(page).toHaveTitle(/Ela MCB/);
  await expect(page.getByRole('heading', { name: 'AI Projects' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Research' })).toBeVisible();
});
