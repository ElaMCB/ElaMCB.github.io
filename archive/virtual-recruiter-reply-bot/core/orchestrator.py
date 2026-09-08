"""
Central Orchestrator - Coordinates all agents and manages conversation flow
"""

import os
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

from core.state_manager import StateManager, ConversationState
from core.llm_processor import LLMProcessor
from agents.email_agent import EmailAgent
from agents.sms_agent import SMSAgent


class JobApplicationOrchestrator:
    """
    Central coordinator for the AI recruiter agent
    
    Responsibilities:
    - Monitor all communication channels
    - Route messages to appropriate handlers
    - Maintain conversation state
    - Generate and send responses
    - Escalate when necessary
    """
    
    def __init__(self, config: Optional[Dict] = None):
        load_dotenv()
        
        self.config = config or self._load_config()
        
        # Initialize components
        self.state_manager = StateManager(
            db_path=os.getenv('DATABASE_PATH', 'data/conversations.db')
        )
        
        self.llm_processor = LLMProcessor(
            provider=os.getenv('LLM_PROVIDER', 'ollama'),
            model=os.getenv('OLLAMA_MODEL', 'llama2')
        )
        
        self.email_agent = EmailAgent(
            credentials_path=os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials/gmail_credentials.json'),
            token_path=os.getenv('GMAIL_TOKEN_PATH', 'credentials/gmail_token.json')
        )
        
        self.sms_agent = SMSAgent(
            email_agent=self.email_agent,
            default_gateway=os.getenv('SMS_EMAIL_GATEWAY', '@txt.att.net')
        )
        
        self.auto_reply_enabled = os.getenv('AUTO_REPLY_ENABLED', 'true').lower() == 'true'
        self.require_approval = os.getenv('REQUIRE_APPROVAL', 'false').lower() == 'true'
    
    def _load_config(self) -> Dict:
        """Load configuration from environment"""
        return {
            'check_interval': int(os.getenv('CHECK_INTERVAL_SECONDS', '300')),
            'auto_reply': os.getenv('AUTO_REPLY_ENABLED', 'true').lower() == 'true',
            'require_approval': os.getenv('REQUIRE_APPROVAL', 'false').lower() == 'true',
        }
    
    def process_new_messages(self) -> int:
        """
        Check all channels for new messages and process them
        
        Returns:
            Number of messages processed
        """
        processed_count = 0
        
        # Process emails
        processed_count += self._process_emails()
        
        # Process SMS (check for SMS emails)
        processed_count += self._process_sms()
        
        return processed_count
    
    def _process_emails(self) -> int:
        """Process new recruiter emails"""
        print("Checking for new emails...")
        
        emails = self.email_agent.get_unread_recruiter_emails()
        processed = 0
        
        for email in emails:
            email_id = email.get('id')
            thread_id = email.get('thread_id')
            
            try:
                print(f"\nProcessing email from {email.get('from_name')}: {email.get('subject')}")
                
                # Label email immediately so we know ARIA analyzed it
                self.email_agent.add_label(email_id, 'AI-Recruiter/Processed')
                
                # Get or create conversation state
                state = self.state_manager.get_state(thread_id)
                
                if not state:
                    # New conversation
                    state = self.state_manager.create_conversation(
                        thread_id=thread_id,
                        channel='email',
                        initial_message={
                            'timestamp': datetime.now(),
                            'channel': 'email',
                            'direction': 'incoming',
                            'content': email.get('body'),
                            'metadata': {
                                'from': email.get('from'),
                                'from_name': email.get('from_name'),
                                'subject': email.get('subject')
                            }
                        }
                    )
                else:
                    # Existing conversation - add message
                    self.state_manager.add_message(thread_id, {
                        'timestamp': datetime.now(),
                        'channel': 'email',
                        'direction': 'incoming',
                        'content': email.get('body'),
                        'metadata': email
                    })
                
                # Generate response
                response_data = self.llm_processor.generate_response(
                    message=email.get('body'),
                    channel='email',
                    conversation_state=state.__dict__ if hasattr(state, '__dict__') else {},
                    context={'email_metadata': email}
                )
                
                # Update state with extracted information
                updates = {
                    'stage': response_data.get('next_stage', state.stage)
                }
                
                extracted_info = response_data.get('extracted_info', {})
                if extracted_info.get('company'):
                    updates['company'] = extracted_info['company']
                if extracted_info.get('position'):
                    updates['position'] = extracted_info['position']
                if extracted_info.get('recruiter_name'):
                    updates['recruiter_name'] = extracted_info['recruiter_name']
                if extracted_info.get('salary_range'):
                    updates['salary_range'] = extracted_info['salary_range']
                if extracted_info.get('work_arrangement'):
                    updates['work_arrangement'] = extracted_info['work_arrangement']
                
                self.state_manager.update_state(thread_id, updates)
                
                # Check if escalation needed
                if response_data.get('requires_escalation'):
                    self.state_manager.mark_for_escalation(
                        thread_id,
                        response_data.get('escalation_reason', 'Unknown reason')
                    )
                    self._notify_escalation(thread_id, response_data)
                    processed += 1
                    continue
                
                # Send response if auto-reply enabled
                if self.auto_reply_enabled:
                    if self.require_approval:
                        self._request_approval(thread_id, response_data, email)
                    else:
                        self._send_email_response(thread_id, response_data, email)
                
                # Mark email as processed
                self.email_agent.mark_as_read(email.get('id'))
                self.email_agent.add_label(email.get('id'), 'AI-Recruiter/Processed')
                
                processed += 1
                
            except Exception as e:
                print(f"Error processing email: {e}")
                import traceback
                traceback.print_exc()
        
        return processed
    
    def _process_sms(self) -> int:
        """Process SMS messages (received as emails)"""
        print("Checking for SMS messages...")
        
        # Get emails that might be SMS
        all_emails = self.email_agent.get_unread_recruiter_emails(max_results=20)
        
        processed = 0
        for email in all_emails:
            sms_data = self.sms_agent.parse_incoming_sms(email)
            
            if not sms_data:
                continue
            
            try:
                print(f"\nProcessing SMS from {sms_data['phone_number']}")
                
                # Check for special keywords
                special_action = self.sms_agent.handle_special_keywords(sms_data['message'])
                
                if special_action == 'unsubscribe':
                    print("STOP keyword detected - marking conversation as declined")
                    # Handle unsubscribe
                    continue
                
                # Use phone number as thread_id for SMS
                thread_id = f"sms_{sms_data['phone_number']}"
                state = self.state_manager.get_state(thread_id)
                
                if not state:
                    state = self.state_manager.create_conversation(
                        thread_id=thread_id,
                        channel='sms',
                        initial_message={
                            'timestamp': datetime.now(),
                            'channel': 'sms',
                            'direction': 'incoming',
                            'content': sms_data['message'],
                            'metadata': {'phone': sms_data['phone_number']}
                        }
                    )
                else:
                    self.state_manager.add_message(thread_id, {
                        'timestamp': datetime.now(),
                        'channel': 'sms',
                        'direction': 'incoming',
                        'content': sms_data['message'],
                        'metadata': sms_data
                    })
                
                # Generate response
                response_data = self.llm_processor.generate_response(
                    message=sms_data['message'],
                    channel='sms',
                    conversation_state=state.__dict__ if hasattr(state, '__dict__') else {},
                    context={'sms_data': sms_data}
                )
                
                # Send SMS response if enabled
                if self.auto_reply_enabled and not response_data.get('requires_escalation'):
                    success = self.sms_agent.reply_to_sms(email, response_data['response'])
                    
                    if success:
                        self.state_manager.add_message(thread_id, {
                            'timestamp': datetime.now(),
                            'channel': 'sms',
                            'direction': 'outgoing',
                            'content': response_data['response']
                        })
                
                self.email_agent.mark_as_read(email.get('id'))
                processed += 1
                
            except Exception as e:
                print(f"Error processing SMS: {e}")
        
        return processed
    
    def _send_email_response(self, thread_id: str, response_data: Dict, original_email: Dict):
        """Send email response"""
        try:
            response_text = response_data.get('response', '')
            
            success = self.email_agent.send_reply(
                thread_id=thread_id,
                to=original_email.get('from'),
                subject=original_email.get('subject'),
                body=response_text
            )
            
            if success:
                # Log outgoing message
                self.state_manager.add_message(thread_id, {
                    'timestamp': datetime.now(),
                    'channel': 'email',
                    'direction': 'outgoing',
                    'content': response_text
                })
                
                print(f"✓ Response sent to {original_email.get('from_name')}")
            
        except Exception as e:
            print(f"Error sending response: {e}")
    
    def _request_approval(self, thread_id: str, response_data: Dict, original_email: Dict):
        """Request human approval before sending"""
        print("\n" + "="*60)
        print("APPROVAL REQUIRED")
        print("="*60)
        print(f"From: {original_email.get('from_name')} <{original_email.get('from')}>")
        print(f"Subject: {original_email.get('subject')}")
        print(f"\nProposed response:\n{response_data.get('response')}")
        print("="*60)
        
        # In production, this would send a notification or open a web UI
        # For now, just log it
        
        approval_file = 'data/pending_approvals.txt'
        os.makedirs('data', exist_ok=True)
        
        with open(approval_file, 'a') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Thread ID: {thread_id}\n")
            f.write(f"Time: {datetime.now()}\n")
            f.write(f"From: {original_email.get('from')}\n")
            f.write(f"Subject: {original_email.get('subject')}\n")
            f.write(f"\nResponse:\n{response_data.get('response')}\n")
    
    def _notify_escalation(self, thread_id: str, response_data: Dict):
        """Notify about escalation requirement"""
        print("\n" + "!"*60)
        print("ESCALATION REQUIRED")
        print("!"*60)
        print(f"Thread: {thread_id}")
        print(f"Reason: {response_data.get('escalation_reason', 'Unknown')}")
        print("!"*60)
        
        # In production, send email/SMS notification
        escalation_email = os.getenv('ESCALATION_EMAIL')
        if escalation_email:
            # Would send notification here
            pass
    
    def get_status_report(self) -> Dict:
        """Get status of all conversations"""
        active_conversations = self.state_manager.get_active_conversations()
        
        status = {
            'total_conversations': len(active_conversations),
            'by_stage': {},
            'requiring_escalation': [],
            'by_channel': {'email': 0, 'sms': 0, 'voice': 0}
        }
        
        for conv in active_conversations:
            # Count by stage
            stage = conv.stage
            status['by_stage'][stage] = status['by_stage'].get(stage, 0) + 1
            
            # Count by channel
            status['by_channel'][conv.channel] = status['by_channel'].get(conv.channel, 0) + 1
            
            # Track escalations
            if conv.requires_escalation:
                status['requiring_escalation'].append({
                    'thread_id': conv.thread_id,
                    'company': conv.company,
                    'position': conv.position,
                    'reason': conv.escalation_reason
                })
        
        return status
    
    def print_status(self):
        """Print formatted status report"""
        status = self.get_status_report()
        
        print("\n" + "="*60)
        print("AI RECRUITER AGENT - STATUS REPORT")
        print("="*60)
        print(f"Active Conversations: {status['total_conversations']}")
        
        print("\nBy Stage:")
        for stage, count in status['by_stage'].items():
            print(f"  {stage}: {count}")
        
        print("\nBy Channel:")
        for channel, count in status['by_channel'].items():
            if count > 0:
                print(f"  {channel}: {count}")
        
        if status['requiring_escalation']:
            print(f"\n⚠️  {len(status['requiring_escalation'])} conversation(s) require escalation:")
            for item in status['requiring_escalation']:
                print(f"  - {item['company']} - {item['position']}: {item['reason']}")
        
        print("="*60 + "\n")

