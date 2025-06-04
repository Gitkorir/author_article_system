from lib.db.connection import get_connection
from lib.models.article import Article
from lib.models.magazine import Magazine
import re

class Author:
    def __init__(self,name,email,id=None):
          self.id = id
          self.name= name
          self.email= email
          self._validate()
    
    def _validate(self):
        """Validate author attributes"""
        if not isinstance(self.name, str) or len(self.name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.email):
            raise ValueError("Invalid email format")
        
        if len(self.email) > 255:
            raise ValueError("Email too long (max 255 chars)")
        
    def save(self):
        """Save the author to the database"""
        with get_connection() as conn:
              cursor = conn.cursor()
              if self.id is None :
                   cursor.execute(
                         "INSERT INTO authors (name, email) VALUES (?, ?)",
                        (self.name,self.email)
                   )
                   self.id = cursor.lastrowid
              else:
                   cursor.execute(
                       "UPDATE authors SET name = ?, email = ? WHERE id = ?",
                       (self.name,self.email,self.id) 
                   )
              conn.commit()
        return    self   

    def articles(self):
         """Get all articles by this author"""
         with get_connection() as conn:
              cursor = conn.cursor()
              cursor.execute(
                    "SELECT * FROM articles WHERE author_id = ?",
                   (self.id,)

              )
              return [Article(**row) for row in cursor.fetchall()]
         
    def magazines(self):
        """Get all magazines this author has written for""" 
        with get_connection() as conn:
             cursor = conn.cursor()
             cursor.execute(
                   """
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
            """,
                  (self.id,)
             )
             return [Magazine(**row) for row in cursor.fetchall()]
        
                  
    
    @classmethod
    def find_by_id(cls, author_id):
        """Find an author by ID"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM authors WHERE id = ?",
                (author_id,)
            )
            row = cursor.fetchone()
            if row:
                return cls(**row)
            return None

    @classmethod
    def find_by_name(cls, name):
        """Find authors by name"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM authors WHERE name LIKE ?",
                (f"%{name}%",)
            )
            return [cls(**row) for row in cursor.fetchall()]
   # In lib/models/author.py

class Author:
    # ... (existing methods)
    
    @classmethod
    def top_writers(cls, limit=5):
        """Get authors with most articles, ordered by article count"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT authors.*, COUNT(articles.id) as article_count
                FROM authors
                LEFT JOIN articles ON authors.id = articles.author_id
                GROUP BY authors.id
                ORDER BY article_count DESC
                LIMIT ?
                """, (limit,))
            return cursor.fetchall()

    def magazines_by_article_count(self):
        """Get magazines this author writes for, with article counts"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT magazines.*, COUNT(articles.id) as article_count
                FROM magazines
                JOIN articles ON magazines.id = articles.magazine_id
                WHERE articles.author_id = ?
                GROUP BY magazines.id
                ORDER BY article_count DESC
                """, (self.id,))
            return cursor.fetchall()
   
                  
     

