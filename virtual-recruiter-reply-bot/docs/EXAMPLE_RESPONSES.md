# Example Agent Responses

Real-world examples of how the AI agent handles recruiter messages.

## Example 1: The Message You Received

### Incoming SMS from Alex (Virtual Recruiter)

```
Hi Elena, this is Alex, a virtual recruiter from Artech Information 
Systems. I am reaching out to you for a position of Java Selenium 
Automation Architect with TCS. Text CALL to receive a call back. 
It will take 5-7 mins. By replying, you consent to receive limited 
text messages and automated artificial voice calls for job 
opportunities from Artech Information Systems and its partners. 
Standard text rates apply; reply STOP to unsubscribe
```

### Agent Analysis

```json
{
  "message_type": "initial_contact",
  "channel": "sms",
  "extracted_info": {
    "recruiter_name": "Alex",
    "recruiter_type": "virtual (AI)",
    "company": "Artech Information Systems",
    "client": "TCS",
    "position": "Java Selenium Automation Architect",
    "action_requested": "CALL"
  },
  "assessment": {
    "matches_title_criteria": true,
    "keyword_match": ["Java", "Selenium", "Automation", "Architect"],
    "interest_level": "high"
  }
}
```

### Agent Response (Option A: Request Email Details)

```
Hi Alex! Thanks for reaching out about the Java Selenium Automation 
Architect role with TCS. I'm interested in learning more. Could you 
email me the details at elena@email.com? I'd like to review the 
requirements, salary range, and remote/hybrid options. Thanks!
```

**Why this response:**
- ✅ Professional and friendly
- ✅ Shows interest
- ✅ Redirects to email (easier for detailed discussion)
- ✅ Sets expectations (what info you need)
- ✅ Under 160 characters when optimized
- ✅ Avoids immediate commitment

### Agent Response (Option B: Request Call)

```
CALL
```

**Note:** This triggers their automated system to call you. The voice agent (if enabled) would handle this call.

### Agent Response (Option C: Detailed via Email)

If they follow up via email:

```
Hi Alex,

Thank you for reaching out about the Java Selenium Automation Architect 
position with TCS through Artech Information Systems.

I have 10+ years of experience in test automation architecture with 
strong expertise in Java and Selenium. I'm interested in learning more 
about this opportunity.

Could you please provide:
- Detailed job description and key responsibilities
- Required technical skills and qualifications
- Work arrangement (remote, hybrid, or onsite)
- Location if onsite/hybrid
- Salary range for this position
- Expected start date and timeline

I'm currently employed and would need 2 weeks notice. My preferred work 
arrangement is remote or hybrid, and I'm targeting opportunities in the 
$120-150k range.

Looking forward to hearing from you.

Best regards,
Elena
Java Selenium Automation Architect
```

---

## Example 2: Initial Email from Real Recruiter

### Incoming Email

```
Subject: Senior Automation Engineer - Remote - Up to $140k

Hi Elena,

I came across your profile and was impressed by your automation 
experience. I'm working with a well-funded fintech startup looking 
for a Senior Automation Engineer to lead their QA automation efforts.

Details:
- 100% Remote
- Salary: $120-140k + equity
- Tech Stack: Java, Selenium, Cucumber, Jenkins
- Small team (3 QA, growing to 5)
- Direct impact on product quality

Are you open to exploring this opportunity? I'd love to schedule a 
15-minute call to discuss further.

Best,
Sarah Johnson
Tech Recruiter | TalentSource
sarah@talentsource.com | (555) 123-4567
```

### Agent Response

```
Hi Sarah,

Thank you for reaching out about the Senior Automation Engineer 
position. The role sounds interesting, and I appreciate the detailed 
information.

The remote arrangement, tech stack, and salary range align well with 
my interests. I have extensive experience with Java, Selenium, and 
CI/CD pipelines including Jenkins.

Before scheduling a call, could you provide:
- Company name (if not confidential)
- What's the product/industry focus?
- What are the biggest automation challenges they're facing?
- Team structure and reporting line
- Benefits package highlights

I'm currently employed with a 2-week notice period, so timeline 
expectations would be helpful as well.

Looking forward to learning more.

Best regards,
Elena
```

**Why this response:**
- ✅ Acknowledges all key points
- ✅ Confirms interest
- ✅ Asks strategic questions
- ✅ Establishes expertise credibly
- ✅ Sets expectations about timeline
- ✅ Professional but not too eager

---

## Example 3: Screening Questions

### Incoming Email

```
Subject: Re: Senior Automation Engineer - Remote - Up to $140k

Hi Elena,

Great to hear you're interested! To answer your questions:

- Company: FinanceFlow (Series B, raised $50M last year)
- Product: B2B SaaS for invoice automation
- Challenges: Scaling test coverage, reducing flaky tests, E2E automation
- Reporting to: VP of Engineering
- Benefits: Full health/dental, 401k match, unlimited PTO, $2k learning budget

A few questions for you:
1. How many years of experience do you have with test automation frameworks?
2. Have you built test automation frameworks from scratch?
3. Experience with API testing?
4. When would you be available to start?

Best,
Sarah
```

### Agent Response

```
Hi Sarah,

Thank you for the additional details. FinanceFlow sounds like an 
exciting opportunity, and the challenges you mentioned are areas where 
I have strong experience.

To answer your questions:

1. I have 10+ years of experience designing and implementing test 
automation frameworks, primarily using Java, Selenium, and TestNG/JUnit.

2. Yes, I've built several test automation frameworks from scratch. 
Most recently, I architected a modular framework that reduced test 
execution time by 60% and improved test reliability significantly.

3. Extensive API testing experience using Rest Assured, Postman, and 
custom Java frameworks. I've automated end-to-end workflows covering 
both UI and API layers.

4. I'm currently employed and would need to provide 2 weeks notice. 
Assuming a good mutual fit, I could start approximately 3 weeks from 
an accepted offer.

I'm interested in moving forward. What would be the next steps?

Best regards,
Elena
```

**Why this response:**
- ✅ Direct answers to each question
- ✅ Provides specific examples and metrics
- ✅ Demonstrates relevant experience
- ✅ Manages expectations on timeline
- ✅ Moves conversation forward

---

## Example 4: Salary Discussion (ESCALATION)

### Incoming Email

```
Subject: Re: Senior Automation Engineer - Remote - Up to $140k

Hi Elena,

Your experience is exactly what we're looking for! The team is excited 
to move forward.

Based on your experience, we're thinking $125k base + equity (0.1%) 
+ full benefits. Does this work for you?

I'd like to set up a technical interview with the VP of Engineering 
next week. Are you available Tuesday or Wednesday afternoon?

Best,
Sarah
```

### Agent Response

```
Hi Sarah,

Thank you for the offer details and interview invitation. I appreciate 
the team's interest.

I'd like to review the complete compensation package carefully before 
moving forward with interviews. Could you provide:

- Full details on the equity package (vesting schedule, current valuation)
- Complete benefits breakdown
- Any performance bonuses or other compensation

Regarding timing, I'll need to review everything and will get back to 
you within 24 hours with my thoughts and availability for next steps.

Best regards,
Elena
```

**Behind the scenes:**

```
🚨 ESCALATION TRIGGERED
Reason: Salary negotiation
Thread ID: <thread_id>
Stage: negotiation

Agent Action:
1. Sent professional holding response
2. Logged escalation
3. Email notification sent to Elena
4. Awaiting human decision

Recommended next steps:
- Review the offer ($125k vs your target $120-150k)
- Evaluate equity package
- Decide if you want to negotiate higher
- Confirm interview availability
```

---

## Example 5: Clearly Not a Match

### Incoming Email

```
Subject: Junior QA Tester Position - $45k - Onsite

Hi,

We have an entry-level QA testing position available at our office 
in Nebraska. Starting salary $45k. Manual testing, no automation 
required.

Let me know if interested.

Thanks
```

### Agent Response

```
Hi,

Thank you for thinking of me for this opportunity. However, I'm 
currently seeking senior-level automation architecture roles with 
remote options, which doesn't align with this position.

I appreciate you reaching out and wish you the best in finding the 
right candidate.

Best regards,
Elena
```

**Why this response:**
- ✅ Polite decline
- ✅ Clear about mismatch
- ✅ Professional and brief
- ✅ Leaves positive impression

**Agent Logic:**
```python
# Auto-decline triggered:
- Title doesn't contain required keywords (architect, senior, lead)
- Salary below minimum threshold ($45k < $100k)
- No remote option (onsite only)

Decision: Auto-decline with polite response
```

---

## Example 6: Spam/Scam Detection

### Incoming Email

```
Subject: URGENT: $200K REMOTE JOB!!!

Dear Applicant,

CONGRATULATIONS! You have been selected for a $200,000 remote position!

To proceed, please send your:
- Social Security Number
- Bank account details
- $50 processing fee

REPLY IMMEDIATELY!!!
```

### Agent Response

```
None - Flagged as spam/scam
```

**Agent Logic:**
```python
# Spam detection:
- Excessive caps and exclamation marks
- Unrealistic salary for cold contact
- Requests sensitive personal information
- Requests money
- Generic greeting ("Dear Applicant")

Decision: Mark as spam, do NOT respond
Action: Log and move to spam folder
```

---

## Example 7: LinkedIn Message

### Incoming LinkedIn Message

```
Hi Elena, I noticed your impressive background in test automation. 
Are you open to new opportunities? We're hiring a Lead Automation 
Architect for a Fortune 500 company. Would love to connect!
```

### Agent Response

```
Hi [Name],

Thanks for reaching out! I'm always open to hearing about interesting 
opportunities in automation architecture.

Could you share more details about the role, including:
- Company name
- Remote/hybrid/onsite arrangement
- Salary range
- Key responsibilities

Feel free to email me at elena@email.com for a more detailed discussion.

Best,
Elena
```

---

## Response Customization

All responses are customizable via `config/prompts.yaml`.

### Adjust Tone

```yaml
communication_style:
  tone: "professional"  # or "casual", "formal", "friendly"
  formality: "medium"   # or "high", "low"
  response_length: "concise"  # or "detailed", "brief"
```

### Custom Templates

```yaml
email_templates:
  initial_response: |
    Hi {recruiter_name},
    
    [Your custom template here]
    
    Best regards,
    Elena
```

### Auto-Decline Rules

```yaml
auto_decline:
  salary_below: 100000
  keywords: ["unpaid", "internship", "volunteer"]
  contract_length_under_months: 6
```

---

## SMS-Specific Responses

SMS requires brevity (160 chars):

### Good SMS Response

```
Hi! Thanks for reaching out about the TCS role. Very interested! 
Could you email details to elena@email.com? Salary range & 
remote options? Thanks! -Elena
```

(159 characters)

### Too Long (Will be Split)

```
Hi Alex, thank you so much for reaching out to me about this 
opportunity. I am definitely interested in learning more about 
the Java Selenium Automation Architect position with TCS. Could 
you please send me more details including the full job description, 
salary range, benefits, and information about remote work options?
```

(This would be split into 2-3 messages)

---

## Multi-Turn Conversation Example

### Turn 1: Initial Contact
**Recruiter:** "Hi, I have a senior automation role..."
**Agent:** "Thanks! Could you share more details about..."

### Turn 2: Information Gathering
**Recruiter:** "Sure! Here are the details... [details]"
**Agent:** "Great! That aligns with my experience. A few more questions..."

### Turn 3: Screening
**Recruiter:** "Do you have experience with..."
**Agent:** "Yes, I have 10+ years with... [specific examples]"

### Turn 4: Scheduling (ESCALATION)
**Recruiter:** "Perfect! Can you interview next Tuesday?"
**Agent:** "I'm interested in moving forward. Let me check my calendar and get back to you within 24 hours."
**[ESCALATION EMAIL SENT TO YOU]**

### You Take Over
You review, confirm availability, and the agent helps schedule or you handle it manually.

---

## Tips for Best Results

1. **Keep profile.yaml updated** - Agent uses this info
2. **Review logs regularly** - Check `logs/conversations/`
3. **Refine prompts** - Adjust tone in `prompts.yaml`
4. **Monitor escalations** - Check `logs/escalations.log` daily
5. **Test with old emails** - Use past recruiter emails to test responses

---

## Testing Your Responses

```python
# Test mode in main.py
python main.py --once --test-mode

# This will:
# 1. Process emails but NOT send responses
# 2. Show what it WOULD send
# 3. Let you approve before enabling auto-reply
```

---

Happy job hunting! Let the AI handle the grunt work. 🚀

