"""
Logging utility for AI Recruiter Agent
"""

import os
import logging
import colorlog
from datetime import datetime


def setup_logger(name: str = 'ai-recruiter', log_file: str = None, level: str = None) -> logging.Logger:
    """
    Setup colored console logger
    
    Args:
        name: Logger name
        log_file: Optional log file path
        level: Log level (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Configured logger
    """
    # Get log level from environment or use default
    if level is None:
        level = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Console handler with colors
    console_handler = colorlog.StreamHandler()
    console_handler.setLevel(level)
    
    console_format = colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)-8s%(reset)s %(message)s',
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file is None:
        log_file = os.getenv('LOG_FILE', 'logs/agent.log')
    
    if log_file:
        # Create log directory
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger


def log_conversation(thread_id: str, message: dict, direction: str):
    """
    Log a conversation message to a separate conversation log
    
    Args:
        thread_id: Conversation thread ID
        message: Message dict
        direction: 'incoming' or 'outgoing'
    """
    log_dir = 'logs/conversations'
    os.makedirs(log_dir, exist_ok=True)
    
    # Sanitize thread_id for filename
    safe_thread_id = thread_id.replace('/', '_').replace('\\', '_')
    log_file = os.path.join(log_dir, f'{safe_thread_id}.log')
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    arrow = "→" if direction == "outgoing" else "←"
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*80}\n")
        f.write(f"{timestamp} {arrow} {direction.upper()}\n")
        f.write(f"{'='*80}\n")
        f.write(f"{message.get('content', '')}\n")
        
        if message.get('metadata'):
            f.write(f"\nMetadata: {message['metadata']}\n")


def log_escalation(thread_id: str, reason: str, context: dict):
    """
    Log an escalation event
    
    Args:
        thread_id: Conversation thread ID
        reason: Escalation reason
        context: Additional context
    """
    log_file = 'logs/escalations.log'
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*80}\n")
        f.write(f"ESCALATION - {timestamp}\n")
        f.write(f"{'='*80}\n")
        f.write(f"Thread ID: {thread_id}\n")
        f.write(f"Reason: {reason}\n")
        f.write(f"\nContext:\n")
        for key, value in context.items():
            f.write(f"  {key}: {value}\n")
        f.write(f"{'='*80}\n")


if __name__ == "__main__":
    # Test logger
    logger = setup_logger()
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    
    print("\nLogger test complete. Check logs/agent.log")

