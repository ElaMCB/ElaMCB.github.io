# SMS Setup Guide

Two approaches: **Free** (email-to-SMS gateway) or **Paid** (Twilio)

## Option 1: Free Email-to-SMS Gateway (Recommended)

Major carriers provide free email-to-SMS gateways. No account needed!

### How It Works

1. Recruiter sends you an SMS
2. It arrives as an email (if they use certain services)
3. Agent detects it and processes it
4. Agent replies by sending email to `phonenumber@carrier.com`
5. Recruiter receives it as SMS

### Supported Carriers

| Carrier | Gateway Address | Example |
|---------|-----------------|---------|
| AT&T | @txt.att.net | 5551234567@txt.att.net |
| T-Mobile | @tmomail.net | 5551234567@tmomail.net |
| Verizon | @vtext.com | 5551234567@vtext.com |
| Sprint | @messaging.sprintpcs.com | 5551234567@messaging.sprintpcs.com |
| Boost | @sms.myboostmobile.com | 5551234567@sms.myboostmobile.com |
| Cricket | @mms.cricketwireless.net | 5551234567@mms.cricketwireless.net |
| Google Fi | @msg.fi.google.com | 5551234567@msg.fi.google.com |

### Configuration

Edit `.env`:

```bash
# Default carrier gateway
SMS_EMAIL_GATEWAY=@txt.att.net
```

### Usage

The agent automatically:
1. Detects incoming SMS (as emails)
2. Extracts phone number
3. Generates response
4. Sends via email-to-SMS gateway

### Limitations

❌ **Not all SMS come as emails** - Only certain business SMS services
❌ **Need to know carrier** - Must know recruiter's carrier for replies
❌ **No delivery confirmation** - Can't confirm SMS was delivered
❌ **Character limits** - 160 characters per message

### When This Works

✅ Recruiters using mass texting services (like the one in your example)
✅ SMS from VoIP services
✅ Automated recruiting platforms

### Example: Replying to the Recruiter

The recruiter Alex sent:
> "Hi Elena, this is Alex... Text CALL to receive a call back..."

If you can find out their carrier, the agent can reply:

```python
# Agent automatically does this:
agent.send_sms(
    phone_number="1234567890",  # Alex's number
    message="Hi Alex! Thanks for reaching out. Could you share more details about the TCS role via email? elena@example.com",
    carrier="att"  # or detected from response
)
```

## Option 2: Twilio (Paid, More Reliable)

For full SMS automation with any carrier.

### Costs

- Phone number: ~$1.00/month
- Incoming SMS: $0.0075 per message
- Outgoing SMS: $0.0075 per message

**Total for job hunting:** ~$5-10/month (handling 100+ messages)

### Setup

1. **Sign up at [twilio.com](https://www.twilio.com/)**

2. **Get credentials:**
   - Account SID
   - Auth Token

3. **Buy a phone number:**
   - Go to Phone Numbers > Buy a Number
   - Choose a local number
   - Cost: ~$1/month

4. **Configure webhook (for incoming SMS):**

   You need a server to receive webhooks. Options:
   - **Ngrok** (for testing): Free tunneling
   - **Flask on cloud**: Deploy on Render/Railway (free tier)
   - **Skip incoming**: Just send SMS, don't receive

5. **Update configuration:**

   ```bash
   # In .env
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=+15551234567
   SMS_PROVIDER=twilio
   ```

### Using Twilio in Code

```python
from agents.sms_agent import TwilioSMSAgent

agent = TwilioSMSAgent(
    account_sid=os.getenv('TWILIO_ACCOUNT_SID'),
    auth_token=os.getenv('TWILIO_AUTH_TOKEN'),
    from_number=os.getenv('TWILIO_PHONE_NUMBER')
)

# Send SMS
agent.send_sms(
    to_number="+15551234567",
    message="Hi! Thanks for reaching out about the role."
)
```

### Webhook Setup (for Receiving SMS)

Create a Flask endpoint:

```python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

@app.route("/sms-webhook", methods=['POST'])
def handle_sms():
    from_number = request.form['From']
    message_body = request.form['Body']
    
    # Process with orchestrator
    response_text = orchestrator.process_sms(from_number, message_body)
    
    # Reply
    resp = MessagingResponse()
    resp.message(response_text)
    return str(resp)
```

Deploy this Flask app and set the webhook URL in Twilio console.

### Ngrok (for Testing Webhooks Locally)

```bash
# Install ngrok
# Download from https://ngrok.com/

# Run your Flask app
python webhook_server.py

# In another terminal, tunnel to it
ngrok http 5000

# Copy the https URL (e.g., https://abc123.ngrok.io)
# Paste in Twilio console as webhook URL
```

## Option 3: Google Voice (Limited Free)

Google Voice can forward SMS to email, but:
- US only
- Manual setup
- Limited automation capabilities
- Not recommended for production

## Recommendation

### For Starting Out:
Use **email-to-SMS gateway** (Option 1)
- Completely free
- Works for many recruiting services
- Easy setup

### For Serious Automation:
Use **Twilio** (Option 2)
- Reliable
- Works with any carrier
- Better control
- Only ~$5-10/month

## Handling the Specific Message

For Alex's message ("Text CALL to receive a call back"):

### Automated Response Strategy:

```
Hi Alex! Thanks for reaching out about the Java Selenium Automation 
Architect role with TCS. I'd prefer to discuss details via email first. 
Could you send more info to elena@example.com? Thanks!
```

This:
✅ Acknowledges the message
✅ Shows interest
✅ Redirects to email (easier to automate)
✅ Professional and brief (fits in SMS)

### Or, to get on the call:

```
CALL
```

Then handle the phone call (see voice_agent.py for voice automation options).

## SMS Best Practices

1. **Keep it brief** - Under 160 chars ideally
2. **Be professional** - Recruiters may be automated too
3. **Redirect to email** - Easier for detailed discussions
4. **Include your email** - So they can follow up
5. **Respect STOP** - Agent automatically handles unsubscribe

## Testing

Test the SMS agent:

```python
python agents/sms_agent.py
```

This will show:
- Supported carriers
- Example usage
- Gateway addresses

## Integration with Main Agent

The orchestrator automatically:
1. Checks for SMS (as emails) during each cycle
2. Processes them with the LLM
3. Generates appropriate responses
4. Sends replies via configured method

No manual intervention needed once configured!

## Security Note

⚠️ **SMS is less secure than email:**
- Can be spoofed
- No encryption
- Carrier depends on security

Always verify important details via email or phone call.

## Summary

| Feature | Email-to-SMS | Twilio | Google Voice |
|---------|--------------|--------|--------------|
| Cost | Free | ~$5-10/month | Free |
| Reliability | Medium | High | Low |
| Setup | Easy | Medium | Easy |
| Automation | Limited | Full | Limited |
| **Recommendation** | Start here | Upgrade later | Skip |

Start with free email-to-SMS, upgrade to Twilio if you get lots of recruiter texts!

