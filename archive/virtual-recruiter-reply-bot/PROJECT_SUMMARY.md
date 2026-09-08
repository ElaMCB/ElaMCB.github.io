# AI Recruiter Response Agent - Project Summary

## 🎯 What Is This?

A **100% FREE** autonomous AI agent that automatically responds to job recruiters on your behalf via:
- ✉️ Email (Gmail API)
- 📱 SMS (Email-to-SMS gateways) 
- 📞 Voice (Future - requires paid services)

## 💡 The Problem It Solves

You received a message from "Alex, a virtual recruiter" - an AI reaching out to you. Why not have **your AI respond to their AI** while you focus on actual interviews?

This agent:
- Monitors your email for recruiter messages
- Responds professionally with your preferences
- Asks the right questions (salary, remote options, etc.)
- Tracks conversation context
- Escalates to you when needed (salary negotiation, interview scheduling)

## 💰 Cost: $0/month

Unlike paid solutions that cost $50-150/month, this uses:
- **Ollama** (free local LLM) instead of OpenAI/Claude
- **Gmail API** (free unlimited) for email
- **Email-to-SMS gateways** (free) instead of Twilio
- **SQLite** (free) for data storage
- **Your computer** for hosting

## 🚀 Quick Start (15 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install Ollama and pull model
# Download from: https://ollama.ai/download
ollama pull llama2

# 3. Setup Gmail API
# Follow: docs/gmail_setup.md
# Place credentials in: credentials/gmail_credentials.json

# 4. Configure your profile
cp env.example .env
# Edit config/profile.yaml with your info

# 5. Run!
python main.py --once
```

See [docs/QUICK_START.md](docs/QUICK_START.md) for detailed instructions.

## 📁 Project Structure

```
ai-recruiter-agent/
├── agents/                    # Channel handlers
│   ├── email_agent.py        # Gmail API integration
│   ├── sms_agent.py          # SMS via email-to-SMS
│   └── voice_agent.py        # Future voice handling
│
├── core/                      # Core logic
│   ├── orchestrator.py       # Main coordinator
│   ├── state_manager.py      # Conversation tracking
│   └── llm_processor.py      # AI response generation
│
├── config/                    # Configuration
│   ├── profile.yaml          # Your professional profile
│   └── prompts.yaml          # AI prompts and templates
│
├── utils/                     # Utilities
│   └── logger.py             # Logging system
│
├── docs/                      # Documentation
│   ├── QUICK_START.md        # Getting started guide
│   ├── ARCHITECTURE.md       # System design
│   ├── EXAMPLE_RESPONSES.md  # Response examples
│   ├── gmail_setup.md        # Gmail API setup
│   ├── ollama_setup.md       # Ollama installation
│   └── sms_setup.md          # SMS configuration
│
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── env.example               # Environment template
└── README.md                 # Main documentation
```

## 🔄 How It Works

```
1. Recruiter sends message
         ↓
2. Agent detects it (email/SMS)
         ↓
3. Extracts info (company, position, salary, etc.)
         ↓
4. Consults your profile (preferences, criteria)
         ↓
5. Generates professional response (using Ollama)
         ↓
6. Checks if escalation needed
   ├─ YES → Notifies you, waits for approval
   └─ NO → Sends response automatically
         ↓
7. Updates conversation state
         ↓
8. Continues thread-aware conversation
```

## 🎭 Responding to Alex (Your Example)

### The Message You Got:
```
Hi Elena, this is Alex, a virtual recruiter from Artech Information 
Systems. I am reaching out to you for a position of Java Selenium 
Automation Architect with TCS. Text CALL to receive a call back...
```

### What the Agent Would Do:

**Analysis:**
- Recruiter: Alex (AI recruiter)
- Company: Artech Information Systems
- Client: TCS  
- Position: Java Selenium Automation Architect ✅ (matches your criteria)
- Action: Request call

**Response (Option A - Redirect to Email):**
```
Hi Alex! Thanks for reaching out about the Java Selenium Automation 
Architect role with TCS. I'm interested! Could you email me details 
at elena@email.com? Specifically: job description, salary range, and 
remote/hybrid options. Thanks!
```

**Response (Option B - Request Call):**
```
CALL
```
(Then voice agent handles the call - requires Twilio)

See [docs/EXAMPLE_RESPONSES.md](docs/EXAMPLE_RESPONSES.md) for more examples.

## 🛡️ Safety Features

### Escalation Triggers
Agent automatically escalates (stops and notifies you) when:
- 💰 Salary negotiation starts
- 📄 Final offer received
- 📅 Interview needs scheduling
- ❓ Unclear requirements
- 🧪 Technical assessment needed

### Auto-Decline Rules
Agent politely declines if:
- Salary below your threshold (configurable)
- Position doesn't match criteria
- Keywords like "unpaid", "internship"
- No remote option (if required)

### Approval Mode
Enable `REQUIRE_APPROVAL=true` in `.env` to review every response before sending.

## 📊 Conversation Tracking

All conversations stored in SQLite database:
```
data/conversations.db
```

View conversation history:
```bash
python main.py --interactive
> list  # Show all conversations
> view <thread_id>  # View specific conversation
> status  # Overall status report
```

## 🎨 Customization

### Your Profile (`config/profile.yaml`)
```yaml
personal:
  name: "Elena"
  current_title: "Java Selenium Automation Architect"
  years_experience: 10

preferences:
  work_arrangement: "Remote preferred"
  salary_range:
    minimum: 120000
    target: 150000

job_criteria:
  must_have:
    - title_contains: ["architect", "lead", "senior"]
    - remote_option: true
```

### Response Style (`config/prompts.yaml`)
```yaml
communication_style:
  tone: "professional"
  formality: "medium"
  response_length: "concise"
```

### Auto-Reply Behavior (`.env`)
```bash
# Enable/disable automatic responses
AUTO_REPLY_ENABLED=true

# Require manual approval
REQUIRE_APPROVAL=false

# Check interval (daemon mode)
CHECK_INTERVAL_SECONDS=300
```

## 🔌 Running Modes

### 1. Single Check (Testing)
```bash
python main.py --once
```
Process messages once and exit. Good for testing.

### 2. Daemon Mode (Production)
```bash
python main.py --daemon --interval 300
```
Run continuously, check every 5 minutes. Press Ctrl+C to stop.

### 3. Interactive Mode
```bash
python main.py --interactive
```
Interactive shell with commands: `check`, `status`, `list`, `view`, `quit`

## 📈 Benefits

### Time Savings
- ⏱️ **Initial screening:** 5-10 minutes per recruiter → **Automated**
- 📧 **Email composition:** 10-15 minutes → **Instant**
- 🔄 **Follow-ups:** Often forgotten → **Never missed**

### Better Outcomes
- ✅ Always asks about salary and remote options
- ✅ Never forgets to respond
- ✅ Consistent professional tone
- ✅ Tracks all conversations in one place

### Focus Your Energy
- 🎯 You handle: Final interviews, offer negotiation, big decisions
- 🤖 AI handles: Initial contact, info gathering, screening questions

## 🌟 Use Cases

### Daily Job Hunt
```bash
# Morning: Check new messages
python main.py --once

# Enable daemon for continuous monitoring
python main.py --daemon
```

### Passive Job Search
Enable daemon mode and forget about it. The agent:
- Responds to interesting opportunities
- Declines mismatches
- Escalates when you need to step in

### High Volume
Getting 10+ recruiter messages/day? Let the agent:
- Handle the initial screening
- Filter to only good matches
- Escalate the top 2-3 for your review

## ⚙️ Advanced Features

### Multiple LLM Providers
```bash
# Ollama (default, free)
LLM_PROVIDER=ollama

# OpenAI (paid, higher quality)
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key

# Anthropic Claude (paid)
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key
```

### Gmail Labels
Agent automatically adds labels:
- `AI-Recruiter/Processed` - Handled by agent
- Custom labels via code

### Conversation Export
```python
# Export conversations to review
python -c "
from core.state_manager import StateManager
sm = StateManager()
convs = sm.get_active_conversations()
for c in convs:
    print(f'{c.company} - {c.position} - {c.stage}')
"
```

## 🐛 Troubleshooting

### "Gmail credentials not found"
➡️ Follow [docs/gmail_setup.md](docs/gmail_setup.md)

### "Ollama connection refused"
➡️ Run `ollama serve` to start Ollama server

### "Model not found"
➡️ Run `ollama pull llama2`

### Slow responses
➡️ Use smaller model: `ollama pull phi`

### Too aggressive/passive
➡️ Adjust prompts in `config/prompts.yaml`

## 🔮 Future Enhancements

### Planned (Community Welcome!)
- 🎙️ Voice call handling (Twilio integration)
- 🔗 LinkedIn message automation
- 📅 Calendar integration (auto-schedule interviews)
- 📊 Analytics dashboard
- 📱 Mobile app notifications
- 🌍 Multi-language support
- 👥 Team/family mode (multiple job seekers)

### Voice Integration (Next Priority)
```bash
# Using Twilio + OpenAI Whisper
# Cost: ~$1/month + $0.01/min
# See: agents/voice_agent.py for implementation outline
```

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Overview and features |
| [QUICK_START.md](docs/QUICK_START.md) | Get started in 15 mins |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design details |
| [EXAMPLE_RESPONSES.md](docs/EXAMPLE_RESPONSES.md) | Response examples |
| [gmail_setup.md](docs/gmail_setup.md) | Gmail API setup |
| [ollama_setup.md](docs/ollama_setup.md) | Ollama installation |
| [sms_setup.md](docs/sms_setup.md) | SMS configuration |

## 🤝 Contributing

This is your personal project, but you can:
- Share with friends (it's free!)
- Customize for your needs
- Add features you want
- Improve the prompts
- Share your success stories

## ⚖️ Legal & Ethical

### Transparent
- Agent identifies as AI when appropriate
- Provides option to speak with human
- Respects opt-out requests (STOP keyword)

### Conservative
- Never makes final commitments
- Escalates important decisions
- Logs all interactions for review

### Compliant
- Respects recruiter opt-out (STOP)
- No spam or harassment
- Professional communication only

### Your Data
- Stored locally (SQLite)
- LLM runs locally (Ollama)
- No data sent to third parties (except Gmail API for sending email)

## 🎓 Learning Resources

### Understanding the Code
- Well-commented Python code
- Modular architecture
- Easy to extend

### LLM Prompt Engineering
- See `config/prompts.yaml` for examples
- Adjust to your communication style
- Test and iterate

### API Integration
- Gmail API examples in `agents/email_agent.py`
- SMS gateway usage in `agents/sms_agent.py`
- Extensible for other channels

## 🚦 Getting Started Checklist

- [ ] Python 3.9+ installed
- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Install Ollama and pull model: `ollama pull llama2`
- [ ] Setup Gmail API credentials
- [ ] Configure `.env` file
- [ ] Update `config/profile.yaml` with your info
- [ ] Test run: `python main.py --setup-check`
- [ ] First real run: `python main.py --once`
- [ ] Review responses in logs
- [ ] Enable daemon: `python main.py --daemon`
- [ ] Check escalations daily
- [ ] Refine prompts based on results

## 🎉 Success Stories

Once you have success with this agent, you'll:
- ✅ Never miss a recruiter message
- ✅ Always ask the right questions
- ✅ Maintain professional communication
- ✅ Focus on interviews, not screening
- ✅ Track all opportunities in one place

## 📞 Support

- Check docs in `docs/` folder
- Review example responses
- Check logs for debugging
- Read the well-commented code

## 🎯 Bottom Line

**Problem:** AI recruiter reached out to you
**Solution:** Your AI responds to their AI
**Result:** You focus on final interviews and offers
**Cost:** $0/month

**Ready to automate?**

```bash
cd ai-recruiter-agent
python main.py --daemon
```

Let the robots talk to each other. You focus on landing the job! 🚀

---

**Built with:** Python, Ollama, Gmail API, SQLite, and lots of coffee ☕

