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
     

