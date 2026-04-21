"""
Airport Model
"""
from database.connection import execute_query


class Airport:
    """Airport model class"""
    
    def __init__(self, id=None, code=None, name=None, city=None, country=None):
        self.id = id
        self.code = code
        self.name = name
        self.city = city
        self.country = country
    
    @staticmethod
    def get_all():
        """Get all airports"""
        query = "SELECT * FROM airports ORDER BY code"
        return execute_query(query, fetch=True) or []
    
    @staticmethod
    def get_by_id(airport_id):
        """Get airport by ID"""
        query = "SELECT * FROM airports WHERE id = %s"
        return execute_query(query, (airport_id,), fetch=True)
    
    @staticmethod
    def get_by_code(code):
        """Get airport by IATA code"""
        query = "SELECT * FROM airports WHERE code = %s"
        result = execute_query(query, (code,), fetch=True)
        return result[0] if result else None
    
    def save(self):
        """Create new airport"""
        query = """INSERT INTO airports (code, name, city, country) 
                   VALUES (%s, %s, %s, %s)"""
        return execute_query(query, (self.code, self.name, self.city, self.country))
    
    def update(self):
        """Update airport"""
        query = """UPDATE airports 
                   SET code = %s, name = %s, city = %s, country = %s 
                   WHERE id = %s"""
        return execute_query(query, (self.code, self.name, self.city, self.country, self.id))
    
    @staticmethod
    def delete(airport_id):
        """Delete airport"""
        query = "DELETE FROM airports WHERE id = %s"
        return execute_query(query, (airport_id,))
    
    def __repr__(self):
        return f"<Airport {self.code} - {self.name}>"

