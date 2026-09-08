"""
Label the remaining recruiter emails that were tracked but not labeled
"""

from agents.email_agent import EmailAgent

agent = EmailAgent()

# Emails that should be labeled but might not be
searches = [
    ('from:indeed.com subject:Addison', 'Indeed - Addison Group QA Engineer'),
    ('from:glassdoor subject:Parsons', 'Glassdoor - Parsons QA Manager'),
    ('from:glassdoor subject:community', 'Glassdoor Community'),
]

print("Labeling remaining recruiter emails...")
print("="*80)

for query, description in searches:
    try:
        results = agent.service.users().messages().list(
            userId='me',
            q=query,
            maxResults=1
        ).execute()
        
        messages = results.get('messages', [])
        if messages:
            msg_id = messages[0]['id']
            agent.add_label(msg_id, 'AI-Recruiter/Processed')
            print(f"[+] {description} - Labeled")
        else:
            print(f"[-] {description} - Not found")
    except Exception as e:
        print(f"[!] {description} - Error: {e}")

print("="*80)
print("\nDone! Check Gmail with: label:ai-recruiter-processed")

