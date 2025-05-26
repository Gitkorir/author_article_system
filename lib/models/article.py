from lib.db.connection import get_connection

class Article:
    def __init__(self, title, content, author_id, magazine_id, id=None):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        self._validate()

    def save(self):
        """Save the article to the database"""
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                    """INSERT INTO articles 
                    (title, content, author_id, magazine_id) 
                    VALUES (?, ?, ?, ?)""",
                    (self.title, self.content, self.author_id, self.magazine_id)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    """UPDATE articles SET 
                    title = ?, content = ?, author_id = ?, magazine_id = ?
                    WHERE id = ?""",
                    (self.title, self.content, self.author_id, self.magazine_id, self.id)
                )
            conn.commit()
        return self

    def author(self):
        """Get the author of this article"""
        from lib.models.author import Author
        with get_connection() as conn:
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
        """Get the magazine this article belongs to"""
        from lib.models.magazine import Magazine
        with get_connection() as conn:
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
        """Find an article by ID"""
        with get_connection() as conn:
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
        """Find all articles by a specific author"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE author_id = ?",
                (author_id,)
            )
            return [cls(**row) for row in cursor.fetchall()]

    @classmethod
    def find_by_magazine(cls, magazine_id):
        """Find all articles in a specific magazine"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE magazine_id = ?",
                (magazine_id,)
            )
            return [cls(**row) for row in cursor.fetchall()]

    @classmethod
    def all(cls):
        """Get all articles"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles")
            return [cls(**row) for row in cursor.fetchall()]
        
   # In lib/models/article.py

class Article:
    # ... (existing methods)
    
    @classmethod
    def search(cls, query):
        """Search articles by title or content"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM articles
                WHERE title LIKE ? OR content LIKE ?
                ORDER BY title
                """, (f"%{query}%", f"%{query}%"))
            return [cls(**row) for row in cursor.fetchall()]

    @classmethod
    def recent(cls, limit=5):
        """Get most recent articles"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM articles
                ORDER BY id DESC
                LIMIT ?
                """, (limit,))
            return [cls(**row) for row in cursor.fetchall()]     