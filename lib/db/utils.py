import sqlite3
from contextlib import contextmanager
import os

# Path to your database
DB_PATH = os.path.join(os.path.dirname(__file__), "../../data/articles.db")

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables dict-like access to rows
    try:
        yield conn
    finally:
        conn.close()

def count(tbl, where):
    with get_connection() as conn:
        cursor = conn.cursor()
        key, val = next(iter(where.items()))  # Only works for one key-value pair
        q = f"SELECT COUNT(*) AS count FROM {tbl} WHERE {key} = ?"
        row = cursor.execute(q, (val,)).fetchone()
        return row[0]  # Works because of row_factory

def get_one(results):
    # Converts a list to a single result, or returns None
    return results[0] if results else None
