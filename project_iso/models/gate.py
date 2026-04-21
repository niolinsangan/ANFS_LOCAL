"""
Gate Model
"""
from database.connection import execute_query


class Gate:
    """Gate model class"""
    
    def __init__(self, id=None, gate_number=None, airport_id=None, 
                 terminal='T1', is_operational=True):
        self.id = id
        self.gate_number = gate_number
        self.airport_id = airport_id
        self.terminal = terminal
        self.is_operational = is_operational
    
    @staticmethod
    def get_all():
        """Get all gates with airport info"""
        query = """
            SELECT g.*, a.code as airport_code, a.name as airport_name
            FROM gates g
            JOIN airports a ON g.airport_id = a.id
            ORDER BY a.code, g.gate_number
        """
        return execute_query(query, fetch=True) or []
    
    @staticmethod
    def get_by_airport(airport_id):
        """Get gates by airport"""
        query = """
            SELECT * FROM gates 
            WHERE airport_id = %s 
            ORDER BY terminal, gate_number
        """
        return execute_query(query, (airport_id,), fetch=True) or []
    
    @staticmethod
    def get_available_by_airport(airport_id):
        """Get available gates by airport"""
        query = """
            SELECT * FROM gates 
            WHERE airport_id = %s AND is_operational = TRUE
            ORDER BY terminal, gate_number
        """
        return execute_query(query, (airport_id,), fetch=True) or []
    
    @staticmethod
    def get_by_id(gate_id):
        """Get gate by ID"""
        query = "SELECT * FROM gates WHERE id = %s"
        result = execute_query(query, (gate_id,), fetch=True)
        return result[0] if result else None
    
    def save(self):
        """Create new gate"""
        query = """INSERT INTO gates (gate_number, airport_id, terminal, is_operational)
                   VALUES (%s, %s, %s, %s)"""
        return execute_query(query, (self.gate_number, self.airport_id, 
                                      self.terminal, self.is_operational))
    
    def update(self):
        """Update gate"""
        query = """UPDATE gates 
                   SET gate_number = %s, airport_id = %s, terminal = %s, is_operational = %s
                   WHERE id = %s"""
        return execute_query(query, (self.gate_number, self.airport_id, 
                                      self.terminal, self.is_operational, self.id))
    
    @staticmethod
    def delete(gate_id):
        """Delete gate"""
        query = "DELETE FROM gates WHERE id = %s"
        return execute_query(query, (gate_id,))
    
    def __repr__(self):
        return f"<Gate {self.gate_number}>"

