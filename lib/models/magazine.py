from lib.db.connection import get_connection
import sqlite3

class Magazine:

    VALID_CATEGORIES = ['Technology', 'Science', 'Business', 'Arts', 'Health']

    def __init__(self, id=None, category=None, name=None, bio=None, email=None):
        self.id = id
        self.name = name
        self.bio = bio
        self.category = category
        self.email = email
        self._validate()

    def _validate(self):
        if not isinstance(self.name, str) or len(self.name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        if self.category not in self.VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(self.VALID_CATEGORIES)}")

    def save(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?)",
                    (self.name, self.category)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                    (self.name, self.category, self.id)
                )
            conn.commit()
        return self

    def articles(self):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE magazine_id = ?",
                (self.id,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def contributors(self):
        from lib.models.author import Author
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT authors.* FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id = ?
            """, (self.id,))
            rows = cursor.fetchall()
        return [Author(**row) for row in rows]

    def article_titles(self):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT title FROM articles WHERE magazine_id = ?",
                (self.id,)
            )
            return [row['title'] for row in cursor.fetchall()]

    def contributing_authors(self):
        from lib.models.author import Author
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT authors.*, COUNT(articles.id) as article_count
                FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id = ?
                GROUP BY authors.id
                HAVING article_count > 2
            """, (self.id,))
            rows = cursor.fetchall()
        return [Author(**row) for row in rows]

    @classmethod
    def find_by_id(cls, magazine_id):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM magazines WHERE id = ?",
                (magazine_id,)
            )
            row = cursor.fetchone()
        if row:
            return cls(**row)
        return None

    @classmethod
    def find_by_name(cls, name):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM magazines WHERE name LIKE ?",
                (f"%{name}%",)
            )
            rows = cursor.fetchall()
        return [cls(**row) for row in rows]

    @classmethod
    def find_by_category(cls, category):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM magazines WHERE category = ?",
                (category,)
            )
            rows = cursor.fetchall()
        return [cls(**row) for row in rows]

    @classmethod
    def most_popular(cls, limit=3):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT magazines.*, COUNT(articles.id) as article_count
                FROM magazines
                LEFT JOIN articles ON magazines.id = articles.magazine_id
                GROUP BY magazines.id
                ORDER BY article_count DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def authors_by_contribution(self):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT authors.*, COUNT(articles.id) as article_count
                FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id = ?
                GROUP BY authors.id
                ORDER BY article_count DESC
            """, (self.id,))
            rows = cursor.fetchall()
        return [dict(row) for row in rows]

    @classmethod
    def with_multiple_authors(cls):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            result = cursor.execute("""
                SELECT magazines.* FROM magazines
                JOIN articles ON magazines.id = articles.magazine_id
                GROUP BY magazines.id
                HAVING COUNT(DISTINCT articles.author_id) > 1
            """).fetchall()
        return [cls(**row) for row in result]

    @classmethod
    def article_counts(cls):
        with get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            result = cursor.execute("""
                SELECT magazines.*, COUNT(articles.id) as article_count FROM magazines
                LEFT JOIN articles ON magazines.id = articles.magazine_id
                GROUP BY magazines.id
            """).fetchall()
        return [dict(row) for row in result]
