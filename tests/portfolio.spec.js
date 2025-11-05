const { test, expect } = require('@playwright/test');

test('Portfolio smoke test', async ({ page }) => {
  await page.goto('https://elamcb.github.io');
  
  // Verify critical elements
  await expect(page).toHaveTitle(/Ela MCB/);
  await expect(page.getByText('Projects')).toBeVisible();
  await expect(page.getByText('Research')).toBeVisible();
  
  // Check responsive design
  await page.setViewportSize({ width: 375, height: 667 }); // Mobile
  await expect(page.getByRole('navigation')).toBeVisible();
});
