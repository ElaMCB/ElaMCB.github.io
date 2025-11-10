# Quick Start Guide

Get your AI Recruiter Agent up and running in 15 minutes!

## Prerequisites

- Python 3.9 or higher
- Gmail account
- ~10GB free disk space (for Ollama)

## Installation Steps

### 1. Clone/Download the Project

```bash
cd ai-recruiter-agent
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama (Free Local LLM)

**Windows:**
- Download from [ollama.ai/download](https://ollama.ai/download)
- Run the installer

**macOS/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Pull a model:**
```bash
ollama pull llama2
```

See [docs/ollama_setup.md](ollama_setup.md) for detailed instructions.

### 4. Setup Gmail API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials as `credentials/gmail_credentials.json`

See [docs/gmail_setup.md](gmail_setup.md) for detailed instructions.

### 5. Configure Your Profile

1. Copy the environment file:
   ```bash
   cp env.example .env
   ```

2. Edit `.env` and update:
   ```bash
   EMAIL_ADDRESS=your.email@gmail.com
   ```

3. Edit `config/profile.yaml` with your information:
   - Name and title
   - Skills and experience
   - Salary expectations
   - Work preferences
   - Job criteria

### 6. First Run & Authentication

```bash
python main.py --setup-check
```

This will:
- Verify all requirements
- Open a browser for Gmail authentication
- Test Ollama connection
- Check configuration

Follow the browser prompts to authorize Gmail access.

### 7. Test Run

```bash
python main.py --once
```

The agent will:
- Check for new recruiter emails
- Process and respond to them
- Show you a status report

## Usage Modes

### Single Check (Default)

Process messages once and exit:

```bash
python main.py --once
```

### Daemon Mode (Continuous)

Run in background and check periodically:

```bash
python main.py --daemon --interval 300
```

Checks every 300 seconds (5 minutes). Press Ctrl+C to stop.

### Interactive Mode

Interactive shell with commands:

```bash
python main.py --interactive
```

Commands:
- `check` - Check for new messages
- `status` - Show status report
- `list` - List all conversations
- `view <thread_id>` - View conversation details
- `quit` - Exit

## Your First Recruiter Message

When a recruiter emails you:

1. **The agent detects it** - Identifies recruiter keywords
2. **Extracts information** - Company, position, salary, etc.
3. **Generates response** - Using your profile and LLM
4. **Sends reply** - Professional, personalized message
5. **Tracks conversation** - Maintains context for follow-ups

## Example Workflow

```bash
# Morning: Check messages
python main.py --once

# Output:
# ✓ Processed 2 message(s)
# 
# Active Conversations: 3
# By Stage:
#   initial_contact: 1
#   information_gathering: 2
```

## Monitoring Conversations

View all active conversations:

```bash
python main.py --interactive
> list
```

View specific conversation:

```bash
> view <thread_id>
```

## Customization

### Adjust Response Tone

Edit `config/prompts.yaml`:
- Change system prompts
- Modify email/SMS templates
- Adjust conversation stages

### Adjust Auto-Reply Behavior

Edit `.env`:
```bash
# Disable auto-reply (just log messages)
AUTO_REPLY_ENABLED=false

# Require manual approval before sending
REQUIRE_APPROVAL=true
```

### Adjust Job Criteria

Edit `config/profile.yaml`:
```yaml
job_criteria:
  must_have:
    - title_contains: ["senior", "architect", "lead"]
    - remote_option: true
  
  auto_decline:
    - salary_below: 100000
```

## Logs and Data

### Conversation Logs

All conversations saved to:
```
data/conversations.db
logs/conversations/<thread_id>.log
```

### Activity Logs

Agent activity logged to:
```
logs/agent.log
```

### Escalations

Important conversations requiring your attention:
```
logs/escalations.log
```

## SMS Support (Optional)

To handle SMS from recruiters:

1. **Find out recruiter's carrier** (AT&T, Verizon, etc.)

2. **Reply via email-to-SMS gateway:**
   ```python
   # The agent does this automatically
   # Just need to set default carrier in .env
   SMS_EMAIL_GATEWAY=@txt.att.net
   ```

3. **Supported carriers:**
   - AT&T: `@txt.att.net`
   - T-Mobile: `@tmomail.net`
   - Verizon: `@vtext.com`
   - Sprint: `@messaging.sprintpcs.com`

See [docs/sms_setup.md](sms_setup.md) for details.

## Safety Features

### Escalation Triggers

Agent will alert you for:
- Salary negotiation
- Final offers
- Interview scheduling
- Unclear requirements

### Opt-Out Support

Automatically handles:
- "STOP" keyword (unsubscribe)
- Spam detection
- Blacklist support

### Review Mode

Enable `REQUIRE_APPROVAL=true` to review all responses before sending.

## Common Issues

### "Gmail credentials not found"

Place `gmail_credentials.json` in `credentials/` folder.

### "Ollama connection refused"

Start Ollama: `ollama serve`

### "Model not found"

Pull the model: `ollama pull llama2`

### Slow responses

Use a smaller model: `ollama pull phi` and set `OLLAMA_MODEL=phi`

## What's Next?

1. **Test with real emails** - Let it handle a few recruiter messages
2. **Refine prompts** - Adjust tone and responses to your style
3. **Monitor results** - Check conversation logs daily
4. **Enable daemon mode** - Set and forget
5. **Add voice (optional)** - Integrate Twilio for calls

## Pro Tips

💡 **Start conservative:** Use `REQUIRE_APPROVAL=true` initially

💡 **Check logs daily:** Review `logs/agent.log` and escalations

💡 **Keep profile updated:** Update salary expectations and criteria

💡 **Use labels:** Agent adds "AI-Recruiter/Processed" label to handled emails

💡 **Test responses:** Use `--once` mode before enabling `--daemon`

## Getting Help

- Check `README.md` for detailed architecture
- Review `docs/` folder for setup guides
- Check logs in `logs/` for errors
- GitHub issues (if applicable)

---

**Ready to automate your job search?** 🚀

```bash
python main.py --daemon
```

Let the AI handle the initial conversations while you focus on the final interviews!

