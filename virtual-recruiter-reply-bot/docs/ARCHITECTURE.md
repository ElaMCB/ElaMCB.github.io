# AI Recruiter Agent - Architecture & Free Solution Strategy

## Overview

This project implements a **100% FREE** autonomous agent that can handle job recruiter communications across email, SMS, and (future) voice channels.

## Design Philosophy

### Free-First Approach

Every component was chosen to be free or have generous free tiers:

| Component | Free Solution | Paid Alternative | Cost Savings |
|-----------|---------------|------------------|--------------|
| LLM | Ollama (local) | OpenAI GPT-4 | ~$50-100/month |
| Email | Gmail API | - | Free |
| SMS | Email-to-SMS Gateway | Twilio | ~$10-20/month |
| Database | SQLite | - | Free |
| Hosting | Local/Free tier | Cloud VM | ~$5-20/month |
| **Total** | **$0/month** | **$65-140/month** | **100% savings** |

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Configuration                       │
│                  (profile.yaml, prompts.yaml)                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Main Entry Point (main.py)                 │
│              (Daemon/Once/Interactive modes)                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Central Orchestrator (orchestrator.py)          │
│                                                              │
│  • Monitors all channels                                    │
│  • Routes messages to appropriate handlers                  │
│  • Coordinates response generation                          │
│  • Manages escalations                                      │
└─────────────────────────────────────────────────────────────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Email Agent  │    │  SMS Agent   │    │ Voice Agent  │
│              │    │              │    │  (Future)    │
│ Gmail API    │    │ Email-to-SMS │    │   Twilio     │
└──────────────┘    └──────────────┘    └──────────────┘
        │                    │                    │
        └────────────────────┴────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         State Manager                    │
        │  (SQLite - conversations.db)            │
        │                                         │
        │  • Conversation history                 │
        │  • Extracted information                │
        │  • Current stage tracking               │
        │  • Escalation flags                     │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │         LLM Processor                    │
        │  (Ollama - Local & Free)                │
        │                                         │
        │  • Response generation                  │
        │  • Information extraction               │
        │  • Conversation stage detection         │
        │  • Job matching assessment              │
        └─────────────────────────────────────────┘
```

## Component Details

### 1. Central Orchestrator

**File:** `core/orchestrator.py`

**Responsibilities:**
- Main event loop
- Channel coordination
- Message routing
- Response sending
- Escalation handling

**Key Methods:**
- `process_new_messages()` - Main processing loop
- `_process_emails()` - Handle email channel
- `_process_sms()` - Handle SMS channel
- `_notify_escalation()` - Human intervention

### 2. Email Agent

**File:** `agents/email_agent.py`

**Free Solution:** Gmail API
- No cost
- 1 billion quota units/day (effectively unlimited)
- OAuth 2.0 authentication
- Full access to labels, threads, attachments

**Features:**
- Fetch unread emails
- Filter for recruiter messages (keyword detection)
- Send threaded replies
- Mark as read
- Add custom labels
- Parse email threads

**Why Free:**
Google provides generous free tier for personal use.

### 3. SMS Agent

**File:** `agents/sms_agent.py`

**Free Solution:** Email-to-SMS Gateways
- Carrier-provided gateways (AT&T, Verizon, etc.)
- Send SMS by emailing `phonenumber@txt.att.net`
- Receive SMS as emails (from some services)
- Zero cost

**Limitations:**
- Need to know carrier
- Not all SMS arrive as emails
- No delivery confirmation

**Paid Alternative:** Twilio (~$10/month for typical use)

**Why Free:**
Carriers provide these gateways for compatibility. We leverage them for automation.

### 4. LLM Processor

**File:** `core/llm_processor.py`

**Free Solution:** Ollama (Local LLM)
- Runs on your computer
- Models: Llama 2, Mistral, CodeLlama
- No API costs
- No rate limits
- Complete privacy

**Features:**
- Response generation
- Information extraction (company, position, salary, etc.)
- Conversation stage detection
- Job matching assessment
- Context-aware replies

**System Requirements:**
- 8GB RAM minimum (16GB recommended)
- 10GB disk space
- Works on Windows, Mac, Linux

**Why Free:**
Open-source models run locally. No cloud API needed.

### 5. State Manager

**File:** `core/state_manager.py`

**Free Solution:** SQLite
- File-based database
- No server needed
- Built into Python
- Reliable and fast

**Schema:**
```sql
conversations:
  - thread_id (PK)
  - stage, channel, company, recruiter_name
  - position, tech_stack, salary_range
  - work_arrangement, location
  - conversation_history (JSON)
  - requires_escalation, escalation_reason
  - created_at, updated_at

messages:
  - id (PK)
  - thread_id (FK)
  - timestamp, channel, direction
  - content, metadata (JSON)
```

**Features:**
- Conversation tracking
- Message history
- State persistence
- Escalation flags

**Why Free:**
SQLite is free, lightweight, and perfect for this use case.

## Conversation Flow

### Stage Progression

```
initial_contact
    │
    ├─→ information_gathering
    │       │
    │       ├─→ screening
    │       │       │
    │       │       ├─→ negotiation [ESCALATE]
    │       │       │       │
    │       │       │       └─→ scheduling [ESCALATE]
    │       │       │
    │       │       └─→ declined
    │       │
    │       └─→ declined
    │
    └─→ declined
```

### Stage Definitions

1. **initial_contact:** First message from recruiter
   - Extract basic info (company, position)
   - Ask clarifying questions
   - Express interest

2. **information_gathering:** Collecting details
   - Tech stack requirements
   - Work arrangement (remote/hybrid/onsite)
   - Salary range
   - Team structure

3. **screening:** Answering qualification questions
   - Confirm experience
   - Highlight relevant skills
   - Address concerns

4. **negotiation:** Discussing compensation [ESCALATION]
   - Salary discussion
   - Benefits review
   - Requires human approval

5. **scheduling:** Setting up interviews [ESCALATION]
   - Coordinate calendar
   - Confirm details
   - Human confirmation needed

6. **declined:** Not a good fit
   - Thank them professionally
   - Explain briefly
   - Leave door open

## Escalation Strategy

### When to Escalate

Automatically escalate when:
- Salary negotiation starts
- Final offer received
- Interview needs scheduling
- Unclear requirements
- Technical assessment required
- Any uncertainty

### Escalation Methods

1. **Log to file:** `logs/escalations.log`
2. **Email notification:** (configurable)
3. **Pending approvals:** `data/pending_approvals.txt`
4. **Database flag:** `requires_escalation` in conversations table

### Safety First

The agent is **conservative by default:**
- Never makes final commitments
- Never accepts/rejects offers
- Never schedules without confirmation
- Always asks for clarification when unsure

## Data Flow Example

### Incoming Recruiter Email

```
1. Gmail → EmailAgent detects unread recruiter email
                ↓
2. Orchestrator creates/updates ConversationState
                ↓
3. LLMProcessor generates response
   - Analyzes message
   - Extracts information
   - Consults profile.yaml
   - Generates professional reply
                ↓
4. StateManager updates database
   - New stage
   - Extracted info
   - Message history
                ↓
5. Check escalation rules
   → If escalation needed: Notify and STOP
   → If safe to continue: ↓
                ↓
6. EmailAgent sends reply
                ↓
7. Mark email as processed
```

## LLM Prompt Engineering

### System Prompt Structure

```
Base System Prompt (from prompts.yaml)
    +
User Profile (from profile.yaml)
    +
Stage-Specific Guidance
    +
Conversation Context
    +
Channel Constraints (SMS: brief, Email: detailed)
```

### Response Format

LLM returns structured JSON:

```json
{
  "response": "Generated message text",
  "extracted_info": {
    "company": "TCS",
    "position": "Java Selenium Automation Architect",
    "recruiter_name": "Alex",
    "salary_range": "$120k-150k",
    "work_arrangement": "remote"
  },
  "next_stage": "information_gathering",
  "requires_escalation": false,
  "escalation_reason": null,
  "confidence": 0.85
}
```

### Fallback Parsing

If JSON parsing fails:
- Use entire output as response
- Extract info using regex
- Check escalation keywords
- Set confidence low

## Deployment Options

### 1. Local Machine (Recommended for Free)

```bash
# Run once per check
python main.py --once

# Run continuously
python main.py --daemon --interval 300

# Interactive mode
python main.py --interactive
```

**Pros:**
- Completely free
- Full control
- Maximum privacy

**Cons:**
- Computer must be on
- Manual restarts needed

### 2. Free Cloud (Always-On)

Options:
- **Render.com** - Free tier (750 hours/month)
- **Railway.app** - Free tier ($5 credit/month)
- **Fly.io** - Free tier (3GB RAM)

**Challenge:** Need to run Ollama on limited resources
**Solution:** Use smaller model (phi - 2.7GB) or cloud API

### 3. Scheduled Cloud (Most Efficient)

Use GitHub Actions or similar:
- Runs every 5-30 minutes
- No always-on server
- Completely free

**Limitation:** No webhook support for instant responses

### 4. Hybrid (Best of Both)

- Email/SMS: Cloud (lightweight)
- LLM: Local Ollama (powerful)
- Communication via API

## Security Considerations

### Credentials

- Gmail OAuth token: `credentials/gmail_token.json`
- Never commit to git
- Encrypt if storing remotely
- Rotate periodically

### Data Privacy

- All conversations in local SQLite
- LLM runs locally (no data leaves computer)
- Email API uses OAuth (more secure than passwords)

### Safe Defaults

- `AUTO_REPLY_ENABLED=true` but conservative
- `REQUIRE_APPROVAL=false` for routine messages
- Escalate anything risky
- Log everything for review

## Cost Comparison

### This Solution (Free)

```
Gmail API:           $0
Ollama (Local LLM):  $0
SQLite Database:     $0
Email-to-SMS:        $0
Total:               $0/month
```

**One-time cost:** Computer to run it on (you already have)

### Typical Paid Stack

```
OpenAI API:          $50-100/month
Twilio SMS:          $10-20/month
Database Hosting:    $5-10/month
Server Hosting:      $10-20/month
Total:               $75-150/month
```

**Annual savings with free solution: $900-1,800**

## Scalability

### Current Capacity (Free Tier)

- **Emails:** Unlimited (Gmail API)
- **SMS:** Unlimited (email gateways)
- **LLM:** Unlimited (local)
- **Storage:** Unlimited (SQLite on your disk)

### Bottlenecks

1. **Ollama speed:** ~2-10 seconds per response
   - Mitigated: Async processing
   - Upgrade: Better hardware or GPU

2. **Email API rate limits:** 250 quota units per user per second
   - Not a problem for job hunting
   - Can process 1000s of emails/day

### When to Upgrade

Consider paid services if:
- Getting 50+ recruiter messages per day
- Need instant SMS responses
- Want higher quality LLM (GPT-4)
- Need phone call handling
- Deploying for multiple people

## Future Enhancements

### Planned Features

1. **Voice Integration** (Twilio + Whisper + TTS)
2. **Multi-language Support**
3. **LinkedIn Integration**
4. **Calendar Sync** (automatic scheduling)
5. **Resume Attachment** (send automatically)
6. **Analytics Dashboard** (track success rate)
7. **Multiple Profiles** (different job types)
8. **Team Mode** (multiple job seekers)

### Community Contributions

Open to:
- Better LLM prompts
- Additional channel integrations
- UI improvements
- Deployment guides
- Language translations

## Conclusion

This architecture provides:

✅ **100% free** - No ongoing costs
✅ **Private** - Data never leaves your computer
✅ **Extensible** - Easy to add features
✅ **Reliable** - Battle-tested components
✅ **Powerful** - Handles complex conversations
✅ **Safe** - Conservative escalation strategy

Perfect for automating the tedious parts of job hunting while keeping you in control of important decisions!

---

**Questions?** Check other docs or review the code - it's well-commented!

