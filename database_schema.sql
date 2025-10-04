-- =====================================================
-- Automated Bus Ticketing and Reservation System
-- Database Schema and Initial Data
-- =====================================================

-- Create Database
CREATE DATABASE IF NOT EXISTS bus_ticketing_system;
USE bus_ticketing_system;

-- =====================================================
-- 1. USER MANAGEMENT TABLES
-- =====================================================

-- Users table (Customers, Drivers, Staff, Admins)
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('customer', 'driver', 'staff', 'admin') NOT NULL DEFAULT 'customer',
    phone_number VARCHAR(20),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role),
    INDEX idx_is_active (is_active)
);

-- =====================================================
-- 2. TERMINAL AND ROUTE MANAGEMENT
-- =====================================================

-- Terminals/Bus Stops
CREATE TABLE terminals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    terminal_type ENUM('main_terminal', 'bus_stop', 'pickup_point') DEFAULT 'bus_stop',
    location TEXT,
    city VARCHAR(50) NOT NULL,
    operating_hours_start TIME,
    operating_hours_end TIME,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_city (city),
    INDEX idx_is_active (is_active)
);

-- Routes between terminals
CREATE TABLE routes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    origin VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    origin_terminal_id INT,
    destination_terminal_id INT,
    distance_km DECIMAL(8, 2),
    estimated_duration_minutes INT,
    price DECIMAL(10, 2) NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (origin_terminal_id) REFERENCES terminals(id) ON DELETE SET NULL,
    FOREIGN KEY (destination_terminal_id) REFERENCES terminals(id) ON DELETE SET NULL,
    INDEX idx_origin_destination (origin_terminal_id, destination_terminal_id),
    INDEX idx_price (price),
    INDEX idx_is_active (is_active)
);

-- =====================================================
-- 3. BUS AND DRIVER MANAGEMENT
-- =====================================================

-- Buses
CREATE TABLE buses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    bus_number VARCHAR(20) UNIQUE NOT NULL,
    bus_name VARCHAR(100),
    bus_type ENUM('mini', 'standard', 'large', 'luxury') DEFAULT 'standard',
    seat_capacity INT NOT NULL,
    assigned_route_id INT,
    license_plate VARCHAR(20),
    manufacturer VARCHAR(50),
    model VARCHAR(50),
    year INT,
    current_latitude DECIMAL(10, 8),
    current_longitude DECIMAL(11, 8),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assigned_route_id) REFERENCES routes(id) ON DELETE SET NULL,
    INDEX idx_bus_number (bus_number),
    INDEX idx_assigned_route (assigned_route_id),
    INDEX idx_is_active (is_active)
);

-- Drivers (extends users)
CREATE TABLE drivers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    license_expiry_date DATE NOT NULL,
    phone_number VARCHAR(20),
    assigned_bus_id INT,
    is_active BOOLEAN DEFAULT TRUE,
    hire_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_bus_id) REFERENCES buses(id) ON DELETE SET NULL,
    INDEX idx_license_number (license_number),
    INDEX idx_assigned_bus (assigned_bus_id),
    INDEX idx_is_active (is_active)
);

-- =====================================================
-- 4. SEAT AND BOOKING MANAGEMENT
-- =====================================================

-- Seats for each bus
CREATE TABLE seats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    bus_id INT NOT NULL,
    seat_number VARCHAR(10) NOT NULL,
    seat_type ENUM('window', 'aisle', 'middle') DEFAULT 'aisle',
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bus_id) REFERENCES buses(id) ON DELETE CASCADE,
    UNIQUE KEY unique_bus_seat (bus_id, seat_number),
    INDEX idx_bus_id (bus_id),
    INDEX idx_is_available (is_available)
);

-- Bookings/Reservations
CREATE TABLE bookings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pnr_code VARCHAR(20) UNIQUE NOT NULL,
    customer_id INT NOT NULL,
    route_id INT NOT NULL,
    bus_id INT NOT NULL,
    seat_id INT NOT NULL,
    travel_date DATE NOT NULL,
    travel_time TIME NOT NULL,
    trip_type ENUM('one_way', 'round_trip') DEFAULT 'one_way',
    return_date DATE,
    return_time TIME,
    payment_method ENUM('cash', 'card', 'mobile_money', 'paypal') DEFAULT 'cash',
    amount_paid DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'SLL',
    booking_status ENUM('pending', 'confirmed', 'cancelled', 'completed') DEFAULT 'pending',
    payment_status ENUM('pending', 'paid', 'refunded', 'failed') DEFAULT 'pending',
    qr_code_path VARCHAR(255),
    special_requests TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (route_id) REFERENCES routes(id) ON DELETE CASCADE,
    FOREIGN KEY (bus_id) REFERENCES buses(id) ON DELETE CASCADE,
    FOREIGN KEY (seat_id) REFERENCES seats(id) ON DELETE CASCADE,
    INDEX idx_pnr_code (pnr_code),
    INDEX idx_customer_id (customer_id),
    INDEX idx_route_id (route_id),
    INDEX idx_bus_id (bus_id),
    INDEX idx_travel_date (travel_date),
    INDEX idx_booking_status (booking_status),
    INDEX idx_payment_status (payment_status)
);

-- =====================================================
-- 5. GPS TRACKING AND LOCATION MANAGEMENT
-- =====================================================

-- GPS Location tracking for buses
CREATE TABLE bus_locations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    bus_id INT NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    speed_kmh DECIMAL(5, 2),
    heading DECIMAL(5, 2),
    is_moving BOOLEAN DEFAULT FALSE,
    accuracy_meters DECIMAL(6, 2),
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bus_id) REFERENCES buses(id) ON DELETE CASCADE,
    INDEX idx_bus_id (bus_id),
    INDEX idx_recorded_at (recorded_at),
    INDEX idx_is_moving (is_moving)
);

-- =====================================================
-- 6. PAYMENT AND FINANCIAL MANAGEMENT
-- =====================================================

-- Payment transactions
CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'SLL',
    payment_method ENUM('cash', 'card', 'mobile_money', 'paypal') NOT NULL,
    transaction_id VARCHAR(100) UNIQUE,
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed_by INT,
    notes TEXT,
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    FOREIGN KEY (processed_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_booking_id (booking_id),
    INDEX idx_payment_status (payment_status),
    INDEX idx_payment_date (payment_date)
);

-- Currency exchange rates
CREATE TABLE currency_rates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    from_currency VARCHAR(3) NOT NULL,
    to_currency VARCHAR(3) NOT NULL,
    exchange_rate DECIMAL(12, 6) NOT NULL,
    effective_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_currency_date (from_currency, to_currency, effective_date),
    INDEX idx_effective_date (effective_date)
);

-- =====================================================
-- 7. NOTIFICATION AND COMMUNICATION
-- =====================================================

-- Notifications
CREATE TABLE notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    notification_type ENUM('booking', 'payment', 'reminder', 'system', 'promotion') DEFAULT 'system',
    is_read BOOLEAN DEFAULT FALSE,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_is_read (is_read),
    INDEX idx_notification_type (notification_type)
);

-- =====================================================
-- 8. SYSTEM MANAGEMENT AND LOGGING
-- =====================================================

-- System settings
CREATE TABLE system_settings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT,
    setting_type ENUM('string', 'number', 'boolean', 'json') DEFAULT 'string',
    description TEXT,
    updated_by INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_setting_key (setting_key)
);

-- Audit log
CREATE TABLE audit_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    table_name VARCHAR(50),
    record_id INT,
    old_values JSON,
    new_values JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_table_name (table_name),
    INDEX idx_created_at (created_at)
);

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- Active routes with terminal information
CREATE VIEW active_routes_view AS
SELECT
    r.id,
    r.name,
    r.origin,
    r.destination,
    ot.name as origin_terminal_name,
    dt.name as destination_terminal_name,
    r.distance_km,
    r.estimated_duration_minutes,
    r.price,
    r.departure_time,
    r.arrival_time
FROM routes r
LEFT JOIN terminals ot ON r.origin_terminal_id = ot.id
LEFT JOIN terminals dt ON r.destination_terminal_id = dt.id
WHERE r.is_active = TRUE;

-- Available seats for each bus
CREATE VIEW available_seats_view AS
SELECT
    b.id as bus_id,
    b.bus_number,
    b.bus_name,
    COUNT(s.id) as total_seats,
    COUNT(CASE WHEN s.is_available THEN 1 END) as available_seats
FROM buses b
LEFT JOIN seats s ON b.id = s.bus_id
WHERE b.is_active = TRUE
GROUP BY b.id, b.bus_number, b.bus_name;

-- Booking summary view
CREATE VIEW booking_summary_view AS
SELECT
    b.id,
    b.pnr_code,
    CONCAT(u.first_name, ' ', u.last_name) as customer_name,
    u.email,
    r.name as route_name,
    r.origin,
    r.destination,
    bus.bus_number,
    s.seat_number,
    b.travel_date,
    b.travel_time,
    b.amount_paid,
    b.currency,
    b.booking_status,
    b.payment_status,
    b.created_at
FROM bookings b
JOIN users u ON b.customer_id = u.id
JOIN routes r ON b.route_id = r.id
JOIN buses bus ON b.bus_id = bus.id
JOIN seats s ON b.seat_id = s.id;

-- =====================================================
-- TRIGGERS FOR AUTOMATED PROCESSES
-- =====================================================

-- Trigger to update seat availability when booking is made
DELIMITER //
CREATE TRIGGER update_seat_availability_on_booking
AFTER INSERT ON bookings
FOR EACH ROW
BEGIN
    UPDATE seats SET is_available = FALSE WHERE id = NEW.seat_id;
END//
DELIMITER ;

-- Trigger to make seat available when booking is cancelled
DELIMITER //
CREATE TRIGGER update_seat_availability_on_cancel
AFTER UPDATE ON bookings
FOR EACH ROW
BEGIN
    IF OLD.booking_status != 'cancelled' AND NEW.booking_status = 'cancelled' THEN
        UPDATE seats SET is_available = TRUE WHERE id = NEW.seat_id;
    END IF;
END//
DELIMITER ;

-- Trigger to log booking status changes
DELIMITER //
CREATE TRIGGER log_booking_status_changes
AFTER UPDATE ON bookings
FOR EACH ROW
BEGIN
    IF OLD.booking_status != NEW.booking_status THEN
        INSERT INTO audit_log (user_id, action, table_name, record_id, old_values, new_values)
        VALUES (
            NEW.customer_id,
            'STATUS_CHANGE',
            'bookings',
            NEW.id,
            JSON_OBJECT('booking_status', OLD.booking_status),
            JSON_OBJECT('booking_status', NEW.booking_status)
        );
    END IF;
END//
DELIMITER ;

-- =====================================================
-- INITIAL DATA INSERTION
-- =====================================================

-- Insert default system settings
INSERT INTO system_settings (setting_key, setting_value, setting_type, description) VALUES
('system_name', 'Automated Bus Ticketing and Reservation System', 'string', 'System display name'),
('currency', 'SLL', 'string', 'Default currency'),
('timezone', 'Africa/Freetown', 'string', 'System timezone'),
('max_booking_advance_days', '30', 'number', 'Maximum days in advance for booking'),
('min_booking_hours', '2', 'number', 'Minimum hours before departure for booking'),
('qr_code_expiry_hours', '24', 'number', 'QR code validity period in hours'),
('enable_live_tracking', 'true', 'boolean', 'Enable GPS live tracking feature'),
('maintenance_mode', 'false', 'boolean', 'System maintenance mode');

-- Insert sample terminals
INSERT INTO terminals (name, terminal_type, location, city, operating_hours_start, operating_hours_end, latitude, longitude) VALUES
('Lumley Main Terminal', 'main_terminal', 'Lumley Roundabout', 'Freetown', '05:00:00', '22:00:00', 8.4842, -13.2317),
('Kissytown Bus Stop', 'bus_stop', 'Kissytown Road', 'Freetown', '06:00:00', '20:00:00', 8.4778, -13.2456),
('Waterloo Terminal', 'main_terminal', 'Waterloo Junction', 'Waterloo', '05:30:00', '21:30:00', 8.3389, -13.0667),
('Makeni Bus Station', 'main_terminal', 'Makeni Central', 'Makeni', '06:00:00', '19:00:00', 8.8833, -12.0500),
('Bo Terminal', 'main_terminal', 'Bo Central', 'Bo', '06:00:00', '18:00:00', 7.9667, -11.7333);

-- Insert sample routes
INSERT INTO routes (name, origin, destination, origin_terminal_id, destination_terminal_id, distance_km, estimated_duration_minutes, price, departure_time, arrival_time) VALUES
('Lumley to Kissytown', 'Lumley', 'Kissytown', 1, 2, 5.2, 25, 15000.00, '06:00:00', '06:25:00'),
('Lumley to Waterloo', 'Lumley', 'Waterloo', 1, 3, 25.8, 75, 35000.00, '07:00:00', '08:15:00'),
('Lumley to Makeni', 'Lumley', 'Makeni', 1, 4, 185.5, 240, 85000.00, '08:00:00', '12:00:00'),
('Lumley to Bo', 'Lumley', 'Bo', 1, 5, 245.3, 300, 120000.00, '09:00:00', '14:00:00'),
('Waterloo to Makeni', 'Waterloo', 'Makeni', 3, 4, 159.7, 180, 65000.00, '10:00:00', '13:00:00');

-- Insert sample buses
INSERT INTO buses (bus_number, bus_name, bus_type, seat_capacity, assigned_route_id, license_plate, manufacturer, model, year) VALUES
('SL-001', 'Comfort Rider 1', 'standard', 45, 1, 'SL 1234 A', 'Mercedes', 'Sprinter', 2022),
('SL-002', 'Comfort Rider 2', 'standard', 45, 2, 'SL 5678 B', 'Mercedes', 'Sprinter', 2022),
('SL-003', 'Luxury Express', 'luxury', 35, 3, 'SL 9012 C', 'Volvo', '9700', 2023),
('SL-004', 'City Hopper', 'mini', 25, 1, 'SL 3456 D', 'Toyota', 'Hiace', 2021),
('SL-005', 'Regional Service', 'large', 55, 4, 'SL 7890 E', 'Scania', 'K410', 2023);

-- Insert seats for buses
INSERT INTO seats (bus_id, seat_number, seat_type)
SELECT b.id, CONCAT('A', LPAD(n.num, 2, '0')), 'window'
FROM buses b
CROSS JOIN (SELECT 1 as num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION SELECT 12) n
WHERE b.seat_capacity >= n.num;

INSERT INTO seats (bus_id, seat_number, seat_type)
SELECT b.id, CONCAT('B', LPAD(n.num, 2, '0')), 'aisle'
FROM buses b
CROSS JOIN (SELECT 1 as num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION SELECT 12) n
WHERE b.seat_capacity >= n.num + 12;

INSERT INTO seats (bus_id, seat_number, seat_type)
SELECT b.id, CONCAT('C', LPAD(n.num, 2, '0')), 'window'
FROM buses b
CROSS JOIN (SELECT 1 as num UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9 UNION SELECT 10 UNION SELECT 11 UNION SELECT 12) n
WHERE b.seat_capacity >= n.num + 24;

-- Insert sample users
INSERT INTO users (username, email, password_hash, role, phone_number, first_name, last_name) VALUES
('admin', 'admin@busystem.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeCt1uLjRpJjQ8l2', 'admin', '+232 76 123456', 'System', 'Administrator'),
('driver1', 'driver1@busystem.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeCt1uLjRpJjQ8l2', 'driver', '+232 77 234567', 'John', 'Driver'),
('staff1', 'staff1@busystem.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeCt1uLjRpJjQ8l2', 'staff', '+232 78 345678', 'Mary', 'Staff'),
('customer1', 'customer1@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeCt1uLjRpJjQ8l2', 'customer', '+232 79 456789', 'Alice', 'Johnson'),
('customer2', 'customer2@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeCt1uLjRpJjQ8l2', 'customer', '+232 80 567890', 'Bob', 'Smith');

-- Insert sample drivers
INSERT INTO drivers (user_id, license_number, license_expiry_date, phone_number, assigned_bus_id) VALUES
(2, 'DL-2024-001', '2025-12-31', '+232 77 234567', 1),
(3, 'DL-2024-002', '2025-11-30', '+232 78 345678', 2);

-- Insert currency rates
INSERT INTO currency_rates (from_currency, to_currency, exchange_rate, effective_date) VALUES
('USD', 'SLL', 22500.00, CURDATE()),
('EUR', 'SLL', 24500.00, CURDATE()),
('GBP', 'SLL', 27500.00, CURDATE());

-- =====================================================
-- STORED PROCEDURES
-- =====================================================

-- Procedure to create a booking
DELIMITER //
CREATE PROCEDURE create_booking(
    IN p_customer_id INT,
    IN p_route_id INT,
    IN p_bus_id INT,
    IN p_seat_id INT,
    IN p_travel_date DATE,
    IN p_travel_time TIME,
    IN p_payment_method VARCHAR(20),
    IN p_amount DECIMAL(10,2)
)
BEGIN
    DECLARE v_pnr_code VARCHAR(20);
    DECLARE v_seat_available BOOLEAN;

    -- Check if seat is available
    SELECT is_available INTO v_seat_available
    FROM seats
    WHERE id = p_seat_id;

    IF v_seat_available = FALSE THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Seat is not available';
    END IF;

    -- Generate PNR code
    SET v_pnr_code = CONCAT('PNR', DATE_FORMAT(NOW(), '%Y%m%d'), LPAD(FLOOR(RAND() * 10000), 4, '0'));

    -- Create booking
    INSERT INTO bookings (
        pnr_code, customer_id, route_id, bus_id, seat_id,
        travel_date, travel_time, payment_method, amount_paid,
        booking_status, payment_status
    ) VALUES (
        v_pnr_code, p_customer_id, p_route_id, p_bus_id, p_seat_id,
        p_travel_date, p_travel_time, p_payment_method, p_amount,
        'confirmed', 'paid'
    );

    -- Return the PNR code
    SELECT v_pnr_code as pnr_code;
END//
DELIMITER ;

-- Procedure to get available seats for a route and date
DELIMITER //
CREATE PROCEDURE get_available_seats(
    IN p_route_id INT,
    IN p_travel_date DATE
)
BEGIN
    SELECT
        s.id,
        s.seat_number,
        s.seat_type,
        b.bus_number,
        b.bus_name
    FROM seats s
    JOIN buses b ON s.bus_id = b.id
    WHERE b.assigned_route_id = p_route_id
    AND s.is_available = TRUE
    AND NOT EXISTS (
        SELECT 1 FROM bookings bk
        WHERE bk.seat_id = s.id
        AND bk.travel_date = p_travel_date
        AND bk.booking_status IN ('pending', 'confirmed')
    )
    ORDER BY s.seat_number;
END//
DELIMITER ;

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Additional indexes for better query performance
CREATE INDEX idx_bookings_travel_date_status ON bookings (travel_date, booking_status);
CREATE INDEX idx_bus_locations_bus_time ON bus_locations (bus_id, recorded_at);
CREATE INDEX idx_notifications_user_read ON notifications (user_id, is_read);
CREATE INDEX idx_audit_log_user_action ON audit_log (user_id, action, created_at);

-- =====================================================
-- END OF DATABASE SCHEMA
-- =====================================================