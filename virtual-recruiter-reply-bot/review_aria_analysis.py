"""
Review what ARIA analyzed and what responses it would send
"""

import sqlite3
import json

# Connect to database
db_path = 'data/conversations.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 80)
print("ARIA'S ANALYSIS OF YOUR RECRUITER EMAILS")
print("=" * 80)
print()

# Get all conversations
cursor.execute("""
    SELECT thread_id, company, recruiter_name, position, stage, 
           conversation_history, requires_escalation, escalation_reason
    FROM conversations
    ORDER BY created_at DESC
""")

conversations = cursor.fetchall()

print(f"Total Recruiter Emails Analyzed: {len(conversations)}")
print()
print("=" * 80)

for i, conv in enumerate(conversations, 1):
    thread_id, company, recruiter_name, position, stage, history_json, escalation, reason = conv
    
    print(f"\n{i}. CONVERSATION {i}")
    print("-" * 80)
    
    # Parse conversation history
    try:
        history = json.loads(history_json) if history_json else []
    except:
        history = []
    
    # Get first message
    if history and len(history) > 0:
        first_msg = history[0]
        metadata = first_msg.get('metadata', {})
        
        print(f"FROM: {metadata.get('from_name', 'Unknown')}")
        print(f"EMAIL: {metadata.get('from', '')}")
        print(f"SUBJECT: {metadata.get('subject', '')}")
        print()
        
        # Show snippet of content
        content = first_msg.get('content', '')
        preview = content[:300] + "..." if len(content) > 300 else content
        print(f"MESSAGE PREVIEW:")
        print(preview)
        print()
    
    print(f"ARIA's ANALYSIS:")
    print(f"  Company: {company or 'Not detected'}")
    print(f"  Position: {position or 'Not detected'}")
    print(f"  Recruiter: {recruiter_name or 'Not detected'}")
    print(f"  Stage: {stage}")
    print(f"  Needs Your Attention: {'YES - ' + str(reason) if escalation else 'NO'}")
    print()
    
    # Show responses if any
    outgoing_messages = [msg for msg in history if msg.get('direction') == 'outgoing']
    
    if outgoing_messages:
        print(f"ARIA WOULD SEND:")
        print("-" * 40)
        for msg in outgoing_messages:
            print(msg.get('content', ''))
        print("-" * 40)
    else:
        print(f"STATUS: ARIA has not generated a response yet")
        print(f"        (Marked for escalation or waiting for approval)")
    
    print()
    print("=" * 80)

conn.close()

print()
print("IMPORTANT:")
print("-" * 80)
print("ARIA has NOT sent any responses yet!")
print("All emails are just ANALYZED and LABELED in Gmail.")
print()
print("ARIA is in APPROVAL MODE - you review before anything is sent.")
print()
print("Next steps:")
print("1. Review the analysis above")
print("2. Check the 'AI-Recruiter/Processed' label in Gmail")
print("3. Decide which opportunities to pursue")
print("4. Run ARIA in daemon mode when ready to automate")
print()
print("=" * 80)

