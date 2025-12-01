"""
Simple database module for voter management
Uses SQLite for simplicity (can be upgraded to PostgreSQL for production)
"""
import sqlite3
import os
from contextlib import contextmanager
from typing import Optional, Dict

DB_PATH = os.path.join(os.path.dirname(__file__), 'voters.db')

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initialize the database schema"""
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS voters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                has_voted BOOLEAN DEFAULT FALSE,
                is_admin BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                voted_at TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                voter_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                ip_address TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (voter_id) REFERENCES voters(id)
            )
        ''')
        
        conn.commit()

def create_voter(email: str, password_hash: str, full_name: str = None, is_admin: bool = False) -> int:
    """Create a new voter account"""
    with get_db() as conn:
        cursor = conn.execute(
            'INSERT INTO voters (email, password_hash, full_name, is_admin) VALUES (?, ?, ?, ?)',
            (email, password_hash, full_name, is_admin)
        )
        conn.commit()
        return cursor.lastrowid

def get_voter_by_email(email: str) -> Optional[Dict]:
    """Get voter by email address"""
    with get_db() as conn:
        cursor = conn.execute('SELECT * FROM voters WHERE email = ?', (email,))
        row = cursor.fetchone()
        return dict(row) if row else None

def get_voter_by_id(voter_id: int) -> Optional[Dict]:
    """Get voter by ID"""
    with get_db() as conn:
        cursor = conn.execute('SELECT * FROM voters WHERE id = ?', (voter_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def mark_as_voted(voter_id: int) -> bool:
    """Mark a voter as having voted"""
    with get_db() as conn:
        conn.execute(
            'UPDATE voters SET has_voted = TRUE, voted_at = CURRENT_TIMESTAMP WHERE id = ?',
            (voter_id,)
        )
        conn.commit()
        return True

def has_voted(voter_id: int) -> bool:
    """Check if voter has already voted"""
    voter = get_voter_by_id(voter_id)
    return voter['has_voted'] if voter else False

def log_action(voter_id: int, action: str, details: str = None, ip_address: str = None):
    """Log an action to the audit trail"""
    with get_db() as conn:
        conn.execute(
            'INSERT INTO audit_log (voter_id, action, details, ip_address) VALUES (?, ?, ?, ?)',
            (voter_id, action, details, ip_address)
        )
        conn.commit()

def get_voter_count() -> int:
    """Get total number of registered voters"""
    with get_db() as conn:
        cursor = conn.execute('SELECT COUNT(*) FROM voters')
        return cursor.fetchone()[0]

def get_votes_count() -> int:
    """Get total number of votes cast"""
    with get_db() as conn:
        cursor = conn.execute('SELECT COUNT(*) FROM voters WHERE has_voted = TRUE')
        return cursor.fetchone()[0]

# Initialize database on module import
init_db()
