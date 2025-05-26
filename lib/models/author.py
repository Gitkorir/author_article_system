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
                  
               
            
                  
     

