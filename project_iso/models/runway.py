"""
Runway Model
"""
from database.connection import execute_query


class Runway:
    """Runway model class"""
    
    def __init__(self, id=None, runway_name=None, airport_id=None, is_operational=True):
        self.id = id
        self.runway_name = runway_name
        self.airport_id = airport_id
        self.is_operational = is_operational
    
    @staticmethod
    def get_all():
        """Get all runways with airport info"""
        query = """
            SELECT r.*, a.code as airport_code, a.name as airport_name
            FROM runways r
            JOIN airports a ON r.airport_id = a.id
            ORDER BY a.code, r.runway_name
        """
        return execute_query(query, fetch=True) or []
    
    @staticmethod
    def get_by_airport(airport_id):
        """Get runways by airport"""
        query = """
            SELECT * FROM runways 
            WHERE airport_id = %s 
            ORDER BY runway_name
        """
        return execute_query(query, (airport_id,), fetch=True) or []
    
    @staticmethod
    def get_available_by_airport(airport_id):
        """Get available runways by airport"""
        query = """
            SELECT * FROM runways 
            WHERE airport_id = %s AND is_operational = TRUE
            ORDER BY runway_name
        """
        return execute_query(query, (airport_id,), fetch=True) or []
    
    @staticmethod
    def get_by_id(runway_id):
        """Get runway by ID"""
        query = "SELECT * FROM runways WHERE id = %s"
        result = execute_query(query, (runway_id,), fetch=True)
        return result[0] if result else None
    
    def save(self):
        """Create new runway"""
        query = """INSERT INTO runways (runway_name, airport_id, is_operational)
                   VALUES (%s, %s, %s)"""
        return execute_query(query, (self.runway_name, self.airport_id, self.is_operational))
    
    def update(self):
        """Update runway"""
        query = """UPDATE runways 
                   SET runway_name = %s, airport_id = %s, is_operational = %s
                   WHERE id = %s"""
        return execute_query(query, (self.runway_name, self.airport_id, 
                                      self.is_operational, self.id))
    
    @staticmethod
    def delete(runway_id):
        """Delete runway"""
        query = "DELETE FROM runways WHERE id = %s"
        return execute_query(query, (runway_id,))
    
    def __repr__(self):
        return f"<Runway {self.runway_name}>"

