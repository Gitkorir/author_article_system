from lib.db.connection import get_connection

class magazine:
    VALID_CATEGORIES = ['Technology', 'Science', 'Business', 'Arts', 'Health']

    def __init__(self,name, category, id= None):
        self.name= name
        self.category= category
        self.id = id
        self._validate()

    def _validate(self):
        """Validate magazine attributes"""
        if not isinstance(self.name, str) or len(self.name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters long")
        
        if self.category not in self.VALID_CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(self.VALID_CATEGORIES)}")     
    
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
    
    @classmethod
    def most_popular(cls, limit=3):
        """Get magazines with most articles"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT magazines.*, COUNT(articles.id) as article_count
                FROM magazines
                LEFT JOIN articles ON magazines.id = articles.magazine_id
                GROUP BY magazines.id
                ORDER BY article_count DESC
                LIMIT ?
                """, (limit,))
            return cursor.fetchall()

    def authors_by_contribution(self):
        """Get authors ordered by their contribution count"""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT authors.*, COUNT(articles.id) as article_count
                FROM authors
                JOIN articles ON authors.id = articles.author_id
                WHERE articles.magazine_id = ?
                GROUP BY authors.id
                ORDER BY article_count DESC
                """, (self.id,))
            return cursor.fetchall()