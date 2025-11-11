# Test Plan: Portfolio Website Quality Assurance

## 📋 Document Information

| Field | Value |
|-------|-------|
| **Project** | ElaMCB Portfolio Website |
| **URL** | https://elamcb.github.io |
| **Version** | 1.0 |
| **Author** | Ela MCB |
| **Last Updated** | November 2025 |
| **Status** | Active |

---

## 1. Executive Summary

This test plan outlines the quality assurance strategy for the ElaMCB portfolio website. The testing approach encompasses functional, performance, visual, and accessibility testing using modern automation frameworks to ensure a high-quality user experience across all devices and browsers.

### Key Objectives
- ✅ Ensure 100% critical functionality works correctly
- ✅ Meet Google Core Web Vitals standards
- ✅ Achieve WCAG 2.1 Level AA accessibility compliance
- ✅ Maintain visual consistency across devices
- ✅ Provide fast, reliable user experience

---

## 2. Scope

### 2.1 In Scope

**Functional Testing:**
- Homepage content and layout
- Navigation links (internal and external)
- Project showcase pages
- Social media links
- Contact information
- Responsive design (mobile, tablet, desktop)

**Performance Testing:**
- Page load times
- Core Web Vitals (LCP, FCP, CLS, TTFB)
- Resource loading optimization
- Time to Interactive (TTI)

**Visual Testing:**
- Cross-browser rendering
- Responsive design breakpoints
- Dark mode implementation
- Print styles
- Component-level consistency

**Accessibility Testing:**
- WCAG 2.1 Level A compliance
- WCAG 2.1 Level AA compliance
- Keyboard navigation
- Screen reader compatibility
- Color contrast ratios
- ARIA attributes

### 2.2 Out of Scope

- Backend API testing (static site)
- Load/stress testing (GitHub Pages handles this)
- Security penetration testing
- Payment processing (not applicable)
- Database testing (not applicable)

---

## 3. Test Strategy

### 3.1 Testing Approach

**Test Pyramid:**
```
           /\
          /  \  E2E Tests (Playwright)
         /____\
        /      \ Integration Tests
       /________\
      /          \ Unit Tests (Future)
     /____________\
```

**Current Focus:** E2E and Integration testing with Playwright

### 3.2 Test Levels

#### 3.2.1 Smoke Testing
**Frequency:** Before every commit, after every deployment  
**Duration:** ~30 seconds  
**Coverage:** Critical user paths

**Tests:**
- Homepage loads successfully
- Critical content visible
- Main navigation functional
- Social links present

**Command:** `npm run test:smoke`

#### 3.2.2 Functional Testing
**Frequency:** Daily, on every PR  
**Duration:** ~2 minutes  
**Coverage:** All user-facing features

**Tests:**
- All navigation links work
- Project links navigate correctly
- Social media links valid
- External links open properly
- Content loads correctly

**Command:** `npm run test:fast`

#### 3.2.3 Performance Testing
**Frequency:** Weekly, before major releases  
**Duration:** ~3 minutes  
**Coverage:** Performance metrics and Core Web Vitals

**Tests:**
- LCP < 2.5 seconds
- FCP < 1.8 seconds
- CLS < 0.1
- TTFB < 600ms
- Total page load < 3 seconds
- Resource count and size analysis

**Command:** `npm run test:performance`

**Acceptance Criteria:**
- ✅ All Core Web Vitals in "Good" range (Google standards)
- ✅ Page load under 3 seconds on 4G connection
- ✅ Total page size under 2MB

#### 3.2.4 Visual Regression Testing
**Frequency:** Before releases, when UI changes  
**Duration:** ~5 minutes  
**Coverage:** UI consistency across devices

**Tests:**
- Desktop view (1280x720)
- Tablet view (768x1024)
- Mobile view (375x667)
- Dark mode rendering
- Print layout
- Component-level screenshots

**Command:** `npm run test:visual`

**Baseline Management:**
- Update baselines after approved UI changes
- Store baselines in version control
- Review diffs manually before approving

#### 3.2.5 Accessibility Testing
**Frequency:** Weekly, before releases  
**Duration:** ~2 minutes  
**Coverage:** WCAG 2.1 compliance

**Tests:**
- Automated WCAG 2.1 Level A & AA scans
- Keyboard navigation (Tab, Enter, Escape)
- Focus indicators visible
- Color contrast ≥ 4.5:1 for normal text
- Color contrast ≥ 3:1 for large text
- Alt text on all images
- Proper heading hierarchy
- Form labels (if applicable)
- ARIA attributes correct

**Command:** `npm run test:a11y`

**Compliance Target:** WCAG 2.1 Level AA

---

## 4. Test Environment

### 4.1 Browsers

**Primary (Automated):**
- ✅ Chromium 120+ (Desktop Chrome)

**Secondary (Manual/Future):**
- Firefox 120+
- Safari 17+
- Edge 120+

**Mobile Browsers:**
- Chrome Mobile (Android)
- Safari Mobile (iOS)

### 4.2 Devices

**Viewports Tested:**
- 📱 Mobile: 375x667 (iPhone SE)
- 📱 Tablet: 768x1024 (iPad)
- 💻 Desktop: 1280x720 (Standard)
- 💻 Large Desktop: 1920x1080 (Full HD)

### 4.3 Testing Infrastructure

**Local Development:**
- OS: Windows 10/11, macOS, Linux
- Node.js: 18+
- Playwright: 1.56+

**CI/CD:**
- Platform: GitHub Actions
- OS: Ubuntu Latest
- Trigger: Push to main, Pull Requests
- Reporting: HTML report emailed after each run

---

## 5. Test Cases

### 5.1 Test Case Categories

| Category | Test Cases | Priority | Automation Status |
|----------|-----------|----------|-------------------|
| Smoke Tests | 4 | Critical | ✅ Automated |
| Navigation | 3 | High | ✅ Automated |
| Performance | 3 | High | ✅ Automated |
| Visual Regression | 7 | Medium | ✅ Automated |
| Accessibility | 6 | High | ✅ Automated |
| Responsive Design | 3 | Medium | ✅ Automated |

**Total:** 26+ automated test cases

### 5.2 Sample Test Cases

#### TC-001: Homepage Load (Smoke)
**Priority:** Critical  
**Tag:** @smoke, @critical, @fast  
**Preconditions:** None  
**Steps:**
1. Navigate to https://elamcb.github.io
2. Wait for DOM content loaded
3. Verify page title contains "Ela MCB"
4. Verify "AI Projects" heading is visible
5. Verify "Research" heading is visible

**Expected Result:** All verifications pass  
**Actual Result:** ✅ Pass  
**Automation:** `tests/portfolio.spec.js`

#### TC-002: Navigation Links (Functional)
**Priority:** High  
**Tag:** @links, @fast  
**Preconditions:** Homepage loaded  
**Steps:**
1. Extract all navigation links
2. Filter internal portfolio links
3. Navigate to each link
4. Verify HTTP status < 400
5. Verify page loads successfully

**Expected Result:** All links return valid responses  
**Actual Result:** ✅ Pass  
**Automation:** `tests/navigation-links.spec.js`

#### TC-003: Core Web Vitals (Performance)
**Priority:** High  
**Tag:** @performance, @metrics  
**Preconditions:** None  
**Steps:**
1. Navigate to homepage
2. Collect performance metrics
3. Measure LCP, FCP, CLS, TTFB
4. Assert LCP < 2500ms
5. Assert FCP < 1800ms
6. Assert CLS < 0.1
7. Assert TTFB < 600ms

**Expected Result:** All metrics within Google "Good" thresholds  
**Actual Result:** ✅ Pass  
**Automation:** `tests/performance.spec.js`

#### TC-004: Mobile Responsive (Visual)
**Priority:** Medium  
**Tag:** @visual, @responsive, @mobile  
**Preconditions:** Baseline screenshot exists  
**Steps:**
1. Set viewport to 375x667 (iPhone SE)
2. Navigate to homepage
3. Wait for content loaded
4. Capture full page screenshot
5. Compare with baseline

**Expected Result:** No visual regressions detected  
**Actual Result:** ✅ Pass  
**Automation:** `tests/visual-regression.spec.js`

#### TC-005: WCAG Compliance (Accessibility)
**Priority:** High  
**Tag:** @a11y, @critical, @wcag  
**Preconditions:** None  
**Steps:**
1. Navigate to homepage
2. Run axe-core accessibility scan
3. Filter WCAG 2.1 Level A & AA rules
4. Check for violations
5. Assert zero violations

**Expected Result:** No WCAG violations found  
**Actual Result:** ✅ Pass  
**Automation:** `tests/accessibility.spec.js`

#### TC-006: Keyboard Navigation (Accessibility)
**Priority:** High  
**Tag:** @a11y, @keyboard  
**Preconditions:** Homepage loaded  
**Steps:**
1. Identify all focusable elements
2. Press Tab key
3. Verify focus moves to first element
4. Verify focus indicator visible
5. Continue tabbing through all elements
6. Verify logical tab order

**Expected Result:** Keyboard navigation works, focus visible  
**Actual Result:** ✅ Pass  
**Automation:** `tests/accessibility.spec.js`

---

## 6. Test Data

### 6.1 Test URLs

**Primary:**
- Homepage: `https://elamcb.github.io`

**Project Pages:**
- LLM Guardian: `https://elamcb.github.io/llm-guardian/`
- Research: `https://elamcb.github.io/research/`
- Job Search Automation: `https://elamcb.github.io/job-search-automation/`
- AI IDE Comparison: `https://elamcb.github.io/ai-ide-comparison/`

**Social Links:**
- LinkedIn: Pattern `/linkedin\.com/i`
- GitHub: Pattern `/github\.com/i`

### 6.2 Test Credentials

N/A - Public website, no authentication required

---

## 7. Entry and Exit Criteria

### 7.1 Entry Criteria

**Before Testing Begins:**
- ✅ Test environment set up (Playwright installed)
- ✅ Test data prepared (URLs, baseline images)
- ✅ Test cases documented
- ✅ Automation framework ready
- ✅ CI/CD pipeline configured

### 7.2 Exit Criteria

**Before Release:**
- ✅ All critical tests passing (100%)
- ✅ All high-priority tests passing (95%+)
- ✅ No critical defects open
- ✅ Performance metrics within thresholds
- ✅ Accessibility compliance verified
- ✅ Visual regressions reviewed and approved
- ✅ Test report generated and reviewed

---

## 8. Defect Management

### 8.1 Defect Severity

**Critical (P0):**
- Site completely inaccessible
- Major functionality broken
- Security vulnerabilities

**High (P1):**
- Navigation broken
- Core features not working
- Major accessibility violations

**Medium (P2):**
- Minor functionality issues
- Visual inconsistencies
- Performance degradation

**Low (P3):**
- Cosmetic issues
- Minor text errors
- Enhancement requests

### 8.2 Defect Lifecycle

1. **New** - Bug discovered and logged
2. **Open** - Bug acknowledged, assigned
3. **In Progress** - Developer working on fix
4. **Ready for Test** - Fix deployed, ready to verify
5. **Closed** - Fix verified, test passing
6. **Reopened** - Issue persists, needs more work

### 8.3 Defect Tracking

**Current:** GitHub Issues  
**Labels:** `bug`, `critical`, `accessibility`, `performance`, `visual`

---

## 9. Test Schedule

### 9.1 Continuous Testing

**On Every Commit:**
```bash
npm run test:smoke  # 30 seconds
```

**On Every Pull Request:**
```bash
npm run test:fast   # 2 minutes
```

**On Push to Main:**
```bash
npm test            # Full suite via GitHub Actions
```

### 9.2 Scheduled Testing

**Daily:** 
- Smoke tests (automated via CI)

**Weekly:**
- Full regression suite
- Performance testing
- Accessibility audit
- Visual regression review

**Before Major Release:**
- Complete test suite
- Manual exploratory testing
- Cross-browser testing
- Performance benchmarking

---

## 10. Risks and Mitigations

### 10.1 Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| External link breakage | Medium | Low | Regular link validation, monitoring |
| Performance degradation | Low | High | Automated performance testing, budgets |
| Accessibility regression | Medium | High | Automated WCAG testing, manual review |
| Visual inconsistencies | Medium | Medium | Visual regression testing, approval process |
| Test flakiness | Medium | Medium | Smart retries, explicit waits, stable selectors |
| CI/CD failures | Low | Medium | Local testing first, CI optimization |

### 10.2 Mitigation Strategies

**For Test Flakiness:**
- Use explicit waits instead of arbitrary delays
- Implement smart retry logic (1 local, 2 in CI)
- Use stable selectors (role-based, data-testid)
- Run tests in isolated contexts

**For Performance:**
- Set performance budgets
- Monitor Core Web Vitals trends
- Optimize images and assets
- Use lazy loading

**For Accessibility:**
- Run automated scans on every change
- Manual keyboard navigation testing
- Screen reader testing for critical flows

---

## 11. Test Metrics and Reporting

### 11.1 Key Metrics

**Test Execution:**
- Total test cases: 26+
- Pass rate target: 95%+
- Execution time: < 10 minutes (full suite)
- Smoke test time: < 30 seconds

**Quality Metrics:**
- Core Web Vitals: All "Good" (Green)
- Accessibility violations: 0
- Visual regressions: 0 unapproved
- Broken links: 0

**Performance Metrics:**
- LCP: < 2.5s (Target: < 2.0s)
- FCP: < 1.8s (Target: < 1.5s)
- CLS: < 0.1 (Target: < 0.05)
- TTFB: < 600ms (Target: < 400ms)

### 11.2 Reports Generated

**After Each Test Run:**
1. **HTML Report** - Interactive web report
   - Test results and statistics
   - Screenshots and videos
   - Trace viewer for debugging
   - Filtering and search

2. **JSON Report** - Machine-readable results
   - Location: `test-results/results.json`
   - Used for: CI/CD integration, metrics tracking

3. **Email Report** (CI only)
   - Sent to: Configured recipient
   - Contains: ZIP of HTML report
   - Frequency: Every CI run

**Commands:**
```bash
npm run test:report  # Open HTML report
```

### 11.3 Success Criteria

**Weekly Success Metrics:**
- ✅ 95%+ test pass rate
- ✅ All critical tests passing
- ✅ Core Web Vitals in "Good" range
- ✅ Zero WCAG violations
- ✅ < 5 minute average test execution

---

## 12. Tools and Technologies

### 12.1 Test Automation

**Framework:** Playwright 1.56+
- Cross-browser support
- Auto-wait mechanisms
- Powerful selectors
- Video and trace recording

**Accessibility:** @axe-core/playwright 4.10+
- WCAG 2.1 compliance testing
- Automated violation detection
- Best practices validation

### 12.2 CI/CD

**Platform:** GitHub Actions
- Workflow: `.github/workflows/playwright-tests.yml`
- Triggers: Push, PR, Manual
- Artifacts: 30-day retention

**Email Reporting:** dawidd6/action-send-mail@v3
- Automatic report delivery
- ZIP attachment with HTML report

### 12.3 Version Control

**Repository:** GitHub
- Test code: `tests/` directory
- Configuration: `playwright.config.js`
- Documentation: Multiple MD files

---

## 13. Test Deliverables

### 13.1 Documentation

- ✅ Test Plan (this document)
- ✅ Test Suite README (`tests/README.md`)
- ✅ Quick Reference Guide (`tests/QUICK_REFERENCE.md`)
- ✅ Setup Guide (`PLAYWRIGHT_SETUP_GUIDE.md`)
- ✅ Optimization Summary (`PLAYWRIGHT_OPTIMIZATIONS_SUMMARY.md`)

### 13.2 Test Artifacts

- ✅ Test scripts (26+ test cases)
- ✅ Page Object Models
- ✅ Custom fixtures
- ✅ Configuration files
- ✅ Visual regression baselines
- ✅ CI/CD workflow

### 13.3 Reports

- ✅ HTML test reports
- ✅ JSON results
- ✅ Performance metrics
- ✅ Accessibility audit results
- ✅ Visual regression comparisons

---

## 14. Maintenance and Updates

### 14.1 Test Maintenance

**Regular Updates:**
- Review and update test cases monthly
- Update visual baselines after approved UI changes
- Refresh dependencies quarterly
- Review and update test plan quarterly

**Triggered Updates:**
- New features: Add test coverage
- Bug fixes: Add regression tests
- UI changes: Update baselines and selectors
- Performance issues: Add/update performance tests

### 14.2 Continuous Improvement

**Monthly:**
- Review test execution metrics
- Identify and fix flaky tests
- Optimize slow-running tests
- Update documentation

**Quarterly:**
- Review test coverage
- Assess automation ROI
- Plan new test scenarios
- Update tools and frameworks

---

## 15. Approval and Sign-off

### 15.1 Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test Plan Author | Ela MCB | ✅ | November 2025 |
| Project Owner | Ela MCB | ✅ | November 2025 |

### 15.2 Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | November 2025 | Ela MCB | Initial test plan creation |

---

## 16. References

### 16.1 Documentation

- [Playwright Documentation](https://playwright.dev)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Web Vitals](https://web.dev/vitals/)
- [Axe Accessibility Testing](https://github.com/dequelabs/axe-core)

### 16.2 Project Documentation

- Repository: https://github.com/ElaMCB/ElaMCB.github.io
- Website: https://elamcb.github.io

---

## 17. Contact Information

**Project Owner & QA Lead:** Ela MCB  
**Repository:** https://github.com/ElaMCB/ElaMCB.github.io  
**Issues:** https://github.com/ElaMCB/ElaMCB.github.io/issues

---

## Appendix A: Test Commands Quick Reference

```bash
# Installation
npm install
npx playwright install --with-deps

# Run Tests
npm test                    # All tests
npm run test:smoke          # Smoke tests
npm run test:fast           # Fast tests
npm run test:critical       # Critical tests
npm run test:performance    # Performance tests
npm run test:visual         # Visual regression
npm run test:a11y           # Accessibility tests

# Interactive Testing
npm run test:ui             # UI mode
npm run test:headed         # Headed mode
npm run test:debug          # Debug mode

# Reporting
npm run test:report         # Open HTML report

# Visual Regression
npm run test:update-snapshots  # Update baselines
```

---

**Document Version:** 1.0  
**Last Updated:** November 2025  
**Status:** Active and Maintained ✅

