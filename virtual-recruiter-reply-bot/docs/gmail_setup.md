# Gmail API Setup Guide

This guide will help you set up Gmail API access for the AI Recruiter Agent.

## Step 1: Enable Gmail API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)

2. Create a new project (or select an existing one)
   - Click on the project dropdown at the top
   - Click "New Project"
   - Name it "AI Recruiter Agent"
   - Click "Create"

3. Enable the Gmail API
   - In the left sidebar, go to **APIs & Services > Library**
   - Search for "Gmail API"
   - Click on "Gmail API"
   - Click "Enable"

## Step 2: Create OAuth 2.0 Credentials

1. Go to **APIs & Services > Credentials**

2. Click **+ Create Credentials** at the top

3. Select **OAuth client ID**

4. If prompted, configure the OAuth consent screen:
   - Click **Configure Consent Screen**
   - Choose **External** (unless you have a Google Workspace)
   - Fill in:
     - App name: "AI Recruiter Agent"
     - User support email: Your email
     - Developer contact: Your email
   - Click **Save and Continue**
   - Skip "Scopes" for now (click **Save and Continue**)
   - Add your email as a test user
   - Click **Save and Continue**

5. Back to creating credentials:
   - Application type: **Desktop app**
   - Name: "AI Recruiter Agent Desktop"
   - Click **Create**

6. Download the credentials:
   - Click **Download JSON**
   - Save the file as `gmail_credentials.json`

## Step 3: Place Credentials in Project

1. Create a `credentials` folder in your project:
   ```bash
   mkdir ai-recruiter-agent/credentials
   ```

2. Move the downloaded file:
   ```bash
   mv ~/Downloads/client_secret_*.json ai-recruiter-agent/credentials/gmail_credentials.json
   ```

## Step 4: First Time Authentication

1. Run the agent for the first time:
   ```bash
   cd ai-recruiter-agent
   python main.py --once
   ```

2. A browser window will open asking you to sign in

3. Sign in with your Gmail account

4. Click **Allow** when asked for permissions

5. The token will be saved to `credentials/gmail_token.json`

## Step 5: Verify Setup

Run the email agent test:

```bash
python agents/email_agent.py
```

You should see a list of recent emails (if any).

## Troubleshooting

### "The file gmail_credentials.json was not found"

Make sure the file is in the correct location:
```
ai-recruiter-agent/
├── credentials/
│   └── gmail_credentials.json
```

### "Access blocked: This app's request is invalid"

You need to add your email as a test user in the OAuth consent screen:
1. Go to **APIs & Services > OAuth consent screen**
2. Under "Test users", click **Add Users**
3. Add your Gmail address
4. Try authenticating again

### "insufficient permissions"

The Gmail API needs the correct scope. Make sure you're requesting:
- `https://www.googleapis.com/auth/gmail.modify`

Delete `credentials/gmail_token.json` and authenticate again.

## Security Notes

⚠️ **Important:**
- Never commit `gmail_credentials.json` or `gmail_token.json` to version control
- Keep these files secure - they provide access to your Gmail
- The `.gitignore` file is configured to exclude the `credentials/` folder

## Gmail API Quotas (Free Tier)

Google provides generous free quotas:
- 1 billion quota units per day
- Reading an email: ~5 units
- Sending an email: ~100 units

This means you can:
- Read ~200 million emails per day
- Send ~10 million emails per day

**More than enough for job hunting!**

## App Password Alternative (Less Recommended)

If you don't want to use OAuth, you can use an App Password:

1. Enable 2-factor authentication on your Google account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate an app password
4. Use IMAP/SMTP instead of Gmail API

However, OAuth is recommended because:
- More secure
- Better error handling
- More features available
- No need to enable "less secure apps"

