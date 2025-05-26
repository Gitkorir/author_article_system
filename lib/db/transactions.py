from lib.db.connection import get_connection
from .exceptions import DatabaseError

def transfer_articles(source_author_id, target_author_id):
    """
    Transfer all articles from one author to another in a transaction
    Returns True if successful, False if failed
    """
    try:
        with get_connection() as conn:
            conn.execute("BEGIN TRANSACTION")
            
            # Verify authors exist
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM authors WHERE id = ?", (source_author_id,))
            if not cursor.fetchone():
                raise 'RecordNotFound'(f"Source author {source_author_id} not found")
                
            cursor.execute("SELECT 1 FROM authors WHERE id = ?", (target_author_id,))
            if not cursor.fetchone():
                raise 'RecordNotFound'(f"Target author {target_author_id} not found")
            
            # Perform transfer
            cursor.execute("""
                UPDATE articles
                SET author_id = ?
                WHERE author_id = ?
                """, (target_author_id, source_author_id))
            
            conn.commit()
            return True
            
    except DatabaseError as e:
        conn.rollback()
        print(f"Transaction failed: {e}")
        return False