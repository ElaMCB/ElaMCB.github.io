# Deployment Guide

How to run your AI Recruiter Agent 24/7 for free.

## Option 1: Local Machine (Easiest, Free)

### Windows

#### Method A: Run on Startup

1. Create a batch file `start_agent.bat`:
```batch
@echo off
cd C:\path\to\ai-recruiter-agent
python main.py --daemon --interval 300
```

2. Add to Windows Startup:
   - Press `Win + R`
   - Type `shell:startup`
   - Copy `start_agent.bat` to this folder

3. Agent starts automatically when you log in

#### Method B: Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
   - Name: "AI Recruiter Agent"
   - Trigger: At startup
   - Action: Start a program
   - Program: `python`
   - Arguments: `C:\path\to\ai-recruiter-agent\main.py --daemon`
3. Set to run whether user is logged in or not

### macOS

#### Method A: Launch Agent (Recommended)

1. Create `~/Library/LaunchAgents/com.user.recruiter-agent.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.recruiter-agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/path/to/ai-recruiter-agent/main.py</string>
        <string>--daemon</string>
        <string>--interval</string>
        <string>300</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/path/to/ai-recruiter-agent/logs/stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/ai-recruiter-agent/logs/stderr.log</string>
</dict>
</plist>
```

2. Load the agent:
```bash
launchctl load ~/Library/LaunchAgents/com.user.recruiter-agent.plist
```

3. Check status:
```bash
launchctl list | grep recruiter
```

#### Method B: Simple Background

Add to `~/.zshrc` or `~/.bash_profile`:
```bash
# Start recruiter agent on login
nohup python3 /path/to/ai-recruiter-agent/main.py --daemon &
```

### Linux

#### Method A: Systemd Service (Recommended)

1. Create `/etc/systemd/system/recruiter-agent.service`:

```ini
[Unit]
Description=AI Recruiter Response Agent
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/ai-recruiter-agent
ExecStart=/usr/bin/python3 /path/to/ai-recruiter-agent/main.py --daemon --interval 300
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

2. Enable and start:
```bash
sudo systemctl enable recruiter-agent
sudo systemctl start recruiter-agent
```

3. Check status:
```bash
sudo systemctl status recruiter-agent
```

4. View logs:
```bash
sudo journalctl -u recruiter-agent -f
```

#### Method B: Cron (Simple)

1. Edit crontab:
```bash
crontab -e
```

2. Add entry (runs every 5 minutes):
```cron
*/5 * * * * cd /path/to/ai-recruiter-agent && /usr/bin/python3 main.py --once >> logs/cron.log 2>&1
```

This runs the agent every 5 minutes instead of continuously.

## Option 2: Free Cloud (Always-On)

### Render.com (Free Tier)

**Limitations:**
- Spins down after inactivity
- Ollama might be too large for free tier
- Consider using cloud LLM API

**Setup:**

1. Create `render.yaml`:
```yaml
services:
  - type: worker
    name: recruiter-agent
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py --daemon
    envVars:
      - key: LLM_PROVIDER
        value: openai  # Use cloud API since Ollama is large
      - key: OPENAI_API_KEY
        sync: false
```

2. Push to GitHub

3. Connect to Render.com

4. Deploy

### Railway.app (Free Tier)

Similar to Render. Use `railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python main.py --daemon",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### GitHub Actions (Scheduled, Free)

**Best free option** if you don't need instant responses.

Create `.github/workflows/recruiter-agent.yml`:

```yaml
name: Recruiter Agent

on:
  schedule:
    # Run every 30 minutes
    - cron: '*/30 * * * *'
  workflow_dispatch:  # Manual trigger

jobs:
  run:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Setup Ollama
      run: |
        curl -fsSL https://ollama.ai/install.sh | sh
        ollama serve &
        sleep 5
        ollama pull phi  # Smaller model for CI
    
    - name: Run agent
      env:
        GMAIL_CREDENTIALS: ${{ secrets.GMAIL_CREDENTIALS }}
        GMAIL_TOKEN: ${{ secrets.GMAIL_TOKEN }}
        LLM_PROVIDER: ollama
        OLLAMA_MODEL: phi
      run: |
        # Decode credentials from secrets
        echo "$GMAIL_CREDENTIALS" | base64 -d > credentials/gmail_credentials.json
        echo "$GMAIL_TOKEN" | base64 -d > credentials/gmail_token.json
        
        # Run once
        python main.py --once
    
    - name: Upload logs
      uses: actions/upload-artifact@v3
      with:
        name: logs
        path: logs/
```

**Setup secrets:**
```bash
# Encode credentials
base64 credentials/gmail_credentials.json
base64 credentials/gmail_token.json

# Add to GitHub repo secrets:
# Settings > Secrets > Actions
# - GMAIL_CREDENTIALS
# - GMAIL_TOKEN
```

**Pros:**
- Completely free
- Runs every 30 minutes (configurable)
- No server management

**Cons:**
- Not instant (30-minute delay)
- Cold start each time

## Option 3: Raspberry Pi (Best Free 24/7 Solution)

### Why Raspberry Pi?

- ✅ $35-50 one-time cost
- ✅ Runs 24/7 on ~5W power ($0.50/month electricity)
- ✅ Can run Ollama (Pi 4 8GB or Pi 5)
- ✅ Complete control
- ✅ Always on

### Setup

1. Install Raspberry Pi OS (64-bit)

2. Install Python and dependencies:
```bash
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements.txt
```

3. Install Ollama:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

4. Pull a model (use smaller one on Pi):
```bash
ollama pull phi  # 2.7GB, works on Pi 4 8GB
```

5. Setup systemd service (see Linux section above)

6. Let it run!

### Performance Optimization

For Raspberry Pi:
```bash
# In .env
OLLAMA_MODEL=phi  # Smaller model
CHECK_INTERVAL_SECONDS=600  # Check every 10 min to save resources
```

## Option 4: Docker (Any Platform)

### Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p data logs credentials

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Run
CMD ["python", "main.py", "--daemon"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
    restart: unless-stopped
  
  recruiter-agent:
    build: .
    volumes:
      - ./credentials:/app/credentials
      - ./data:/app/data
      - ./logs:/app/logs
      - ./config:/app/config
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - LLM_PROVIDER=ollama
      - OLLAMA_MODEL=llama2
    depends_on:
      - ollama
    restart: unless-stopped

volumes:
  ollama_data:
```

### Run

```bash
docker-compose up -d
```

### View logs

```bash
docker-compose logs -f recruiter-agent
```

## Monitoring & Maintenance

### Check Agent Status

```bash
# View recent logs
tail -f logs/agent.log

# Check escalations
cat logs/escalations.log

# Interactive status
python main.py --interactive
> status
```

### Automated Health Checks

Create `healthcheck.sh`:

```bash
#!/bin/bash
# Check if agent is running
if ! pgrep -f "main.py --daemon" > /dev/null; then
    echo "Agent not running! Starting..."
    cd /path/to/ai-recruiter-agent
    python main.py --daemon &
    echo "Agent restarted at $(date)" >> logs/restarts.log
fi
```

Add to cron (check every hour):
```cron
0 * * * * /path/to/healthcheck.sh
```

### Email Notifications

Set escalation email in `.env`:
```bash
ESCALATION_EMAIL=your.personal.email@gmail.com
```

Agent will email you when human intervention needed.

### Log Rotation

Create `logrotate.conf`:

```
/path/to/ai-recruiter-agent/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

## Performance Tuning

### Reduce Resource Usage

```bash
# Use smaller model
OLLAMA_MODEL=phi

# Increase check interval
CHECK_INTERVAL_SECONDS=600  # 10 minutes

# Limit conversation history
MAX_HISTORY_MESSAGES=10
```

### Optimize for Speed

```bash
# Use faster model
OLLAMA_MODEL=mistral

# Pre-warm model
ollama run mistral "test"
```

### Save Costs on Cloud

```bash
# Use cloud LLM (skip Ollama)
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key

# Smaller instance needed (no Ollama)
# Render/Railway free tier will work
```

## Backup & Recovery

### Backup Database

```bash
# Automated backup
cp data/conversations.db backups/conversations_$(date +%Y%m%d).db

# Add to cron (daily backup)
0 2 * * * cp /path/to/data/conversations.db /path/to/backups/conversations_$(date +\%Y\%m\%d).db
```

### Restore from Backup

```bash
cp backups/conversations_20240101.db data/conversations.db
```

## Security Considerations

### Credentials

```bash
# Secure permissions
chmod 600 credentials/*.json
chmod 600 .env

# Never commit to git
echo "credentials/" >> .gitignore
echo ".env" >> .gitignore
```

### Running as Service

Create dedicated user:
```bash
sudo useradd -r -s /bin/false recruiter-agent
sudo chown -R recruiter-agent:recruiter-agent /path/to/ai-recruiter-agent
```

Update systemd service to run as this user.

## Troubleshooting Deployment

### Agent Stops Running

Check logs:
```bash
tail -100 logs/agent.log
```

Common issues:
- Ollama not running: `ollama serve`
- Gmail token expired: Delete `credentials/gmail_token.json` and re-authenticate
- Out of memory: Use smaller model (phi)

### No Responses Being Sent

Check:
```bash
# Is auto-reply enabled?
grep AUTO_REPLY_ENABLED .env

# Are there escalations pending?
cat logs/escalations.log

# Check conversation state
python main.py --interactive
> status
```

### High Resource Usage

```bash
# Monitor
top
# Look for ollama or python processes

# Reduce:
# 1. Use smaller model (phi)
# 2. Increase check interval
# 3. Limit concurrent processing
```

## Recommended Setup

### For Testing (Laptop/Desktop)
```bash
python main.py --once  # Manual checks
```

### For Active Job Search (Daily Use)
```bash
python main.py --daemon  # Always running on your computer
```

### For Passive Opportunities (Background)
- Raspberry Pi with systemd service
- Check every 10-30 minutes
- Minimal resources

### For High Volume (Many Applications)
- Cloud deployment (Render/Railway)
- GitHub Actions for scheduled checks
- Consider paid LLM API for better quality

## Cost Analysis

| Option | Setup Cost | Monthly Cost | Effort | Uptime |
|--------|-----------|--------------|--------|--------|
| Local (Manual) | $0 | $0 | Low | When you check |
| Local (Daemon) | $0 | $1-2 | Low | When computer on |
| Raspberry Pi | $35-50 | $0.50 | Medium | 99.9% |
| GitHub Actions | $0 | $0 | Medium | Every 30 min |
| Cloud (Free tier) | $0 | $0 | High | 95% (sleeps) |
| Cloud (Paid) | $0 | $5-10 | Medium | 99.9% |

## Recommendation

**Start:** Local daemon mode
**Scale to:** Raspberry Pi or GitHub Actions
**Upgrade if needed:** Cloud with paid tier

---

**Best free 24/7 solution:**
Raspberry Pi 4 (8GB) + systemd service = $35 one-time + $0.50/month electricity

**Next best:**
GitHub Actions (completely free, runs every 30 min)

**Easiest:**
Local daemon on your computer (free, runs when computer is on)

Choose based on your needs!

