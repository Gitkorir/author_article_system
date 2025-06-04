from lib.db.connection import get_connection
import sqlite3

class Article:
    def __init__(self, title, content, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        self._validate()

    def _validate(self):
        if not self.title or not isinstance(self.title, str):
            raise ValueError("Article title must be a non-empty string")
        if not self.content or not isinstance(self.content, str):
            raise ValueError("Article content must be a non-empty string")
        if not isinstance(self.author_id, int):
            raise ValueError("Author ID must be an integer")
        if not isinstance(self.magazine_id, int):
            raise ValueError("Magazine ID must be an integer")

    def save(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                    """INSERT INTO articles (title, content, author_id, magazine_id)
                    VALUES (?, ?, ?, ?)""",
                    (self.title, self.content, self.author_id, self.magazine_id)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    """UPDATE articles SET title = ?, content = ?, author_id = ?, magazine_id = ?
                    WHERE id = ?""",
                    (self.title, self.content, self.author_id, self.magazine_id, self.id)
                )
            conn.commit()
        return self

    def author(self):
        from lib.models.author import Author
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM authors WHERE id = ?",
                (self.author_id,)
            )
            row = cursor.fetchone()
        if row:
            return Author(**row)
        return None

    def magazine(self):
        from lib.models.magazine import Magazine
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM magazines WHERE id = ?",
                (self.magazine_id,)
            )
            row = cursor.fetchone()
        if row:
            return Magazine(**row)
        return None

    @classmethod
    def find_by_id(cls, article_id):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE id = ?",
                (article_id,)
            )
            row = cursor.fetchone()
        if row:
            return cls(**row)
        return None

    @classmethod
    def find_by_author(cls, author_id):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE author_id = ?",
                (author_id,)
            )
            rows = cursor.fetchall()
        return [cls(**row) for row in rows]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE magazine_id = ?",
                (magazine_id,)
            )
            rows = cursor.fetchall()
        return [cls(**row) for row in rows]

    @classmethod
    def find_by_title(cls, title):
        from lib.db.search_db_conn import get_connection
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        
        record = row.fetchone()
        conn.close()
        return cls(**record) if record else None

    @classmethod
    def all(cls):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles")
            rows = cursor.fetchall()
        return [cls(**row) for row in rows]

    @classmethod
    def search(cls, query):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM articles
                WHERE title LIKE ? OR content LIKE ?
                ORDER BY title
            """, (f"%{query}%", f"%{query}%"))
            rows = cursor.fetchall()
        return [cls(**row) for row in rows]

    @classmethod
    def recent(cls, limit=5):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM articles
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
        return [cls(**row) for row in rows]
