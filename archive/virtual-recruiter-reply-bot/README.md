```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        █████╗ ██████╗ ██╗ █████╗     ╔═╗╦                   ║
║       ██╔══██╗██╔══██╗██║██╔══██╗    ╠═╣║                   ║
║       ███████║██████╔╝██║███████║    ║ ║║                   ║
║       ██╔══██║██╔══██╗██║██╔══██║    ║ ║║                   ║
║       ██║  ██║██║  ██║██║██║  ██║    ╩ ╩╩                   ║
║                                                               ║
║       Automated Recruiter Interaction Assistant               ║
║       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━         ║
║       Your AI agent for intelligent recruiter responses       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

# ARIA - Virtual Recruiter Reply Bot

**Your AI assistant that responds to AI recruiters, so you can focus on landing the job.**

ARIA is an autonomous agent that handles job recruiter communications across multiple channels (Email, SMS, Voice). When virtual recruiters like "Alex" reach out, ARIA responds professionally on your behalf, gathering information, asking the right questions, and escalating to you when needed.

---

## Features

**Email Automation**
- Automatically read and respond to recruiter emails via Gmail API
- Thread-aware conversations with full context tracking
- Professional responses based on your profile and preferences

**SMS Handling**
- Process and reply to text messages from recruiters
- Free email-to-SMS gateway integration (no Twilio fees)
- Handles special keywords (STOP, CALL, etc.)

**Intelligent State Management**
- Track conversation context across all interactions
- SQLite-based conversation history
- Multi-stage conversation tracking (initial contact → screening → negotiation)

**LLM-Powered Responses**
- Generate professional, context-aware replies
- Local Ollama (free) or cloud APIs (OpenAI, Claude)
- Customizable tone, style, and templates

**Multi-Channel Support**
- Unified handling of email, SMS, and future voice integration
- Single codebase for all communication channels
- Extensible architecture for additional channels

---

## 100% Free Implementation

This project uses only free services:

| Component | Free Solution | Typical Cost |
|-----------|---------------|--------------|
| LLM | Ollama (local) | $50-100/month |
| Email | Gmail API | $0 |
| SMS | Email-to-SMS gateway | $10-20/month |
| Database | SQLite | $0 |
| Hosting | Your computer/Raspberry Pi | $5-20/month |
| **Total** | **$0/month** | **$65-140/month** |

---

## Quick Start

### Prerequisites

1. Python 3.9+
2. Gmail account with API access
3. Ollama installed (for local LLM)

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install Ollama (for local LLM)
# Visit: https://ollama.ai/download

# Pull a model
ollama pull llama2
```

### Configuration

1. Set up Gmail API credentials (see `docs/gmail_setup.md`)
2. Copy `.env.example` to `.env` and fill in your details
3. Configure your profile in `config/profile.yaml`

### Running

```bash
# Start the agent
python main.py

# Run in background
python main.py --daemon
```

---

## Project Structure

```
virtual-recruiter-reply-bot/
├── agents/
│   ├── email_agent.py      # Email handling via Gmail API
│   ├── sms_agent.py         # SMS handling via email-to-SMS gateway
│   └── voice_agent.py       # Future voice handling (Twilio)
├── core/
│   ├── orchestrator.py      # Central coordinator for all channels
│   ├── state_manager.py     # Conversation state tracking (SQLite)
│   └── llm_processor.py     # LLM response generation (Ollama/OpenAI/Claude)
├── config/
│   ├── profile.yaml         # Your professional profile and preferences
│   └── prompts.yaml         # AI system prompts and templates
├── docs/
│   ├── QUICK_START.md       # Get started in 15 minutes
│   ├── ARCHITECTURE.md      # System design and architecture
│   ├── EXAMPLE_RESPONSES.md # Real response examples
│   ├── gmail_setup.md       # Gmail API setup guide
│   ├── ollama_setup.md      # Ollama installation guide
│   ├── sms_setup.md         # SMS configuration
│   └── DEPLOYMENT.md        # 24/7 deployment options
├── utils/
│   └── logger.py            # Logging utilities
├── data/
│   └── conversations.db     # SQLite database (auto-created)
├── main.py                  # Entry point
├── requirements.txt         # Python dependencies
└── env.example             # Configuration template
```

---

## How ARIA Works

**1. Monitor**
ARIA checks your email and SMS channels periodically for new recruiter messages.

**2. Parse**
Extracts key information: company name, position title, salary range, work arrangement, tech stack, and more.

**3. Analyze**
Compares the opportunity against your profile and job criteria to determine fit.

**4. Generate**
Creates a professional, context-aware response using LLM (local Ollama or cloud API).

**5. Respond**
Sends the reply via the appropriate channel (email or SMS).

**6. Track**
Updates conversation state in SQLite database for context-aware follow-ups.

**7. Escalate**
When important decisions are needed (salary negotiation, interview scheduling, final offers), ARIA notifies you for human intervention.

---

## Conversation Stages

ARIA tracks conversations through multiple stages:

- **initial_contact** - First message from recruiter
- **information_gathering** - Collecting details about the role
- **screening** - Answering qualification questions
- **negotiation** - Discussing compensation and benefits (escalates to you)
- **scheduling** - Arranging interviews (escalates to you)
- **declined** - Not a good fit, politely declined

---

## Safety & Ethics

**Transparency**
- ARIA can identify itself as an AI assistant when appropriate
- All interactions are logged for your review
- Full conversation history maintained in database

**Human Oversight**
- Automatic escalation for important decisions
- Option to require approval for all responses
- Manual mode available for sensitive conversations

**Compliance**
- Respects STOP/unsubscribe requests automatically
- Never makes final commitments without your approval
- Follows professional communication standards

---

## Documentation

Comprehensive guides available in the `docs/` folder:

- **QUICK_START.md** - Get ARIA running in 15 minutes
- **ARCHITECTURE.md** - System design and free solution strategy
- **EXAMPLE_RESPONSES.md** - Real-world response examples
- **gmail_setup.md** - Gmail API setup walkthrough
- **ollama_setup.md** - Free local LLM installation
- **sms_setup.md** - SMS configuration options
- **DEPLOYMENT.md** - Run ARIA 24/7 for free

---

## Related Projects

**Job Search Automation Suite**

Companion project for proactive job searching. While ARIA handles incoming recruiter messages, the Job Search Automation Suite helps you find and apply to jobs.

**Portfolio:** https://elamcb.github.io/job-search-automation/

**What it does:**
- Intelligent job matching (85% accuracy) across multiple platforms
- Application status tracking and follow-up reminders
- Interview analytics and preparation recommendations
- Resume optimization for ATS systems
- AI-powered skill matching and relevance scoring

**When to use together:**
- **Job Search Automation**: Actively search and apply to jobs you want
- **ARIA**: Passively handle recruiters who reach out to you

Together, they provide complete coverage of your job search - both active hunting and passive opportunity management!

---

## Contributing

This is a personal project, but you're welcome to:
- Fork and customize for your needs
- Submit improvements via pull requests
- Share your success stories
- Report issues or suggestions

---

## License

MIT License - See LICENSE file for details.

Use freely for personal job search automation. No warranty provided.

