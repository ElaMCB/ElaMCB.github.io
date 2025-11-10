# ARIA Complete Setup Guide

You're almost ready to have ARIA automatically respond to recruiters! Here's what we've done and what's next.

## ✅ Step 1: Ollama Installed (COMPLETE!)

```
✓ Ollama installed
✓ Llama2 model downloaded (3.8 GB)
✓ Free local LLM ready to use
```

---

## 🔧 Step 2: Gmail API Setup (15 minutes)

This is the ONLY complex part. Follow carefully:

### 2.1 Go to Google Cloud Console

Visit: https://console.cloud.google.com/

### 2.2 Create a Project

1. Click the project dropdown at the top
2. Click "**New Project**"
3. Name: `ARIA Recruiter Agent`
4. Click "**Create**"
5. Wait 30 seconds for it to create

### 2.3 Enable Gmail API

1. In the left sidebar: **APIs & Services** → **Library**
2. Search for: `Gmail API`
3. Click on "**Gmail API**"
4. Click "**Enable**"

### 2.4 Configure OAuth Consent Screen

1. Go to: **APIs & Services** → **OAuth consent screen**
2. Choose: **External** (unless you have Google Workspace)
3. Click "**Create**"

4. Fill in:
   - **App name:** `ARIA`
   - **User support email:** Your Gmail address
   - **Developer contact:** Your Gmail address
5. Click "**Save and Continue**"

6. **Scopes** page: Click "**Save and Continue**" (skip it)

7. **Test users** page:
   - Click "**Add Users**"
   - Add your Gmail address
   - Click "**Save and Continue**"

8. Click "**Back to Dashboard**"

### 2.5 Create OAuth Credentials

1. Go to: **APIs & Services** → **Credentials**
2. Click "**+ Create Credentials**" at top
3. Select: **OAuth client ID**
4. Application type: **Desktop app**
5. Name: `ARIA Desktop`
6. Click "**Create**"

### 2.6 Download Credentials

1. You'll see a dialog with your credentials
2. Click "**Download JSON**"
3. Save the file (it will be named like `client_secret_xxx.json`)

### 2.7 Place Credentials

Move the downloaded file to ARIA:

```powershell
# Create credentials folder
mkdir C:\Users\elena\OneDrive\Documents\GitHub\ElaMCB.github.io\virtual-recruiter-reply-bot\credentials

# Move the file (adjust the path to where you downloaded it)
Move-Item ~\Downloads\client_secret_*.json C:\Users\elena\OneDrive\Documents\GitHub\ElaMCB.github.io\virtual-recruiter-reply-bot\credentials\gmail_credentials.json
```

---

## ⚙️ Step 3: Configure ARIA

### 3.1 Create .env file

```powershell
cd C:\Users\elena\OneDrive\Documents\GitHub\ElaMCB.github.io\virtual-recruiter-reply-bot
Copy-Item env.example .env
```

### 3.2 Edit .env (Optional - defaults work fine)

The defaults are already configured! But you can customize:

```bash
# Email Configuration
EMAIL_ADDRESS=your.email@gmail.com

# LLM Configuration (already set to use Ollama)
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama2

# Agent Configuration
CHECK_INTERVAL_SECONDS=300  # Check every 5 minutes
AUTO_REPLY_ENABLED=true
```

### 3.3 Update Your Profile

Edit `config/profile.yaml` with YOUR actual details:
- Your zip code
- Your actual years of experience
- Your actual skills
- Update the $65-75/hr rate if needed

---

## 🚀 Step 4: First Run & Gmail Authentication

```powershell
cd C:\Users\elena\OneDrive\Documents\GitHub\ElaMCB.github.io\virtual-recruiter-reply-bot

# Install Python dependencies
pip install -r requirements.txt

# First test run (will open browser for Gmail login)
python main.py --setup-check
```

### What Happens:
1. A browser window opens
2. You sign in to Gmail
3. Google asks for permissions - Click "**Allow**"
4. ARIA saves the token for future use
5. Test completes

---

## 🎯 Step 5: Test ARIA (Once Mode)

Run ARIA once to test:

```powershell
python main.py --once
```

### What This Does:
- Checks your Gmail for recruiter emails
- Shows what it found
- Shows what responses it would send
- **Does NOT send anything** (safe!)

---

## 🔄 Step 6: Enable Daemon Mode (Auto-Pilot!)

Once you're confident, enable full automation:

```powershell
python main.py --daemon
```

### What Daemon Mode Does:

```
Every 5 minutes (configurable):
  1. Check Gmail for new recruiter emails
  2. Analyze each message
  3. Generate professional response
  4. Send reply (or escalate to you)
  5. Update conversation database
  6. Repeat forever...
```

### Stop Daemon Mode:
- Press `Ctrl+C`

---

## 📊 Step 7: Monitor ARIA

### Check Status Anytime:

```powershell
python main.py --interactive

# Then type commands:
status   # Show all conversations
list     # List active conversations
view <thread_id>   # View specific conversation
quit     # Exit
```

### Check Logs:

```powershell
# Recent activity
cat logs/agent.log | Select-Object -Last 50

# Escalations (needs your attention)
cat logs/escalations.log
```

---

## 🎮 How Daemon Mode Works

```
┌─────────────────────────────────────┐
│  ARIA Running in Background         │
├─────────────────────────────────────┤
│                                     │
│  [Check Gmail] Every 5 minutes      │
│       ↓                             │
│  [New Email?]                       │
│       ↓ Yes                         │
│  [From Recruiter?]                  │
│       ↓ Yes                         │
│  [Extract Info] (company, role...)  │
│       ↓                             │
│  [Match Criteria?]                  │
│       ↓ Yes (meets $65/hr, etc.)    │
│  [Generate Response] (using Llama2) │
│       ↓                             │
│  [Important Decision?]              │
│   ├─ Yes → ESCALATE to you          │
│   └─ No  → Send auto-reply          │
│       ↓                             │
│  [Update Database]                  │
│       ↓                             │
│  [Wait 5 minutes...]                │
│       ↓                             │
│  [Repeat]                           │
└─────────────────────────────────────┘
```

---

## 🛡️ What Gets Escalated to You

ARIA will NOT auto-reply to these (you'll get notified):

- ✋ Salary negotiation discussions
- ✋ Final job offers
- ✋ Interview scheduling requests
- ✋ Technical assessment invitations
- ✋ Anything unclear/uncertain

Everything else (initial contact, info gathering, screening) → **Automated**!

---

## 💡 Pro Tips

### Run in Background (Windows)

**Option 1: New PowerShell Window**
```powershell
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\Users\elena\OneDrive\Documents\GitHub\ElaMCB.github.io\virtual-recruiter-reply-bot; python main.py --daemon"
```

**Option 2: Windows Task Scheduler** (runs at startup)
1. Open Task Scheduler
2. Create Basic Task: "ARIA Daemon"
3. Trigger: "At startup"
4. Action: Run `python`
5. Arguments: `C:\Users\elena\OneDrive\Documents\GitHub\ElaMCB.github.io\virtual-recruiter-reply-bot\main.py --daemon`

### Customize Check Interval

Edit `.env`:
```bash
CHECK_INTERVAL_SECONDS=600  # 10 minutes instead of 5
```

### Review Before Auto-Send

Edit `.env`:
```bash
REQUIRE_APPROVAL=true  # You approve each response
```

Then responses go to `data/pending_approvals.txt` for your review.

---

## 🧪 Test with Alex's Email

Once everything is set up, ARIA will automatically:

1. Detect Alex's screening questionnaire email
2. Generate the professional response we created
3. Send it (with ARIA disclosure signature)
4. Track the conversation in the database
5. Handle any follow-ups automatically

---

## ❓ Troubleshooting

### "Gmail credentials not found"
- Make sure file is at: `credentials/gmail_credentials.json`
- Check the filename exactly

### "Ollama connection refused"
- Ollama should run automatically after install
- If not: Open Ollama app from Start menu

### "Model not found"
- Run: `ollama pull llama2`

### Slow Responses
- First response is always slow (model loading)
- After that, should be 2-5 seconds per response

---

## 🎉 You're Ready!

Once you complete Gmail API setup (Step 2), you can:

1. Test with `--once` mode
2. Enable `--daemon` mode for full automation
3. Let ARIA handle Alex and all future recruiters
4. Focus on final interviews!

---

## Next Steps

1. **Now:** Complete Gmail API setup (Step 2)
2. **Then:** Run `python main.py --setup-check`
3. **Test:** Run `python main.py --once`
4. **Deploy:** Run `python main.py --daemon`
5. **Relax:** ARIA handles the rest! 🚀

Need help? Check `docs/gmail_setup.md` for detailed Gmail API instructions.

