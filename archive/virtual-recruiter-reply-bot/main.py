"""
Main entry point for AI Recruiter Agent
"""

import os
import sys
import time
import argparse
from datetime import datetime
from dotenv import load_dotenv

from core.orchestrator import JobApplicationOrchestrator
from utils.logger import setup_logger

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logger()


def run_once(orchestrator: JobApplicationOrchestrator):
    """Run one iteration of message processing"""
    logger.info("=" * 60)
    logger.info(f"AI Recruiter Agent - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # Process new messages
        count = orchestrator.process_new_messages()
        
        if count > 0:
            logger.info(f"✓ Processed {count} message(s)")
        else:
            logger.info("No new messages")
        
        # Print status
        orchestrator.print_status()
        
    except Exception as e:
        logger.error(f"Error in processing: {e}")
        import traceback
        traceback.print_exc()


def run_daemon(orchestrator: JobApplicationOrchestrator, interval: int = 300):
    """Run agent continuously in daemon mode"""
    logger.info("Starting AI Recruiter Agent in daemon mode")
    logger.info(f"Check interval: {interval} seconds")
    logger.info("Press Ctrl+C to stop\n")
    
    try:
        while True:
            run_once(orchestrator)
            
            logger.info(f"\nNext check in {interval} seconds...")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        logger.info("\n\nStopping AI Recruiter Agent...")
        sys.exit(0)


def run_interactive(orchestrator: JobApplicationOrchestrator):
    """Run agent in interactive mode"""
    logger.info("AI Recruiter Agent - Interactive Mode")
    logger.info("Commands:")
    logger.info("  check  - Check for new messages")
    logger.info("  status - Show status report")
    logger.info("  list   - List all conversations")
    logger.info("  view <thread_id> - View conversation details")
    logger.info("  quit   - Exit")
    print()
    
    while True:
        try:
            command = input("\n> ").strip().lower()
            
            if command == "quit" or command == "exit":
                break
            
            elif command == "check":
                run_once(orchestrator)
            
            elif command == "status":
                orchestrator.print_status()
            
            elif command == "list":
                list_conversations(orchestrator)
            
            elif command.startswith("view "):
                thread_id = command.split(" ", 1)[1]
                view_conversation(orchestrator, thread_id)
            
            elif command == "help":
                logger.info("Available commands: check, status, list, view <thread_id>, quit")
            
            else:
                logger.info(f"Unknown command: {command}. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"Error: {e}")
    
    logger.info("\nGoodbye!")


def list_conversations(orchestrator: JobApplicationOrchestrator):
    """List all active conversations"""
    conversations = orchestrator.state_manager.get_active_conversations()
    
    if not conversations:
        print("\nNo active conversations")
        return
    
    print("\n" + "="*80)
    print(f"{'Thread ID':<25} {'Company':<20} {'Position':<25} {'Stage':<15}")
    print("="*80)
    
    for conv in conversations:
        thread_id = conv.thread_id[:23] + "..." if len(conv.thread_id) > 25 else conv.thread_id
        company = conv.company[:18] + "..." if len(conv.company) > 20 else conv.company
        position = conv.position[:23] + "..." if len(conv.position) > 25 else conv.position
        
        marker = "⚠️ " if conv.requires_escalation else ""
        print(f"{marker}{thread_id:<25} {company:<20} {position:<25} {conv.stage:<15}")
    
    print("="*80)


def view_conversation(orchestrator: JobApplicationOrchestrator, thread_id: str):
    """View details of a specific conversation"""
    state = orchestrator.state_manager.get_state(thread_id)
    
    if not state:
        print(f"\nConversation not found: {thread_id}")
        return
    
    print("\n" + "="*80)
    print(f"Conversation: {thread_id}")
    print("="*80)
    print(f"Company: {state.company}")
    print(f"Position: {state.position}")
    print(f"Recruiter: {state.recruiter_name}")
    print(f"Stage: {state.stage}")
    print(f"Channel: {state.channel}")
    print(f"Work Arrangement: {state.work_arrangement or 'Not specified'}")
    print(f"Salary Range: {state.salary_range or 'Not specified'}")
    print(f"Escalation: {'Yes - ' + state.escalation_reason if state.requires_escalation else 'No'}")
    print(f"Created: {state.created_at}")
    print(f"Updated: {state.updated_at}")
    
    print("\nConversation History:")
    print("-"*80)
    
    for msg in state.conversation_history:
        direction = msg.get('direction', 'unknown')
        content = msg.get('content', '')[:200]
        timestamp = msg.get('timestamp', '')
        
        arrow = "→" if direction == "outgoing" else "←"
        print(f"\n{arrow} [{direction.upper()}] {timestamp}")
        print(f"  {content}...")
    
    print("\n" + "="*80)


def setup_check(orchestrator: JobApplicationOrchestrator):
    """Check if setup is complete"""
    issues = []
    
    # Check Gmail credentials
    creds_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials/gmail_credentials.json')
    if not os.path.exists(creds_path):
        issues.append(f"Gmail credentials not found at {creds_path}")
    
    # Check LLM configuration
    llm_provider = os.getenv('LLM_PROVIDER', 'ollama')
    if llm_provider == 'ollama':
        try:
            import ollama
            # Try to ping Ollama
            ollama.list()
        except Exception as e:
            issues.append(f"Ollama not running or not installed. Run 'ollama serve' or install from https://ollama.ai")
    
    # Check profile configuration
    if not os.path.exists('config/profile.yaml'):
        issues.append("Profile configuration not found at config/profile.yaml")
    
    if issues:
        logger.error("\n⚠️  Setup Issues Found:")
        for issue in issues:
            logger.error(f"  - {issue}")
        logger.error("\nPlease resolve these issues before running the agent.")
        logger.error("See README.md for setup instructions.")
        return False
    
    logger.info("✓ Setup check passed")
    return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='AI Recruiter Agent - Automated job application assistant')
    parser.add_argument('--daemon', action='store_true', help='Run continuously in background')
    parser.add_argument('--once', action='store_true', help='Process messages once and exit')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--interval', type=int, default=300, help='Check interval in seconds (daemon mode)')
    parser.add_argument('--setup-check', action='store_true', help='Check if setup is complete')
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    try:
        orchestrator = JobApplicationOrchestrator()
    except Exception as e:
        logger.error(f"Failed to initialize: {e}")
        logger.error("Run with --setup-check to diagnose issues")
        sys.exit(1)
    
    # Setup check
    if args.setup_check or not setup_check(orchestrator):
        if args.setup_check:
            sys.exit(0)
        else:
            sys.exit(1)
    
    # Run based on mode
    if args.once:
        run_once(orchestrator)
    elif args.daemon:
        run_daemon(orchestrator, args.interval)
    elif args.interactive:
        run_interactive(orchestrator)
    else:
        # Default: run once
        logger.info("Running in single-check mode (use --daemon for continuous monitoring)")
        run_once(orchestrator)


if __name__ == "__main__":
    main()

