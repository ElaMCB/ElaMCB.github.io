"""
SMS Agent for handling text messages from recruiters
Free implementation using email-to-SMS gateways
"""

import os
import re
from typing import Dict, List, Optional
from datetime import datetime


class SMSAgent:
    """
    Handles SMS communication using email-to-SMS gateways
    
    This is a FREE alternative to Twilio. Major carriers provide email-to-SMS gateways:
    - AT&T: @txt.att.net
    - T-Mobile: @tmomail.net
    - Verizon: @vtext.com
    - Sprint: @messaging.sprintpcs.com
    - Google Fi: @msg.fi.google.com
    """
    
    # Carrier email-to-SMS gateways
    CARRIER_GATEWAYS = {
        'att': '@txt.att.net',
        't-mobile': '@tmomail.net',
        'verizon': '@vtext.com',
        'sprint': '@messaging.sprintpcs.com',
        'boost': '@sms.myboostmobile.com',
        'cricket': '@mms.cricketwireless.net',
        'uscellular': '@email.uscc.net',
        'google-fi': '@msg.fi.google.com',
    }
    
    def __init__(self, email_agent, default_gateway: str = '@txt.att.net'):
        """
        Initialize SMS agent
        
        Args:
            email_agent: EmailAgent instance to use for sending
            default_gateway: Default carrier gateway to use
        """
        self.email_agent = email_agent
        self.default_gateway = default_gateway
        self.phone_to_email_cache = {}  # Cache phone number to email mappings
    
    def send_sms(self, phone_number: str, message: str, carrier: Optional[str] = None) -> bool:
        """
        Send SMS via email-to-SMS gateway
        
        Args:
            phone_number: Recipient phone number (10 digits)
            message: Message to send (keep under 160 chars for SMS)
            carrier: Carrier name (e.g., 'att', 't-mobile') or None for default
            
        Returns:
            True if sent successfully
        """
        # Clean phone number
        phone_number = self._clean_phone_number(phone_number)
        
        if not phone_number:
            print("Invalid phone number")
            return False
        
        # Get carrier gateway
        if carrier and carrier.lower() in self.CARRIER_GATEWAYS:
            gateway = self.CARRIER_GATEWAYS[carrier.lower()]
        else:
            gateway = self.default_gateway
        
        # Create email address
        sms_email = f"{phone_number}{gateway}"
        
        # Keep message under SMS limit
        if len(message) > 160:
            print(f"Warning: Message exceeds 160 chars ({len(message)}). May be split into multiple texts.")
        
        # Send via email
        # Note: No subject and thread_id for SMS
        from email.mime.text import MIMEText
        import base64
        
        try:
            mime_message = MIMEText(message)
            mime_message['to'] = sms_email
            mime_message['subject'] = ''  # No subject for SMS
            
            raw_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode('utf-8')
            
            send_message = {'raw': raw_message}
            
            result = self.email_agent.service.users().messages().send(
                userId='me',
                body=send_message
            ).execute()
            
            print(f"SMS sent to {phone_number} via {gateway}")
            return True
            
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return False
    
    def parse_incoming_sms(self, email_data: Dict) -> Optional[Dict]:
        """
        Parse an SMS that came in as an email
        
        Args:
            email_data: Email data from EmailAgent
            
        Returns:
            Dict with SMS data or None if not an SMS
        """
        sender = email_data.get('from', '')
        
        # Check if this is from an SMS gateway
        if not any(gateway in sender for gateway in self.CARRIER_GATEWAYS.values()):
            return None
        
        # Extract phone number from email
        phone_match = re.search(r'(\d{10})', sender)
        if not phone_match:
            return None
        
        phone_number = phone_match.group(1)
        
        # Get message body (SMS come as plain text)
        body = email_data.get('body', '').strip()
        
        # Remove email artifacts
        body = self._clean_sms_body(body)
        
        return {
            'phone_number': phone_number,
            'message': body,
            'timestamp': email_data.get('date'),
            'raw_email': email_data
        }
    
    def _clean_phone_number(self, phone: str) -> Optional[str]:
        """Extract and format 10-digit phone number"""
        # Remove all non-digit characters
        digits = re.sub(r'\D', '', phone)
        
        # Handle different formats
        if len(digits) == 11 and digits[0] == '1':
            # Remove leading 1 (US country code)
            digits = digits[1:]
        
        if len(digits) == 10:
            return digits
        
        return None
    
    def _clean_sms_body(self, body: str) -> str:
        """Clean SMS body of email artifacts"""
        # Remove common email footers
        lines = body.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Stop at email artifacts
            if any(marker in line.lower() for marker in [
                'sent from', 'sent via', 'unsubscribe', 'privacy policy',
                'free msg', 'message and data rates'
            ]):
                break
            
            if line:
                cleaned_lines.append(line)
        
        return ' '.join(cleaned_lines)
    
    def detect_carrier_from_response(self, email_data: Dict) -> Optional[str]:
        """Try to detect carrier from response email"""
        sender = email_data.get('from', '')
        
        for carrier, gateway in self.CARRIER_GATEWAYS.items():
            if gateway in sender:
                return carrier
        
        return None
    
    def reply_to_sms(self, original_email_data: Dict, reply_message: str) -> bool:
        """
        Reply to an SMS that came via email
        
        Args:
            original_email_data: The original email data containing the SMS
            reply_message: Reply message to send
            
        Returns:
            True if sent successfully
        """
        sms_data = self.parse_incoming_sms(original_email_data)
        
        if not sms_data:
            print("Cannot reply: original message was not an SMS")
            return False
        
        # Detect carrier from original message
        carrier = self.detect_carrier_from_response(original_email_data)
        
        # Send reply
        return self.send_sms(
            phone_number=sms_data['phone_number'],
            message=reply_message,
            carrier=carrier
        )
    
    def handle_special_keywords(self, message: str) -> Optional[str]:
        """
        Handle special SMS keywords like STOP, CALL
        
        Returns:
            Action to take or None
        """
        message_upper = message.strip().upper()
        
        if message_upper == 'STOP':
            return 'unsubscribe'
        elif message_upper == 'CALL':
            return 'request_call'
        elif message_upper in ['HELP', 'INFO']:
            return 'help'
        
        return None


# Alternative: Twilio integration for those who want to use it
# This requires a paid account or trial credits

class TwilioSMSAgent:
    """
    SMS Agent using Twilio (PAID service, but more reliable)
    
    Setup:
    1. Sign up at twilio.com
    2. Get Account SID and Auth Token
    3. Buy a phone number (~$1/month + usage)
    """
    
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        try:
            from twilio.rest import Client
            self.client = Client(account_sid, auth_token)
            self.from_number = from_number
        except ImportError:
            raise ImportError("Twilio not installed. Run: pip install twilio")
    
    def send_sms(self, to_number: str, message: str) -> bool:
        """Send SMS via Twilio"""
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            print(f"SMS sent via Twilio: {message.sid}")
            return True
        except Exception as e:
            print(f"Twilio error: {e}")
            return False
    
    def setup_webhook(self, webhook_url: str):
        """
        Setup webhook for incoming messages
        
        Note: Requires Flask/FastAPI app running to receive webhooks
        """
        # This would be configured in Twilio console
        # Point to your server endpoint that handles incoming SMS
        pass


if __name__ == "__main__":
    # Test SMS functionality
    print("SMS Agent - Free Email-to-SMS Gateway")
    print("\nSupported carriers:")
    
    agent = SMSAgent(None)  # Would need real email agent
    
    for carrier, gateway in agent.CARRIER_GATEWAYS.items():
        print(f"  - {carrier}: {gateway}")
    
    print("\nExample usage:")
    print("  agent.send_sms('5551234567', 'Hi, this is Elena. Thanks for reaching out!', carrier='att')")
    
    print("\nNote: For SMS replies, you need to know the recruiter's carrier.")
    print("Most recruiters will include carrier info in their signature or you can detect it from their response.")

