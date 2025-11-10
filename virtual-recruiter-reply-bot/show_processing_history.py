"""
Show ARIA's processing history with timestamps
"""

import sqlite3
import json
from datetime import datetime

db_path = 'data/conversations.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("="*80)
print("ARIA PROCESSING HISTORY")
print("="*80)
print()

# Get all conversations with details
cursor.execute("""
    SELECT thread_id, company, recruiter_name, position, stage,
           created_at, updated_at, conversation_history
    FROM conversations
    ORDER BY created_at DESC
""")

conversations = cursor.fetchall()

print(f"Total Emails Processed: {len(conversations)}")
print()

for i, conv in enumerate(conversations, 1):
    thread_id, company, recruiter, position, stage, created, updated, history_json = conv
    
    # Parse history
    try:
        history = json.loads(history_json)
        first_msg = history[0] if history else {}
        metadata = first_msg.get('metadata', {})
    except:
        metadata = {}
    
    from_name = metadata.get('from_name', 'Unknown')
    subject = metadata.get('subject', 'No subject')
    
    print(f"{i}. {from_name}")
    print(f"   Subject: {subject[:60]}{'...' if len(subject) > 60 else ''}")
    print(f"   Processed: {created}")
    print(f"   Status: {stage}")
    
    if company or position or recruiter:
        print(f"   Detected Info:")
        if company:
            print(f"     - Company: {company}")
        if position:
            print(f"     - Position: {position}")
        if recruiter:
            print(f"     - Recruiter: {recruiter}")
    
    print()

print("="*80)
print()
print("HOW TO VIEW IN GMAIL:")
print("-"*80)
print("Search method (easiest):")
print("  1. Go to Gmail")
print("  2. Search box: label:ai-recruiter-processed")
print("  3. Press Enter")
print()
print("Sidebar method:")
print("  1. Gmail left sidebar")
print("  2. Scroll down to labels section")
print("  3. Look for 'AI-Recruiter'")
print("  4. Click the arrow to expand")
print("  5. Click 'Processed'")
print()
print("="*80)

conn.close()

