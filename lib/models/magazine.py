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
                
        
