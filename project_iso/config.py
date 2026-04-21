"""
Configuration settings for the Airport Network Flight Scheduler
"""

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Update with your MySQL password
    'database': 'anfs_db'
}

# Admin credentials (in production, use hashed passwords and secure storage)
ADMIN_CREDENTIALS = {
    'username': 'admin',
    'password': 'admin123'  # Change this in production
}

# Application settings
APP_TITLE = "Airport Network Flight Scheduler (ANFS)"
APP_WIDTH = 1200
APP_HEIGHT = 700

# Flight status options
FLIGHT_STATUS = [
    'On Time',
    'Delayed',
    'Cancelled',
    'Boarding',
    'Departed',
    'Landed'
]

# Aircraft types
AIRCRAFT_TYPES = [
    'Boeing 737',
    'Boeing 747',
    'Boeing 777',
    'Airbus A320',
    'Airbus A330',
    'Airbus A380',
    'Cessna 172',
    'Bombardier CRJ900',
    'Embraer E190'
]

# Airlines
AIRLINES = [
    'SkyWings Airlines',
    'Oceanic Airways',
    'Continental Express',
    'Metro Airlines',
    'Global Airways',
    'Pacific Air',
    'Atlantic Connect',
    'National Flight Services'
]

