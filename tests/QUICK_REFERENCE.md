# Playwright Test Suite - Quick Reference Card

## 🚀 Installation (One-Time Setup)

```bash
# 1. Install dependencies
npm install

# 2. Install browsers
npx playwright install --with-deps
```

---

## ⚡ Common Commands

### Run Tests
```bash
npm test                    # All tests
npm run test:smoke          # Smoke tests (fastest)
npm run test:fast           # Fast tests only
npm run test:critical       # Critical tests
```

### View Reports
```bash
npm run test:report         # Open HTML report
```

### Interactive Testing
```bash
npm run test:ui             # UI mode (recommended for development)
npm run test:headed         # See browser
npm run test:debug          # Step-by-step debugging
```

### Specialized Tests
```bash
npm run test:performance    # Performance metrics
npm run test:visual         # Visual regression
npm run test:a11y           # Accessibility
```

### Visual Regression
```bash
npm run test:update-snapshots  # Update baseline images
```

---

## 🏷️ Test Tags

### By Speed
```bash
--grep @fast               # Quick tests
--grep @slow               # Longer tests
--grep-invert @slow        # Skip slow tests
```

### By Category
```bash
--grep @smoke              # Smoke tests
--grep @critical           # Critical features
--grep @performance        # Performance tests
--grep @visual             # Visual tests
--grep @a11y               # Accessibility tests
```

### By Device
```bash
--grep @mobile             # Mobile tests
--grep @tablet             # Tablet tests
--grep @responsive         # All responsive
```

### Combine Tags
```bash
--grep "@smoke|@critical"  # Multiple tags (OR)
--grep "@smoke.*@fast"     # Multiple tags (AND)
```

---

## 📊 What Gets Tested

### ✅ Functional
- Page loading
- Navigation
- Links
- Content visibility

### ⚡ Performance
- First Contentful Paint (< 1.8s)
- Largest Contentful Paint (< 2.5s)
- Cumulative Layout Shift (< 0.1)
- Time to First Byte (< 600ms)
- Resource loading

### 🎨 Visual
- Full page screenshots
- Mobile, tablet, desktop views
- Dark mode
- Print layout
- Component snapshots

### ♿ Accessibility
- WCAG 2.1 Level A & AA
- Keyboard navigation
- Color contrast
- ARIA attributes
- Form labels
- Heading hierarchy

---

## 🛠️ Debugging Failed Tests

### Option 1: UI Mode (Easiest)
```bash
npm run test:ui
```
- Time-travel through test
- See what Playwright sees
- Inspect at any step

### Option 2: Headed Mode
```bash
npm run test:headed
```
- Watch browser in action
- Good for visual issues

### Option 3: Debug Mode
```bash
npm run test:debug
```
- Step through line-by-line
- Pause execution
- Use DevTools

### Option 4: View Trace
```bash
npx playwright show-trace trace.zip
```
- Review failed test
- See screenshots
- Check network calls

---

## 📁 Test File Locations

```
tests/
├── portfolio.spec.js         # Smoke tests
├── navigation-links.spec.js  # Link validation  
├── performance.spec.js       # Performance metrics
├── visual-regression.spec.js # Visual testing
├── accessibility.spec.js     # A11y testing
├── fixtures-demo.spec.js     # Fixture examples
├── pages/
│   └── PortfolioPage.js      # Page Object Model
└── fixtures/
    └── portfolio-fixtures.js # Custom fixtures
```

---

## 🎯 Before Committing

```bash
# Quick check (recommended)
npm run test:smoke

# More thorough
npm run test:fast

# Full suite (if time permits)
npm test
```

---

## 🤖 CI/CD

Tests run automatically on:
- Push to main/master
- Pull requests
- Manual trigger (Actions tab)

Report emailed after each run.

---

## 📖 Full Documentation

- **`tests/README.md`** - Complete documentation
- **`PLAYWRIGHT_SETUP_GUIDE.md`** - Setup instructions
- **`PLAYWRIGHT_OPTIMIZATIONS_SUMMARY.md`** - What's optimized
- **`.github/PLAYWRIGHT_EMAIL_SETUP.md`** - Email setup

---

## 💡 Pro Tips

1. **Start with `test:ui`** - Best for development
2. **Use `test:smoke`** - Before every commit
3. **Run `test:visual` in CI** - Avoid local conflicts
4. **Tag your tests** - Enable selective running
5. **Check HTML reports** - Rich debugging info
6. **Use fixtures** - Less boilerplate

---

## 🆘 Common Issues

### Tests are slow
```bash
# Run fewer tests
npm run test:fast

# Run specific file
npx playwright test portfolio.spec.js
```

### Visual tests failing
```bash
# Update baselines
npm run test:update-snapshots
```

### Can't see what's happening
```bash
# Use UI mode
npm run test:ui

# Or headed mode
npm run test:headed
```

### Need more details
```bash
# Check HTML report
npm run test:report

# Or use debug mode
npm run test:debug
```

---

## 📞 Need Help?

1. Check `tests/README.md` for detailed docs
2. Run `npm run test:ui` to see tests visually
3. Review HTML report: `npm run test:report`
4. Check Playwright docs: https://playwright.dev

---

**Quick Start:**
```bash
npm install
npx playwright install --with-deps
npm run test:ui
```

**That's it! You're ready to test.** ✨

