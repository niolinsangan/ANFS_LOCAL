"""
Passenger Model
"""
from database.connection import execute_query


class Passenger:
    """Passenger model class"""
    
    def __init__(self, id=None, first_name=None, last_name=None, 
                 passport_number=None, flight_id=None, seat_number=None, 
                 booking_reference=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.passport_number = passport_number
        self.flight_id = flight_id
        self.seat_number = seat_number
        self.booking_reference = booking_reference
    
    @staticmethod
    def get_all():
        """Get all passengers"""
        query = """
            SELECT p.*, f.flight_number, f.airline,
                   o.code as origin_code, d.code as dest_code
            FROM passengers p
            JOIN flights f ON p.flight_id = f.id
            JOIN airports o ON f.origin_airport_id = o.id
            JOIN airports d ON f.destination_airport_id = d.id
            ORDER BY p.last_name, p.first_name
        """
        return execute_query(query, fetch=True) or []
    
    @staticmethod
    def get_by_id(passenger_id):
        """Get passenger by ID"""
        query = """
            SELECT p.*, f.flight_number, f.airline,
                   o.code as origin_code, d.code as dest_code
            FROM passengers p
            JOIN flights f ON p.flight_id = f.id
            JOIN airports o ON f.origin_airport_id = o.id
            JOIN airports d ON f.destination_airport_id = d.id
            WHERE p.id = %s
        """
        result = execute_query(query, (passenger_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def get_by_flight(flight_id):
        """Get passengers by flight"""
        query = """
            SELECT * FROM passengers 
            WHERE flight_id = %s 
            ORDER BY seat_number
        """
        return execute_query(query, (flight_id,), fetch=True) or []
    
    @staticmethod
    def get_by_booking(booking_ref):
        """Get passenger by booking reference"""
        query = "SELECT * FROM passengers WHERE booking_reference = %s"
        result = execute_query(query, (booking_ref,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def get_count_by_flight(flight_id):
        """Get passenger count for a flight"""
        query = "SELECT COUNT(*) as count FROM passengers WHERE flight_id = %s"
        result = execute_query(query, (flight_id,), fetch=True)
        return result[0]['count'] if result else 0
    
    def save(self):
        """Create new passenger"""
        query = """INSERT INTO passengers 
                   (first_name, last_name, passport_number, flight_id, seat_number, booking_reference)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        return execute_query(query, (
            self.first_name, self.last_name, self.passport_number,
            self.flight_id, self.seat_number, self.booking_reference
        ))
    
    def update(self):
        """Update passenger"""
        query = """UPDATE passengers 
                   SET first_name = %s, last_name = %s, passport_number = %s,
                       flight_id = %s, seat_number = %s, booking_reference = %s
                   WHERE id = %s"""
        return execute_query(query, (
            self.first_name, self.last_name, self.passport_number,
            self.flight_id, self.seat_number, self.booking_reference, self.id
        ))
    
    @staticmethod
    def delete(passenger_id):
        """Delete passenger"""
        query = "DELETE FROM passengers WHERE id = %s"
        return execute_query(query, (passenger_id,))
    
    def __repr__(self):
        return f"<Passenger {self.first_name} {self.last_name}>"

