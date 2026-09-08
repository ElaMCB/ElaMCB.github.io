"""
State Manager for tracking conversation context across channels
"""

import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import os


@dataclass
class ConversationState:
    """Represents the state of a conversation with a recruiter"""
    thread_id: str
    stage: str  # initial_contact, information_gathering, screening, negotiation, scheduling, declined
    channel: str  # email, sms, voice
    company: str
    recruiter_name: str
    position: str
    tech_stack: List[str]
    salary_range: Optional[str]
    work_arrangement: Optional[str]  # remote, hybrid, onsite
    location: Optional[str]
    created_at: datetime
    updated_at: datetime
    conversation_history: List[Dict]
    metadata: Dict
    requires_escalation: bool
    escalation_reason: Optional[str]


class StateManager:
    """Manages conversation state using SQLite"""
    
    def __init__(self, db_path: str = "data/conversations.db"):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create database and tables if they don't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                thread_id TEXT PRIMARY KEY,
                stage TEXT NOT NULL,
                channel TEXT NOT NULL,
                company TEXT,
                recruiter_name TEXT,
                position TEXT,
                tech_stack TEXT,
                salary_range TEXT,
                work_arrangement TEXT,
                location TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                conversation_history TEXT,
                metadata TEXT,
                requires_escalation INTEGER DEFAULT 0,
                escalation_reason TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id TEXT NOT NULL,
                timestamp TIMESTAMP,
                channel TEXT,
                direction TEXT,
                content TEXT,
                metadata TEXT,
                FOREIGN KEY (thread_id) REFERENCES conversations(thread_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_conversation(self, thread_id: str, channel: str, initial_message: Dict) -> ConversationState:
        """Create a new conversation state"""
        now = datetime.now()
        
        # Ensure timestamp is serializable
        if 'timestamp' in initial_message and isinstance(initial_message['timestamp'], datetime):
            initial_message['timestamp'] = initial_message['timestamp'].isoformat()
        
        state = ConversationState(
            thread_id=thread_id,
            stage="initial_contact",
            channel=channel,
            company="",
            recruiter_name="",
            position="",
            tech_stack=[],
            salary_range=None,
            work_arrangement=None,
            location=None,
            created_at=now,
            updated_at=now,
            conversation_history=[initial_message],
            metadata={},
            requires_escalation=False,
            escalation_reason=None
        )
        
        self._save_state(state)
        self._save_message(thread_id, initial_message)
        
        return state
    
    def get_state(self, thread_id: str) -> Optional[ConversationState]:
        """Retrieve conversation state by thread ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM conversations WHERE thread_id = ?
        """, (thread_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return self._row_to_state(row)
    
    def update_state(self, thread_id: str, updates: Dict) -> ConversationState:
        """Update conversation state"""
        state = self.get_state(thread_id)
        
        if not state:
            raise ValueError(f"Conversation {thread_id} not found")
        
        # Update fields
        for key, value in updates.items():
            if hasattr(state, key):
                setattr(state, key, value)
        
        state.updated_at = datetime.now()
        
        self._save_state(state)
        return state
    
    def add_message(self, thread_id: str, message: Dict):
        """Add a message to conversation history"""
        # Ensure timestamp is serializable
        if 'timestamp' in message and isinstance(message['timestamp'], datetime):
            message['timestamp'] = message['timestamp'].isoformat()
        
        state = self.get_state(thread_id)
        
        if state:
            state.conversation_history.append(message)
            state.updated_at = datetime.now()
            self._save_state(state)
        
        self._save_message(thread_id, message)
    
    def get_conversation_history(self, thread_id: str) -> List[Dict]:
        """Get all messages for a conversation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timestamp, channel, direction, content, metadata
            FROM messages
            WHERE thread_id = ?
            ORDER BY timestamp ASC
        """, (thread_id,))
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                'timestamp': row[0],
                'channel': row[1],
                'direction': row[2],
                'content': row[3],
                'metadata': json.loads(row[4]) if row[4] else {}
            })
        
        conn.close()
        return messages
    
    def get_active_conversations(self) -> List[ConversationState]:
        """Get all active (non-declined) conversations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM conversations
            WHERE stage != 'declined'
            ORDER BY updated_at DESC
        """)
        
        conversations = [self._row_to_state(row) for row in cursor.fetchall()]
        conn.close()
        
        return conversations
    
    def mark_for_escalation(self, thread_id: str, reason: str):
        """Mark a conversation as requiring human intervention"""
        self.update_state(thread_id, {
            'requires_escalation': True,
            'escalation_reason': reason
        })
    
    def _save_state(self, state: ConversationState):
        """Save conversation state to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO conversations (
                thread_id, stage, channel, company, recruiter_name, position,
                tech_stack, salary_range, work_arrangement, location,
                created_at, updated_at, conversation_history, metadata,
                requires_escalation, escalation_reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            state.thread_id,
            state.stage,
            state.channel,
            state.company,
            state.recruiter_name,
            state.position,
            json.dumps(state.tech_stack),
            state.salary_range,
            state.work_arrangement,
            state.location,
            state.created_at,
            state.updated_at,
            json.dumps(state.conversation_history),
            json.dumps(state.metadata),
            1 if state.requires_escalation else 0,
            state.escalation_reason
        ))
        
        conn.commit()
        conn.close()
    
    def _save_message(self, thread_id: str, message: Dict):
        """Save individual message to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get timestamp and ensure it's a string
        timestamp = message.get('timestamp', datetime.now())
        if isinstance(timestamp, datetime):
            timestamp = timestamp.isoformat()
        
        cursor.execute("""
            INSERT INTO messages (thread_id, timestamp, channel, direction, content, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            thread_id,
            timestamp,
            message.get('channel', 'unknown'),
            message.get('direction', 'incoming'),
            message.get('content', ''),
            json.dumps(message.get('metadata', {}))
        ))
        
        conn.commit()
        conn.close()
    
    def _row_to_state(self, row) -> ConversationState:
        """Convert database row to ConversationState object"""
        return ConversationState(
            thread_id=row[0],
            stage=row[1],
            channel=row[2],
            company=row[3] or "",
            recruiter_name=row[4] or "",
            position=row[5] or "",
            tech_stack=json.loads(row[6]) if row[6] else [],
            salary_range=row[7],
            work_arrangement=row[8],
            location=row[9],
            created_at=datetime.fromisoformat(row[10]) if row[10] else datetime.now(),
            updated_at=datetime.fromisoformat(row[11]) if row[11] else datetime.now(),
            conversation_history=json.loads(row[12]) if row[12] else [],
            metadata=json.loads(row[13]) if row[13] else {},
            requires_escalation=bool(row[14]),
            escalation_reason=row[15]
        )

