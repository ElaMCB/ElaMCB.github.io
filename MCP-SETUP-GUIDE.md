# 🤖 MCP + Playwright Portfolio Testing Setup Guide

## What You've Got Now

✅ **Step 1 DONE**: MCP SDK installed (`@modelcontextprotocol/sdk`)  
✅ **Step 2 DONE**: MCP Playwright Server created (`mcp-playwright-server.js`)  
🔧 **Step 3 TODO**: Configure Claude Desktop (instructions below)

---

## 📋 Step 3: Configure Claude Desktop

### For Windows (Your System):

1. **Locate your Claude Desktop config file**:
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```
   
   Full path usually:
   ```
   C:\Users\elena\AppData\Roaming\Claude\claude_desktop_config.json
   ```

2. **Copy the config I created for you**:
   
   I've created `claude_desktop_config.json` in your project root. You have two options:
   
   **Option A - Copy the entire file**:
   ```powershell
   Copy-Item claude_desktop_config.json "$env:APPDATA\Claude\claude_desktop_config.json"
   ```
   
   **Option B - Manually add to existing config**:
   
   If you already have a config file with other MCP servers, just add this section:
   ```json
   {
     "mcpServers": {
       "playwright-portfolio": {
         "command": "node",
         "args": [
           "C:\\Users\\elena\\OneDrive\\Documents\\GitHub\\ElaMCB.github.io\\mcp-playwright-server.js"
         ]
       }
     }
   }
   ```

3. **Restart Claude Desktop**:
   - Completely quit Claude Desktop (right-click system tray icon → Quit)
   - Reopen Claude Desktop

4. **Verify it's working**:
   
   In Claude Desktop, look for the 🔨 (hammer) icon at the bottom of the chat.
   
   You should see: `playwright-portfolio-tester` connected!

---

## 🎮 How to Use It

Once configured, you can ask Claude Desktop (in the desktop app, not this web version) things like:

### Basic Commands:

**Run smoke test:**
```
Run my portfolio smoke test
```

**Take screenshots:**
```
Take a screenshot of my homepage
```
```
Screenshot my /llm-guardian/ page
```

**Check for broken links:**
```
Check for broken links on my portfolio
```

**Test mobile responsiveness:**
```
Test my portfolio on iPhone 13
```

**Measure performance:**
```
Measure the load time of my homepage
```

### Advanced Commands:

**Full test suite:**
```
Run all portfolio tests and show me a detailed report
```

**Visual regression testing:**
```
Take screenshots of all my main pages for visual comparison
```

**Accessibility check:**
```
Check if my portfolio is mobile-friendly and accessible
```

---

## 🛠️ Available MCP Tools

Your MCP server exposes these tools:

1. **`run_portfolio_smoke_test`** - Comprehensive smoke test
   - Checks homepage loads
   - Verifies critical sections exist
   - Tests navigation
   - Counts links

2. **`screenshot_portfolio`** - Visual testing
   - Full page or viewport screenshots
   - Any path on your site
   - Saved to `screenshots/` directory

3. **`check_broken_links`** - Link validation
   - Tests up to 20 links per page
   - Shows status codes
   - Identifies broken links

4. **`test_mobile_responsive`** - Mobile testing
   - Emulates real devices
   - Tests viewport rendering
   - Checks mobile menu

5. **`measure_performance`** - Performance metrics
   - Page load time
   - DOM metrics
   - Performance rating

---

## 🧪 Testing Locally (Without Claude Desktop)

You can also test the MCP server directly:

```bash
# Run the server (it will wait for stdin input)
node mcp-playwright-server.js
```

Then send it MCP requests via stdin (advanced usage).

**OR** use the regular Playwright test:
```bash
npx playwright test tests/portfolio.spec.js
```

---

## 🔍 Troubleshooting

### MCP server not showing up in Claude Desktop?

1. Check the config file path is correct
2. Make sure the path to `mcp-playwright-server.js` is correct
3. Verify Node.js is in your PATH: `node --version`
4. Check Claude Desktop logs:
   - Windows: `%APPDATA%\Claude\logs\`

### "Cannot find module" errors?

```bash
npm install
```

### Screenshots not saving?

Check that `screenshots/` directory exists:
```powershell
mkdir -Force screenshots
```

---

## 📊 What's Next?

### Integrate with CI/CD:

Your GitHub Actions already runs Playwright tests! You can:

1. Add screenshot comparisons (visual regression)
2. Add performance budgets
3. Run tests on multiple devices
4. Generate HTML reports

### Expand Your MCP Server:

Add more tools like:
- Accessibility testing (axe-core)
- SEO checks (meta tags, etc.)
- Performance budgets (Lighthouse)
- Visual regression (Percy, Chromatic)
- API testing for your projects

### Share Your Setup:

This is portfolio-worthy! Document your MCP + Playwright setup as a project showing:
- AI-augmented testing
- MCP protocol implementation
- Real-world automation

---

## 📚 Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Playwright Docs](https://playwright.dev/)
- [Your MCP Research Notebook](research/notebooks/mcp-software-testing.ipynb)
- [Your LLM Guardian Project](llm-guardian/README.md)

---

## ✅ Quick Checklist

- [x] MCP SDK installed
- [x] MCP server file created
- [ ] Claude Desktop configured
- [ ] Claude Desktop restarted
- [ ] MCP server showing in Claude
- [ ] Run first test!

---

**Need help?** Just ask! I'm here to debug and enhance your MCP setup. 🚀

