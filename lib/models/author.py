from lib.db.connection import get_connection

class Author:
    def __init__(self,name,email,id=None):
          self.id = id
          self.name= name
          self.email= email

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
              return cursor.fetchall()
         
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
             return cursor.fetchall()
        
                  
    
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

   
                  
     

