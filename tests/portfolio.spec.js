const { test, expect } = require('@playwright/test');

test('Portfolio smoke test', async ({ page }) => {
  await page.goto('https://elamcb.github.io');
  
  // Verify critical elements
  await expect(page).toHaveTitle(/Ela MCB/);
  await expect(page.getByRole('heading', { name: 'AI Projects' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Research' })).toBeVisible();
  
  // Check responsive design
  await page.setViewportSize({ width: 375, height: 667 }); // Mobile
  await page.reload(); // Ensure mobile layout loads
  await expect(page.getByRole('button', { name: 'Menu' })).toBeVisible({ timeout: 10000 });
});
