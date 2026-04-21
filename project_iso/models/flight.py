"""
Flight Model
"""
from datetime import datetime
from database.connection import execute_query


class Flight:
    """Flight model class"""
    
    def __init__(self, id=None, flight_number=None, airline=None, 
                 origin_airport_id=None, destination_airport_id=None,
                 departure_time=None, arrival_time=None, status='On Time',
                 gate_id=None, runway_id=None, aircraft_type=None):
        self.id = id
        self.flight_number = flight_number
        self.airline = airline
        self.origin_airport_id = origin_airport_id
        self.destination_airport_id = destination_airport_id
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.status = status
        self.gate_id = gate_id
        self.runway_id = runway_id
        self.aircraft_type = aircraft_type
    
    @staticmethod
    def get_all(limit=100):
        """Get all flights with airport details"""
        query = """
            SELECT f.*, 
                   o.code as origin_code, o.name as origin_name, o.city as origin_city,
                   d.code as dest_code, d.name as dest_name, d.city as dest_city,
                   g.gate_number, r.runway_name
            FROM flights f
            JOIN airports o ON f.origin_airport_id = o.id
            JOIN airports d ON f.destination_airport_id = d.id
            LEFT JOIN gates g ON f.gate_id = g.id
            LEFT JOIN runways r ON f.runway_id = r.id
            ORDER BY f.departure_time DESC
            LIMIT %s
        """
        return execute_query(query, (limit,), fetch=True) or []
    
    @staticmethod
    def get_by_id(flight_id):
        """Get flight by ID with full details"""
        query = """
            SELECT f.*, 
                   o.code as origin_code, o.name as origin_name, o.city as origin_city,
                   d.code as dest_code, d.name as dest_name, d.city as dest_city,
                   g.gate_number, r.runway_name
            FROM flights f
            JOIN airports o ON f.origin_airport_id = o.id
            JOIN airports d ON f.destination_airport_id = d.id
            LEFT JOIN gates g ON f.gate_id = g.id
            LEFT JOIN runways r ON f.runway_id = r.id
            WHERE f.id = %s
        """
        result = execute_query(query, (flight_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def get_by_airport(airport_id):
        """Get flights by airport (as origin or destination)"""
        query = """
            SELECT f.*, 
                   o.code as origin_code, o.name as origin_name, o.city as origin_city,
                   d.code as dest_code, d.name as dest_name, d.city as dest_city,
                   g.gate_number, r.runway_name
            FROM flights f
            JOIN airports o ON f.origin_airport_id = o.id
            JOIN airports d ON f.destination_airport_id = d.id
            LEFT JOIN gates g ON f.gate_id = g.id
            LEFT JOIN runways r ON f.runway_id = r.id
            WHERE f.origin_airport_id = %s OR f.destination_airport_id = %s
            ORDER BY f.departure_time
        """
        return execute_query(query, (airport_id, airport_id), fetch=True) or []
    
    @staticmethod
    def get_by_route(origin_id, dest_id):
        """Get flights by route"""
        query = """
            SELECT f.*, 
                   o.code as origin_code, o.name as origin_name, o.city as origin_city,
                   d.code as dest_code, d.name as dest_name, d.city as dest_city,
                   g.gate_number, r.runway_name
            FROM flights f
            JOIN airports o ON f.origin_airport_id = o.id
            JOIN airports d ON f.destination_airport_id = d.id
            LEFT JOIN gates g ON f.gate_id = g.id
            LEFT JOIN runways r ON f.runway_id = r.id
            WHERE f.origin_airport_id = %s AND f.destination_airport_id = %s
            ORDER BY f.departure_time
        """
        return execute_query(query, (origin_id, dest_id), fetch=True) or []
    
    @staticmethod
    def search(keyword):
        """Search flights by flight number or airline"""
        query = """
            SELECT f.*, 
                   o.code as origin_code, o.name as origin_name,
                   d.code as dest_code, d.name as dest_name
            FROM flights f
            JOIN airports o ON f.origin_airport_id = o.id
            JOIN airports d ON f.destination_airport_id = d.id
            WHERE f.flight_number LIKE %s OR f.airline LIKE %s
            ORDER BY f.departure_time
        """
        search_term = f"%{keyword}%"
        return execute_query(query, (search_term, search_term), fetch=True) or []
    
    def save(self):
        """Create new flight"""
        query = """INSERT INTO flights 
                   (flight_number, airline, origin_airport_id, destination_airport_id,
                    departure_time, arrival_time, status, gate_id, runway_id, aircraft_type)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        return execute_query(query, (
            self.flight_number, self.airline, self.origin_airport_id,
            self.destination_airport_id, self.departure_time, self.arrival_time,
            self.status, self.gate_id, self.runway_id, self.aircraft_type
        ))
    
    def update(self):
        """Update flight"""
        query = """UPDATE flights 
                   SET flight_number = %s, airline = %s, origin_airport_id = %s,
                       destination_airport_id = %s, departure_time = %s, arrival_time = %s,
                       status = %s, gate_id = %s, runway_id = %s, aircraft_type = %s
                   WHERE id = %s"""
        return execute_query(query, (
            self.flight_number, self.airline, self.origin_airport_id,
            self.destination_airport_id, self.departure_time, self.arrival_time,
            self.status, self.gate_id, self.runway_id, self.aircraft_type, self.id
        ))
    
    @staticmethod
    def update_status(flight_id, status):
        """Update flight status"""
        query = "UPDATE flights SET status = %s WHERE id = %s"
        return execute_query(query, (status, flight_id))
    
    @staticmethod
    def delete(flight_id):
        """Delete flight"""
        query = "DELETE FROM flights WHERE id = %s"
        return execute_query(query, (flight_id,))
    
    def __repr__(self):
        return f"<Flight {self.flight_number}>"

