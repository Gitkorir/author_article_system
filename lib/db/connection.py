import sqlite3
from pathlib import Path
from contextlib import contextmanager
from .exceptions import DatabaseError


DB_PATH = Path(__file__).parent.parent.parent /"data" / "articles.db"

@contextmanager
def get_connection():
    """Create and return a database connection"""
    """Create and yield a database connection with error handling"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = None
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        yield conn
    except sqlite3.Error as e:
        raise DatabaseError(f"Database operation failed: {e}")
    finally:
        if conn:
            conn.close()
    
   