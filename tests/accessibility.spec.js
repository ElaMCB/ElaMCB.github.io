import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

/**
 * Accessibility Testing using axe-core
 * Tests WCAG 2.1 compliance and accessibility best practices
 * Install: npm install --save-dev @axe-core/playwright
 */

test.describe('Accessibility Tests', () => {
  test('homepage should not have accessibility violations', { 
    tag: ['@a11y', '@critical', '@wcag'] 
  }, async ({ page }) => {
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('domcontentloaded');
    
    // Run accessibility scan
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']) // WCAG 2.1 Level A and AA
      .analyze();
    
    console.log('♿ Accessibility Scan Results:');
    console.log(`  Total violations: ${accessibilityScanResults.violations.length}`);
    
    // Log violations if any
    if (accessibilityScanResults.violations.length > 0) {
      console.log('\n  Violations found:');
      accessibilityScanResults.violations.forEach((violation, i) => {
        console.log(`\n  ${i + 1}. ${violation.id} (${violation.impact})`);
        console.log(`     ${violation.description}`);
        console.log(`     Help: ${violation.helpUrl}`);
        console.log(`     Affected elements: ${violation.nodes.length}`);
        violation.nodes.forEach((node, j) => {
          console.log(`       ${j + 1}. ${node.html.substring(0, 80)}...`);
        });
      });
    }
    
    // Assert no violations
    expect(accessibilityScanResults.violations).toEqual([]);
    console.log('  ✓ No accessibility violations found');
  });

  test('critical accessibility features are present', { 
    tag: ['@a11y', '@fast'] 
  }, async ({ page }) => {
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('domcontentloaded');
    
    // Check for skip navigation link
    const skipLink = page.locator('a[href="#main"], a[href="#content"]').first();
    const hasSkipLink = await skipLink.count() > 0;
    console.log(`  Skip navigation link: ${hasSkipLink ? '✓' : '✗'}`);
    
    // Check for proper heading hierarchy
    const headings = await page.locator('h1, h2, h3, h4, h5, h6').evaluateAll(elements => 
      elements.map(el => ({ level: parseInt(el.tagName[1]), text: el.textContent?.trim() }))
    );
    
    console.log(`  Heading structure:`);
    headings.forEach(h => {
      console.log(`    ${'  '.repeat(h.level - 1)}H${h.level}: ${h.text?.substring(0, 50)}`);
    });
    
    // Should have at least one H1
    const h1Count = headings.filter(h => h.level === 1).length;
    expect(h1Count).toBeGreaterThan(0);
    console.log(`  ✓ Has H1 heading(s)`);
    
    // Check for alt text on images
    const images = await page.locator('img').evaluateAll(imgs => 
      imgs.map(img => ({ src: img.src, alt: img.alt }))
    );
    
    if (images.length > 0) {
      const imagesWithoutAlt = images.filter(img => !img.alt);
      console.log(`  Images: ${images.length} total, ${imagesWithoutAlt.length} without alt text`);
      
      if (imagesWithoutAlt.length > 0) {
        console.log(`  Images without alt text:`);
        imagesWithoutAlt.forEach(img => {
          console.log(`    ${img.src.split('/').pop()}`);
        });
      }
      
      expect(imagesWithoutAlt.length).toBe(0);
      console.log(`  ✓ All images have alt text`);
    }
    
    // Check for lang attribute
    const htmlLang = await page.getAttribute('html', 'lang');
    expect(htmlLang).toBeTruthy();
    console.log(`  ✓ Language declared: ${htmlLang}`);
  });

  test('keyboard navigation works', { 
    tag: ['@a11y', '@keyboard'] 
  }, async ({ page }) => {
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('domcontentloaded');
    
    // Get all focusable elements
    const focusableElements = await page.evaluateAll(
      'a[href], button, input, select, textarea, [tabindex]:not([tabindex="-1"])',
      elements => elements.length
    );
    
    console.log(`  Focusable elements found: ${focusableElements}`);
    expect(focusableElements).toBeGreaterThan(0);
    
    // Test tab navigation
    await page.keyboard.press('Tab');
    const firstFocusedElement = await page.evaluate(() => {
      const el = document.activeElement;
      return { 
        tag: el?.tagName, 
        text: el?.textContent?.trim().substring(0, 50),
        hasVisibleFocus: window.getComputedStyle(el).outline !== 'none'
      };
    });
    
    console.log(`  First tab focus: ${firstFocusedElement.tag} - "${firstFocusedElement.text}"`);
    console.log(`  Focus indicator visible: ${firstFocusedElement.hasVisibleFocus ? '✓' : '✗'}`);
    
    expect(firstFocusedElement.tag).toBeTruthy();
    console.log(`  ✓ Keyboard navigation works`);
  });

  test('color contrast is sufficient', { 
    tag: ['@a11y', '@wcag', '@contrast'] 
  }, async ({ page }) => {
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('domcontentloaded');
    
    // Run focused scan on color contrast
    const contrastResults = await new AxeBuilder({ page })
      .withTags(['wcag2aa'])
      .include('body')
      .analyze();
    
    const contrastViolations = contrastResults.violations.filter(v => 
      v.id === 'color-contrast'
    );
    
    if (contrastViolations.length > 0) {
      console.log('  Color contrast violations:');
      contrastViolations.forEach(violation => {
        violation.nodes.forEach(node => {
          console.log(`    - ${node.html.substring(0, 60)}...`);
        });
      });
    }
    
    expect(contrastViolations.length).toBe(0);
    console.log('  ✓ Color contrast meets WCAG AA standards');
  });

  test('form elements have proper labels', { 
    tag: ['@a11y', '@forms'] 
  }, async ({ page }) => {
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('domcontentloaded');
    
    // Check if there are form elements
    const formElements = await page.locator('input, select, textarea').count();
    
    if (formElements > 0) {
      console.log(`  Form elements found: ${formElements}`);
      
      // Run focused scan on form labels
      const labelResults = await new AxeBuilder({ page })
        .withRules(['label', 'label-title-only'])
        .analyze();
      
      const labelViolations = labelResults.violations;
      
      if (labelViolations.length > 0) {
        console.log('  Form label violations:');
        labelViolations.forEach(violation => {
          console.log(`    ${violation.id}: ${violation.description}`);
        });
      }
      
      expect(labelViolations.length).toBe(0);
      console.log('  ✓ All form elements properly labeled');
    } else {
      console.log('  No form elements on this page');
    }
  });

  test('ARIA attributes are used correctly', { 
    tag: ['@a11y', '@aria'] 
  }, async ({ page }) => {
    await page.goto('https://elamcb.github.io');
    await page.waitForLoadState('domcontentloaded');
    
    // Run ARIA-specific checks
    const ariaResults = await new AxeBuilder({ page })
      .withTags(['best-practice'])
      .include('body')
      .analyze();
    
    const ariaViolations = ariaResults.violations.filter(v => 
      v.id.includes('aria')
    );
    
    if (ariaViolations.length > 0) {
      console.log('  ARIA violations:');
      ariaViolations.forEach(violation => {
        console.log(`    ${violation.id}: ${violation.description}`);
      });
    }
    
    expect(ariaViolations.length).toBe(0);
    console.log('  ✓ ARIA attributes used correctly');
  });
});

