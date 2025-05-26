from lib.db.connection import get_connection

class Author:
    def __init__(self,name,email,id=None):
          self.id = id
          self.name= name
          self.email= email

    def save(self):
         #saving the Author to the data base
        with get_connection() as conn:
              cursor = conn.cursor()
              if self.id is None :
                   cursor.execute(
                        (self.name,self.email)
                   )
                   self.id = cursor.lastrowid
              else:
                   cursor.execute(
                       (self.name,self.email,self.id) 
                   )
              conn.commit()
        return    self   

    def articles(self):
         #get all articles by an  author in the data base
         with get_connection() as conn:
              cursor = conn.cursor()
              cursor.execute(
                   #SELECT * from articles with a foreign id of Author
                   (self.id,)

              )
              return cursor.fetchall()
         
    def magazines(self):
         #get all the magazines this aurth has written for 
        with get_connection() as conn:
             cursor = conn.cursor()
             cursor.execute(
                  (self.id,)
             )
             return cursor.fetchall()
                  
               
            
                  
     

