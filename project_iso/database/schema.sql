-- Airport Network Flight Scheduler Database Schema

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS anfs_db;
USE anfs_db;

-- Airports Table
CREATE TABLE IF NOT EXISTS airports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(3) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Gates Table
CREATE TABLE IF NOT EXISTS gates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    gate_number VARCHAR(10) NOT NULL,
    airport_id INT NOT NULL,
    terminal VARCHAR(10) DEFAULT 'T1',
    is_operational BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (airport_id) REFERENCES airports(id) ON DELETE CASCADE,
    UNIQUE KEY unique_gate (airport_id, gate_number)
);

-- Runways Table
CREATE TABLE IF NOT EXISTS runways (
    id INT AUTO_INCREMENT PRIMARY KEY,
    runway_name VARCHAR(10) NOT NULL,
    airport_id INT NOT NULL,
    is_operational BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (airport_id) REFERENCES airports(id) ON DELETE CASCADE,
    UNIQUE KEY unique_runway (airport_id, runway_name)
);

-- Flights Table
CREATE TABLE IF NOT EXISTS flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_number VARCHAR(10) NOT NULL,
    airline VARCHAR(50) NOT NULL,
    origin_airport_id INT NOT NULL,
    destination_airport_id INT NOT NULL,
    departure_time DATETIME NOT NULL,
    arrival_time DATETIME NOT NULL,
    status ENUM('On Time', 'Delayed', 'Cancelled', 'Boarding', 'Departed', 'Landed') DEFAULT 'On Time',
    gate_id INT,
    runway_id INT,
    aircraft_type VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (origin_airport_id) REFERENCES airports(id) ON DELETE RESTRICT,
    FOREIGN KEY (destination_airport_id) REFERENCES airports(id) ON DELETE RESTRICT,
    FOREIGN KEY (gate_id) REFERENCES gates(id) ON DELETE SET NULL,
    FOREIGN KEY (runway_id) REFERENCES runways(id) ON DELETE SET NULL,
    INDEX idx_origin (origin_airport_id),
    INDEX idx_destination (destination_airport_id),
    INDEX idx_departure (departure_time),
    INDEX idx_status (status)
);

-- Passengers Table
CREATE TABLE IF NOT EXISTS passengers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    passport_number VARCHAR(20) NOT NULL UNIQUE,
    flight_id INT NOT NULL,
    seat_number VARCHAR(5),
    booking_reference VARCHAR(10) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (flight_id) REFERENCES flights(id) ON DELETE CASCADE,
    INDEX idx_flight (flight_id),
    INDEX idx_booking (booking_reference)
);

-- Admin Users Table
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin user (password: admin123)
INSERT INTO admin_users (username, password, email) 
VALUES ('admin', 'admin123', 'admin@anfs.local')
ON DUPLICATE KEY UPDATE username = username;

