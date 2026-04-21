# Airport Network Flight Scheduler (ANFS) - Project Plan

## Project Overview
Real-time airport network flight scheduler with Tkinter GUI and MySQL database.

## Features
- Admin panel for CRUD operations (Add/Edit/Delete)
- Public overview panel for unregistered users
- View flights by airport/route
- Real-time status updates (On Time, Delayed, Cancelled)
- Passenger information management
- Gate/Runway scheduling

## Tech Stack
- Python 3.x
- Tkinter (GUI)
- MySQL (Database)
- mysql-connector-python (MySQL driver)

---

## Implementation Steps

### Phase 1: Project Setup
- [x] Create project directory structure
- [x] Update requirements.txt with dependencies
- [x] Create database configuration module

### Phase 2: Database Layer
- [x] Create database connection module
- [x] Create SQL schema (tables: airports, flights, passengers, gates, runways)
- [x] Create demo/sample data script

### Phase 3: Models
- [x] Airport model
- [x] Flight model
- [x] Passenger model
- [x] Gate model
- [x] Runway model

### Phase 4: UI Layer
- [x] Main application window with tabbed interface
- [x] Admin login panel
- [x] Admin CRUD operations panel
- [x] Public overview panel
- [x] Flight details dialog
- [x] Add/Edit flight dialog
- [x] Passenger management dialog

### Phase 5: Core Features
- [x] Flight viewing by airport/route
- [x] Real-time status updates
- [x] Gate assignment
- [x] Runway assignment
- [x] Search and filter functionality

### Phase 6: Testing & Demo
- [ ] Run: python database/seed_data.py to create sample data
- [ ] Run: python main.py to launch the application
- [ ] Test all CRUD operations
- [ ] Test public view

---

## Database Schema

### airports
- id (INT, PK, AUTO_INCREMENT)
- code (VARCHAR(3), UNIQUE) - IATA code
- name (VARCHAR(100))
- city (VARCHAR(50))
- country (VARCHAR(50))

### flights
- id (INT, PK, AUTO_INCREMENT)
- flight_number (VARCHAR(10))
- airline (VARCHAR(50))
- origin_airport_id (INT, FK)
- destination_airport_id (INT, FK)
- departure_time (DATETIME)
- arrival_time (DATETIME)
- status (ENUM: 'On Time', 'Delayed', 'Cancelled', 'Boarding', 'Departed', 'Landed')
- gate_id (INT, FK, NULLABLE)
- runway_id (INT, FK, NULLABLE)
- aircraft_type (VARCHAR(30))

### passengers
- id (INT, PK, AUTO_INCREMENT)
- first_name (VARCHAR(50))
- last_name (VARCHAR(50))
- passport_number (VARCHAR(20))
- flight_id (INT, FK)
- seat_number (VARCHAR(5))
- booking_reference (VARCHAR(10))

### gates
- id (INT, PK, AUTO_INCREMENT)
- gate_number (VARCHAR(10))
- airport_id (INT, FK)
- terminal (VARCHAR(10))

### runways
- id (INT, PK, AUTO_INCREMENT)
- runway_name (VARCHAR(10))
- airport_id (INT, FK)
- is_operational (BOOLEAN)

---

## File Structure
```
ANFS_PROJECT_ISO/
├── requirements.txt
├── config.py
├── database/
│   ├── __init__.py
│   ├── connection.py
│   ├── schema.sql
│   └── seed_data.py
├── models/
│   ├── __init__.py
│   ├── airport.py
│   ├── flight.py
│   ├── passenger.py
│   ├── gate.py
│   └── runway.py
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── admin_panel.py
│   ├── public_panel.py
│   ├── dialogs.py
│   └── styles.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
└── main.py
```

