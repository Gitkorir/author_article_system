from contextlib import contextmanager
import sqlite3
from pathlib import Path

DB_PATH = Path("data/articles.db")

@contextmanager
def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists
    conn = None
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row  # Enable dict-like row access
        conn.execute("PRAGMA foreign_keys = ON")
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        print(f"❌ DB connection failed: {e}")
        raise
    finally:
        if conn:
            conn.close()
            print(f"✅ Closed DB connection to {DB_PATH}")
