"""
Show all emails that ARIA has labeled
"""

from agents.email_agent import EmailAgent

print("="*80)
print("EMAILS LABELED BY ARIA")
print("="*80)
print()

agent = EmailAgent()

# Get the AI-Recruiter/Processed label
results = agent.service.users().labels().list(userId='me').execute()
labels = results.get('labels', [])

aria_label = None
for label in labels:
    if label['name'] == 'AI-Recruiter/Processed':
        aria_label = label
        break

if not aria_label:
    print("AI-Recruiter/Processed label not found!")
else:
    print(f"Label ID: {aria_label['id']}")
    print()
    
    # Get messages with this label
    results = agent.service.users().messages().list(
        userId='me',
        labelIds=[aria_label['id']],
        maxResults=20
    ).execute()
    
    messages = results.get('messages', [])
    
    print(f"Total Emails with 'AI-Recruiter/Processed' label: {len(messages)}")
    print()
    print("-"*80)
    
    for i, msg in enumerate(messages, 1):
        email_data = agent._parse_email(msg['id'])
        print(f"\n{i}. FROM: {email_data.get('from_name', 'Unknown')}")
        print(f"   SUBJECT: {email_data.get('subject', 'No subject')}")
        print(f"   DATE: {email_data.get('date', '')}")
    
    print()
    print("-"*80)
    print()
    print("TO SEE THESE IN GMAIL:")
    print("1. Go to Gmail web interface")
    print("2. In the search box at top, type: label:ai-recruiter-processed")
    print("3. Press Enter")
    print()
    print("OR")
    print()
    print("1. Look in left sidebar")
    print("2. Scroll down past Inbox/Sent")
    print("3. Find 'AI-Recruiter' and expand it")
    print("4. Click 'Processed' to see all labeled emails")
    print()
    print("="*80)

