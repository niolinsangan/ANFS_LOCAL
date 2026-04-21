"""
Demo/Sample Data Generator for Airport Network Flight Scheduler
"""
from datetime import datetime, timedelta
import random
from database.connection import execute_query, get_db_connection


def create_database():
    """Create the database if it doesn't exist"""
    try:
        import mysql.connector
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password=''  # Update if needed
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS anfs_db")
        conn.close()
        print("Database created successfully!")
    except Exception as e:
        print(f"Error creating database: {e}")
        return False
    return True


def seed_airports():
    """Insert sample airports"""
    airports = [
        ('JFK', 'John F. Kennedy International', 'New York', 'USA'),
        ('LAX', 'Los Angeles International', 'Los Angeles', 'USA'),
        ('ORD', "O'Hare International", 'Chicago', 'USA'),
        ('LHR', 'Heathrow Airport', 'London', 'UK'),
        ('CDG', 'Charles de Gaulle', 'Paris', 'France'),
        ('NRT', 'Narita International', 'Tokyo', 'Japan'),
        ('DXB', 'Dubai International', 'Dubai', 'UAE'),
        ('SIN', 'Changi Airport', 'Singapore', 'Singapore'),
        ('SYD', 'Sydney Kingsford Smith', 'Sydney', 'Australia'),
        ('HKG', 'Hong Kong International', 'Hong Kong', 'China'),
        ('FRA', 'Frankfurt Airport', 'Frankfurt', 'Germany'),
        ('AMS', 'Amsterdam Schiphol', 'Amsterdam', 'Netherlands'),
        ('MIA', 'Miami International', 'Miami', 'USA'),
        ('SFO', 'San Francisco International', 'San Francisco', 'USA'),
        ('BOS', 'Logan International', 'Boston', 'USA'),
        ('PPS', 'Puerto Pirincesa City', 'Puerto Pirincesa', 'Colombia'),
    ]
    
    query = "INSERT IGNORE INTO airports (code, name, city, country) VALUES (%s, %s, %s, %s)"
    return execute_many(query, airports)


def seed_gates_and_runways():
    """Insert sample gates and runways for each airport"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Get all airport IDs
    cursor.execute("SELECT id FROM airports")
    airports = cursor.fetchall()
    cursor.close()
    
    gates_data = []
    runways_data = []
    
    for airport in airports:
        airport_id = airport['id']
        # Add 5-10 gates per airport
        num_gates = random.randint(5, 10)
        for i in range(1, num_gates + 1):
            terminal = f"T{random.randint(1, 3)}"
            gates_data.append((
                f"G{i:02d}",
                airport_id,
                terminal,
                True
            ))
        
        # Add 2-4 runways per airport
        num_runways = random.randint(2, 4)
        for i in range(1, num_runways + 1):
            runways_data.append((
                f"RW{i:02d}L" if i % 2 else f"RW{i:02d}R",
                airport_id,
                True
            ))
    
    gate_query = "INSERT IGNORE INTO gates (gate_number, airport_id, terminal, is_operational) VALUES (%s, %s, %s, %s)"
    runway_query = "INSERT IGNORE INTO runways (runway_name, airport_id, is_operational) VALUES (%s, %s, %s)"
    
    execute_many(gate_query, gates_data)
    execute_many(runway_query, runways_data)
    return True


def seed_flights():
    """Insert sample flights"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Get all airports and gates
    cursor.execute("SELECT id, code FROM airports")
    airports = cursor.fetchall()
    
    cursor.execute("SELECT id, gate_number, airport_id FROM gates")
    gates = cursor.fetchall()
    
    cursor.execute("SELECT id, runway_name, airport_id FROM runways")
    runways = cursor.fetchall()
    
    cursor.close()
    
    airlines = [
        'SkyWings Airlines', 'Oceanic Airways', 'Continental Express',
        'Metro Airlines', 'Global Airways', 'Pacific Air',
        'Atlantic Connect', 'National Flight Services'
    ]
    
    aircraft_types = [
        'Boeing 737', 'Boeing 747', 'Boeing 777',
        'Airbus A320', 'Airbus A330', 'Airbus A380',
        'Bombardier CRJ900', 'Embraer E190'
    ]
    
    statuses = ['On Time', 'On Time', 'On Time', 'Delayed', 'Boarding', 'Departed', 'Landed']
    
    flights_data = []
    num_flights = 50
    
    for i in range(num_flights):
        # Select random origin and destination (different airports)
        origin = random.choice(airports)
        dest = random.choice(airports)
        while dest['id'] == origin['id']:
            dest = random.choice(airports)
        
        # Generate flight times
        base_time = datetime.now() + timedelta(days=random.randint(-2, 3))
        departure_hour = random.randint(6, 22)
        departure_minute = random.choice([0, 15, 30, 45])
        departure = base_time.replace(hour=departure_hour, minute=departure_minute)
        
        # Flight duration 1-12 hours
        duration = timedelta(hours=random.randint(1, 12), minutes=random.randint(0, 59))
        arrival = departure + duration
        
        # Generate flight number
        airline_prefix = random.choice(['SW', 'OA', 'CE', 'MA', 'GA', 'PA', 'AC', 'NS'])
        flight_num = f"{airline_prefix}{random.randint(100, 9999)}"
        
        # Select random gate and runway for the origin airport
        airport_gates = [g for g in gates if g['airport_id'] == origin['id']]
        airport_runways = [r for r in runways if r['airport_id'] == origin['id']]
        
        gate_id = random.choice(airport_gates)['id'] if airport_gates else None
        runway_id = random.choice(airport_runways)['id'] if airport_runways else None
        
        flights_data.append((
            flight_num,
            random.choice(airlines),
            origin['id'],
            dest['id'],
            departure,
            arrival,
            random.choice(statuses),
            gate_id,
            runway_id,
            random.choice(aircraft_types)
        ))
    
    query = """INSERT INTO flights 
               (flight_number, airline, origin_airport_id, destination_airport_id,
                departure_time, arrival_time, status, gate_id, runway_id, aircraft_type)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    
    return execute_many(query, flights_data)


def seed_passengers():
    """Insert sample passengers"""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Get all flights
    cursor.execute("SELECT id FROM flights")
    flights = cursor.fetchall()
    cursor.close()
    
    first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Lisa', 
                   'James', 'Mary', 'William', 'Jennifer', 'Richard', 'Linda', 'Thomas', 
                   'Patricia', 'Charles', 'Barbara', 'Daniel', 'Elizabeth']
    
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 
                  'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 
                  'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
    
    passengers_data = []
    
    for flight_id in [f['id'] for f in flights[:30]]:  # Add passengers to 30 flights
        num_passengers = random.randint(5, 50)
        
        for _ in range(num_passengers):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            passport = f"P{random.randint(10000000, 99999999)}"
            seat = f"{random.randint(1, 40)}{random.choice(['A', 'B', 'C', 'D', 'E', 'F'])}"
            booking = f"BK{random.randint(100000, 999999)}"
            
            passengers_data.append((
                first_name, last_name, passport, flight_id, seat, booking
            ))
    
    query = """INSERT INTO passengers 
               (first_name, last_name, passport_number, flight_id, seat_number, booking_reference)
               VALUES (%s, %s, %s, %s, %s, %s)"""
    
    return execute_many(query, passengers_data)


def execute_many(query, data_list):
    """Execute a query for multiple rows"""
    from database.connection import execute_many as em
    return em(query, data_list)


def run_seed():
    """Run all seed functions"""
    print("Creating database...")
    create_database()
    
    # Import and run schema
    import mysql.connector
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        database='anfs_db'
    )
    cursor = conn.cursor()
    
    # Read and execute schema
    with open('database/schema.sql', 'r') as f:
        schema = f.read()
        for statement in schema.split(';'):
            if statement.strip():
                try:
                    cursor.execute(statement)
                except Exception as e:
                    pass  # Ignore errors for existing tables
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Seeding airports...")
    seed_airports()
    
    print("Seeding gates and runways...")
    seed_gates_and_runways()
    
    print("Seeding flights...")
    seed_flights()
    
    print("Seeding passengers...")
    seed_passengers()
    
    print("\n✅ Sample data created successfully!")
    print(f"   - 15 Airports")
    print(f"   - ~75 Gates")
    print(f"   - ~45 Runways")
    print(f"   - 50 Flights")
    print(f"   - ~800 Passengers")


if __name__ == '__main__':
    run_seed()

