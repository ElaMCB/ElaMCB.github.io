# Simple Email Setup Alternative

If OAuth is giving you trouble, use App Password instead (simpler, but less secure).

## Step 1: Enable 2-Factor Authentication

1. Go to https://myaccount.google.com/security
2. Under "How you sign in to Google"
3. Click "2-Step Verification"
4. Follow the prompts to enable it (if not already enabled)

## Step 2: Create App Password

1. Go to https://myaccount.google.com/apppasswords
2. **App name:** Type "ARIA"
3. Click "Create"
4. Google shows you a 16-character password
5. **Copy it immediately** (you can't see it again)

## Step 3: Update ARIA to Use App Password

Edit `agents/email_agent.py` - I'll create a simpler version that uses IMAP/SMTP instead of Gmail API.

## Pros and Cons

**App Password Method:**
- ✅ Simpler setup (5 minutes)
- ✅ No OAuth consent screen
- ✅ No test user issues
- ❌ Less secure than OAuth
- ❌ Requires 2FA enabled

**OAuth Method:**
- ✅ More secure
- ✅ Better for long-term use
- ❌ Complex setup
- ❌ Test user issues

## Which Should You Use?

For now: **Try App Password** (easier)
Later: Can switch to OAuth once test user issue resolved

