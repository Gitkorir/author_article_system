from lib.db.connection import get_connection

class magazine:
    def __init__(self,name, category, id= None):
        self.name= name
        self.category= category
        self.id = id
    
    def save(self):
        """Save the magazine to the database"""
        with get_connection() as conn:
            cursor = conn.cursor()
            if self.id is None:
                cursor.execute(
                    "INSERT INTO magazine (name, category) VALUES (?,?) ",
                    (self.name, self.category)
                )
                self.id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE magazine SET name = ?, category = ? WHERE id = ?",
                (self.name,self.category,self.id)
                )
                conn.commit()
                return self
    def articles(self):
        """ Get all articles published in this magazine"""
        with get_connection() as conn: 
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM articles WHERE magazine_id = ?",
                (self.id,)
            )
            return cursor.fetchall()

    def contributors(self):
                   
        """Get all authors who have written for this magazine"""

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                 """
                SELECT DISTINCT authors.* FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id = ?
                """,
                (self.id,)
        )
        return [row['title'] for row in cursor.fetchall()]
    
    def article_titles(self):
        """Get list of all article titles for this magazine"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT title FROM articles WHERE magazine_id = ?",
                (self.id,)
            )
            return [row['title'] for row in cursor.fetchall()]
    
    def contributing_authors(self):
        """Get authors with more than 2 articles in this magazine"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT authors.*, COUNT(articles.id) as article_count
                FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id = ?
                GROUP BY authors.id
                HAVING article_count > 2
                """,
                (self.id,)
            )
            return cursor.fetchall()
    
    @classmethod
    def find_by_id(cls, magazine_id):
        """Find a magazine by ID"""
        with get_connection() as conn:
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
    def find_by_name(cls,name):
        """Find magazines by name"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM magazines WHERE name LIKE  ?",
                (f"%{name}",)
                
            )
            return [cls(**row) for row in cursor.fetchall()]
    
    @classmethod
    def find_by_category(cls, category):
        """Find magazines by category"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM magazines WHERE category = ?",
                (category,)
            )
            return [cls(**row) for row in cursor.fetchall()]
