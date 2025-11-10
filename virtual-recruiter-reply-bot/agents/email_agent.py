"""
Email Agent for handling recruiter emails via Gmail API
"""

import os
import base64
import re
from typing import List, Dict, Optional
from datetime import datetime
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class EmailAgent:
    """Handles email communication with recruiters"""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    
    def __init__(self, credentials_path: str = "credentials/gmail_credentials.json",
                 token_path: str = "credentials/gmail_token.json"):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        # Check if token already exists
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
        
        # If no valid credentials, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_path):
                    raise FileNotFoundError(
                        f"Gmail credentials not found at {self.credentials_path}. "
                        "Please follow the setup guide in docs/gmail_setup.md"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            os.makedirs(os.path.dirname(self.token_path), exist_ok=True)
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
    
    def get_unread_recruiter_emails(self, max_results: int = 10) -> List[Dict]:
        """
        Fetch unread emails that appear to be from recruiters
        
        Returns list of dicts with:
            - id: Email ID
            - thread_id: Thread ID
            - from: Sender email
            - from_name: Sender name
            - subject: Email subject
            - body: Email body (plain text)
            - date: Received date
            - labels: Gmail labels
        """
        try:
            # Search for unread emails
            query = "is:unread"
            
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            email_list = []
            for msg in messages:
                email_data = self._parse_email(msg['id'])
                
                # Filter for recruiter emails (basic heuristics)
                if self._is_likely_recruiter(email_data):
                    email_list.append(email_data)
            
            return email_list
            
        except HttpError as error:
            print(f"Gmail API error: {error}")
            return []
    
    def _parse_email(self, msg_id: str) -> Dict:
        """Parse email message and extract relevant data"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            
            # Extract headers
            email_data = {
                'id': msg_id,
                'thread_id': message['threadId'],
                'labels': message.get('labelIds', []),
                'snippet': message.get('snippet', ''),
            }
            
            for header in headers:
                name = header['name'].lower()
                value = header['value']
                
                if name == 'from':
                    # Parse "Name <email@domain.com>" format
                    match = re.match(r'(.+?)\s*<(.+?)>', value)
                    if match:
                        email_data['from_name'] = match.group(1).strip()
                        email_data['from'] = match.group(2).strip()
                    else:
                        email_data['from'] = value
                        email_data['from_name'] = value
                
                elif name == 'subject':
                    email_data['subject'] = value
                
                elif name == 'date':
                    email_data['date'] = value
            
            # Extract body
            email_data['body'] = self._get_email_body(message['payload'])
            
            return email_data
            
        except HttpError as error:
            print(f"Error parsing email {msg_id}: {error}")
            return {}
    
    def _get_email_body(self, payload: Dict) -> str:
        """Extract plain text body from email payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                        break
                elif part['mimeType'] == 'multipart/alternative' and 'parts' in part:
                    body = self._get_email_body(part)
                    if body:
                        break
        else:
            if 'body' in payload and 'data' in payload['body']:
                body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
        
        return body
    
    def _is_likely_recruiter(self, email_data: Dict) -> bool:
        """Heuristic to identify recruiter emails"""
        
        sender = email_data.get('from', '').lower()
        from_name = email_data.get('from_name', '').lower()
        subject = email_data.get('subject', '').lower()
        body = email_data.get('body', '').lower()
        
        # Exclude known non-recruiter domains (financial, marketing, etc.)
        excluded_domains = [
            'robinhood', 'lenscrafters', 'amazon', 'walmart', 'target',
            'bestbuy', 'ebay', 'paypal', 'venmo', 'chase', 'bankofamerica',
            'wellsfargo', 'citibank', 'capitalone', 'discover', 'americanexpress',
            'netflix', 'spotify', 'hulu', 'disney', 'apple', 'google.com',
            'facebook', 'instagram', 'twitter', 'tiktok', 'snapchat',
            'uber', 'lyft', 'doordash', 'grubhub', 'instacart'
        ]
        
        # If from excluded domain, not a recruiter
        if any(domain in sender for domain in excluded_domains):
            return False
        
        # Job board and recruiter domains (usually legitimate)
        recruiter_domains = [
            'indeed', 'linkedin', 'dice', 'glassdoor', 'ziprecruiter',
            'monster', 'careerbuilder', 'simplyhired', 'hired', 'angellist',
            'greenhouse', 'lever', 'workday', 'taleo', 'icims',
            'recruiting', 'talent', 'staffing', 'search', 'placement'
        ]
        
        # If from known recruiter domain, likely a recruiter
        if any(domain in sender or domain in from_name for domain in recruiter_domains):
            # Check if it's a specific job vs generic alert
            # Specific jobs mention company names and specific roles
            has_company_name = any(company in subject for company in [
                ' at ', ' with ', ' - ', 'company', 'corporation', 'group', 
                'systems', 'solutions', 'technologies', 'services', 'inc'
            ])
            
            # If subject has a company/role mentioned, it's specific enough
            if has_company_name:
                return True
            
            # Filter truly generic alerts
            very_generic = [
                'job alert for:', 'saved search:', 'your daily job', 
                'jobs you might like', 'based on your resume'
            ]
            
            if any(alert in subject for alert in very_generic):
                return False  # Too generic
            
            return True  # From recruiter domain, specific enough
        
        # Keywords that strongly suggest recruiter email (require multiple matches)
        strong_recruiter_keywords = [
            'recruiter', 'recruiting', 'talent acquisition', 'talent partner',
            'hr specialist', 'hiring manager', 'staffing', 'placement'
        ]
        
        combined_text = f"{subject} {from_name}"
        
        # If sender identifies as recruiter, it's a recruiter
        if any(keyword in combined_text for keyword in strong_recruiter_keywords):
            return True
        
        # Job-specific keywords in subject (not just body)
        job_keywords = [
            'position with', 'role with', 'opportunity with',
            'interview', 'job description', 'job opening',
            'we have an opening', 'reaching out to you for',
            'job title:', 'location:', 'pay:', 'salary:'
        ]
        
        # Check for job-specific language in subject
        subject_matches = sum(1 for keyword in job_keywords if keyword in subject)
        
        if subject_matches >= 2:  # Need at least 2 job keywords in subject
            return True
        
        return False
    
    def send_reply(self, thread_id: str, to: str, subject: str, body: str) -> bool:
        """
        Send a reply email
        
        Args:
            thread_id: Gmail thread ID to reply to
            to: Recipient email address
            subject: Email subject (will be prefixed with "Re: " if not already)
            body: Email body text
            
        Returns:
            True if sent successfully
        """
        try:
            # Ensure subject has Re: prefix
            if not subject.lower().startswith('re:'):
                subject = f"Re: {subject}"
            
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            # Add signature
            signature = "\n\n--\nElena\nJava Selenium Automation Architect"
            message.set_payload(message.get_payload() + signature)
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            send_message = {
                'raw': raw_message,
                'threadId': thread_id
            }
            
            result = self.service.users().messages().send(
                userId='me',
                body=send_message
            ).execute()
            
            print(f"Email sent successfully. Message ID: {result['id']}")
            return True
            
        except HttpError as error:
            print(f"Error sending email: {error}")
            return False
    
    def mark_as_read(self, msg_id: str):
        """Mark an email as read"""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
        except HttpError as error:
            print(f"Error marking email as read: {error}")
    
    def add_label(self, msg_id: str, label_name: str):
        """Add a custom label to an email"""
        try:
            # First, get or create the label
            label_id = self._get_or_create_label(label_name)
            
            if label_id:
                self.service.users().messages().modify(
                    userId='me',
                    id=msg_id,
                    body={'addLabelIds': [label_id]}
                ).execute()
        except HttpError as error:
            print(f"Error adding label: {error}")
    
    def _get_or_create_label(self, label_name: str) -> Optional[str]:
        """Get label ID or create if doesn't exist"""
        try:
            # Get all labels
            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            
            # Check if label exists
            for label in labels:
                if label['name'] == label_name:
                    return label['id']
            
            # Create new label
            label_object = {
                'name': label_name,
                'labelListVisibility': 'labelShow',
                'messageListVisibility': 'show'
            }
            
            created_label = self.service.users().labels().create(
                userId='me',
                body=label_object
            ).execute()
            
            return created_label['id']
            
        except HttpError as error:
            print(f"Error with label: {error}")
            return None
    
    def get_thread_messages(self, thread_id: str) -> List[Dict]:
        """Get all messages in a thread"""
        try:
            thread = self.service.users().threads().get(
                userId='me',
                id=thread_id
            ).execute()
            
            messages = []
            for msg in thread['messages']:
                messages.append(self._parse_email(msg['id']))
            
            return messages
            
        except HttpError as error:
            print(f"Error getting thread: {error}")
            return []


if __name__ == "__main__":
    # Test the email agent
    print("Testing Email Agent...")
    
    agent = EmailAgent()
    
    print("\nFetching unread recruiter emails...")
    emails = agent.get_unread_recruiter_emails(max_results=5)
    
    print(f"\nFound {len(emails)} recruiter emails:")
    for email in emails:
        print(f"\nFrom: {email.get('from_name')} <{email.get('from')}>")
        print(f"Subject: {email.get('subject')}")
        print(f"Date: {email.get('date')}")
        print(f"Preview: {email.get('snippet')[:100]}...")

