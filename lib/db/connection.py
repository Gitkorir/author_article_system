import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent /"data" / "articles.db"

def get_connection():
    """Create and return a database connection"""
    # Create data directory if it doesn't exist
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn