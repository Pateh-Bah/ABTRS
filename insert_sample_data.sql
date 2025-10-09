-- Sample Data for Supabase Database
-- Run these commands in your Supabase SQL Editor after creating tables

-- Insert sample site settings
INSERT INTO core_sitesettings (site_name, site_description, header_color, header_text_color, sidebar_color, top_nav_text_color) 
VALUES ('ABTRS', 'Advanced Bus Ticket Reservation System', '#1f2937', '#ffffff', '#374151', '#ffffff');

-- Insert sample terminals
INSERT INTO terminals_terminal (name, location, latitude, longitude, created_at, updated_at) VALUES
('Freetown Central Terminal', 'Freetown City Center', 8.4841, -13.2300, NOW(), NOW()),
('Bo Terminal', 'Bo City Center', 7.9553, -11.7398, NOW(), NOW()),
('Kenema Terminal', 'Kenema City Center', 7.8768, -11.1902, NOW(), NOW()),
('Makeni Terminal', 'Makeni City Center', 8.8833, -12.0500, NOW(), NOW()),
('Koidu Terminal', 'Koidu City Center', 8.6500, -10.9667, NOW(), NOW()),
('Port Loko Terminal', 'Port Loko City Center', 8.7667, -12.7833, NOW(), NOW());

-- Insert sample routes
INSERT INTO routes_route (name, origin_terminal_id, destination_terminal_id, distance, duration, price, is_active, created_at, updated_at) VALUES
('Freetown to Bo', 1, 2, 250.5, 180, 45.00, true, NOW(), NOW()),
('Bo to Kenema', 2, 3, 85.2, 60, 25.00, true, NOW(), NOW()),
('Freetown to Makeni', 1, 4, 120.8, 90, 35.00, true, NOW(), NOW()),
('Makeni to Koidu', 4, 5, 95.3, 75, 30.00, true, NOW(), NOW()),
('Freetown to Port Loko', 1, 6, 65.4, 45, 20.00, true, NOW(), NOW()),
('Bo to Makeni', 2, 4, 180.6, 120, 40.00, true, NOW(), NOW()),
('Kenema to Koidu', 3, 5, 110.7, 80, 32.00, true, NOW(), NOW());

-- Insert sample buses
INSERT INTO buses_bus (bus_number, capacity, model, current_driver_name, current_driver_phone, is_active, created_at, updated_at) VALUES
('AB001', 50, 'Mercedes-Benz Sprinter', 'John Doe', '+232123456789', true, NOW(), NOW()),
('AB002', 45, 'Toyota Coaster', 'Jane Smith', '+232123456790', true, NOW(), NOW()),
('AB003', 55, 'Isuzu NPR', 'Michael Johnson', '+232123456791', true, NOW(), NOW()),
('AB004', 48, 'Nissan Civilian', 'Sarah Wilson', '+232123456792', true, NOW(), NOW()),
('AB005', 52, 'Mitsubishi Rosa', 'David Brown', '+232123456793', true, NOW(), NOW()),
('AB006', 46, 'Hino Rainbow', 'Lisa Davis', '+232123456794', true, NOW(), NOW()),
('AB007', 50, 'Mercedes-Benz Sprinter', 'Robert Miller', '+232123456795', true, NOW(), NOW()),
('AB008', 44, 'Toyota Coaster', 'Emily Taylor', '+232123456796', true, NOW(), NOW());

-- Insert sample seats for each bus
-- Bus AB001 (50 seats)
INSERT INTO buses_seat (bus_id, seat_number, is_available, seat_type) VALUES
(1, '1A', true, 'standard'), (1, '1B', true, 'standard'), (1, '1C', true, 'standard'), (1, '1D', true, 'standard'),
(1, '2A', true, 'standard'), (1, '2B', true, 'standard'), (1, '2C', true, 'standard'), (1, '2D', true, 'standard'),
(1, '3A', true, 'standard'), (1, '3B', true, 'standard'), (1, '3C', true, 'standard'), (1, '3D', true, 'standard'),
(1, '4A', true, 'standard'), (1, '4B', true, 'standard'), (1, '4C', true, 'standard'), (1, '4D', true, 'standard'),
(1, '5A', true, 'standard'), (1, '5B', true, 'standard'), (1, '5C', true, 'standard'), (1, '5D', true, 'standard'),
(1, '6A', true, 'standard'), (1, '6B', true, 'standard'), (1, '6C', true, 'standard'), (1, '6D', true, 'standard'),
(1, '7A', true, 'standard'), (1, '7B', true, 'standard'), (1, '7C', true, 'standard'), (1, '7D', true, 'standard'),
(1, '8A', true, 'standard'), (1, '8B', true, 'standard'), (1, '8C', true, 'standard'), (1, '8D', true, 'standard'),
(1, '9A', true, 'standard'), (1, '9B', true, 'standard'), (1, '9C', true, 'standard'), (1, '9D', true, 'standard'),
(1, '10A', true, 'standard'), (1, '10B', true, 'standard'), (1, '10C', true, 'standard'), (1, '10D', true, 'standard'),
(1, '11A', true, 'standard'), (1, '11B', true, 'standard'), (1, '11C', true, 'standard'), (1, '11D', true, 'standard'),
(1, '12A', true, 'standard'), (1, '12B', true, 'standard'), (1, '12C', true, 'standard'), (1, '12D', true, 'standard'),
(1, '13A', true, 'standard');

-- Bus AB002 (45 seats)
INSERT INTO buses_seat (bus_id, seat_number, is_available, seat_type) VALUES
(2, '1A', true, 'standard'), (2, '1B', true, 'standard'), (2, '1C', true, 'standard'), (2, '1D', true, 'standard'),
(2, '2A', true, 'standard'), (2, '2B', true, 'standard'), (2, '2C', true, 'standard'), (2, '2D', true, 'standard'),
(2, '3A', true, 'standard'), (2, '3B', true, 'standard'), (2, '3C', true, 'standard'), (2, '3D', true, 'standard'),
(2, '4A', true, 'standard'), (2, '4B', true, 'standard'), (2, '4C', true, 'standard'), (2, '4D', true, 'standard'),
(2, '5A', true, 'standard'), (2, '5B', true, 'standard'), (2, '5C', true, 'standard'), (2, '5D', true, 'standard'),
(2, '6A', true, 'standard'), (2, '6B', true, 'standard'), (2, '6C', true, 'standard'), (2, '6D', true, 'standard'),
(2, '7A', true, 'standard'), (2, '7B', true, 'standard'), (2, '7C', true, 'standard'), (2, '7D', true, 'standard'),
(2, '8A', true, 'standard'), (2, '8B', true, 'standard'), (2, '8C', true, 'standard'), (2, '8D', true, 'standard'),
(2, '9A', true, 'standard'), (2, '9B', true, 'standard'), (2, '9C', true, 'standard'), (2, '9D', true, 'standard'),
(2, '10A', true, 'standard'), (2, '10B', true, 'standard'), (2, '10C', true, 'standard'), (2, '10D', true, 'standard'),
(2, '11A', true, 'standard'), (2, '11B', true, 'standard'), (2, '11C', true, 'standard'), (2, '11D', true, 'standard'),
(2, '12A', true, 'standard');

-- Bus AB003 (55 seats)
INSERT INTO buses_seat (bus_id, seat_number, is_available, seat_type) VALUES
(3, '1A', true, 'standard'), (3, '1B', true, 'standard'), (3, '1C', true, 'standard'), (3, '1D', true, 'standard'),
(3, '2A', true, 'standard'), (3, '2B', true, 'standard'), (3, '2C', true, 'standard'), (3, '2D', true, 'standard'),
(3, '3A', true, 'standard'), (3, '3B', true, 'standard'), (3, '3C', true, 'standard'), (3, '3D', true, 'standard'),
(3, '4A', true, 'standard'), (3, '4B', true, 'standard'), (3, '4C', true, 'standard'), (3, '4D', true, 'standard'),
(3, '5A', true, 'standard'), (3, '5B', true, 'standard'), (3, '5C', true, 'standard'), (3, '5D', true, 'standard'),
(3, '6A', true, 'standard'), (3, '6B', true, 'standard'), (3, '6C', true, 'standard'), (3, '6D', true, 'standard'),
(3, '7A', true, 'standard'), (3, '7B', true, 'standard'), (3, '7C', true, 'standard'), (3, '7D', true, 'standard'),
(3, '8A', true, 'standard'), (3, '8B', true, 'standard'), (3, '8C', true, 'standard'), (3, '8D', true, 'standard'),
(3, '9A', true, 'standard'), (3, '9B', true, 'standard'), (3, '9C', true, 'standard'), (3, '9D', true, 'standard'),
(3, '10A', true, 'standard'), (3, '10B', true, 'standard'), (3, '10C', true, 'standard'), (3, '10D', true, 'standard'),
(3, '11A', true, 'standard'), (3, '11B', true, 'standard'), (3, '11C', true, 'standard'), (3, '11D', true, 'standard'),
(3, '12A', true, 'standard'), (3, '12B', true, 'standard'), (3, '12C', true, 'standard'), (3, '12D', true, 'standard'),
(3, '13A', true, 'standard'), (3, '13B', true, 'standard'), (3, '13C', true, 'standard'), (3, '13D', true, 'standard'),
(3, '14A', true, 'standard');

-- Insert sample drivers
INSERT INTO gps_tracking_driver (name, phone, license_number, is_active, created_at) VALUES
('John Doe', '+232123456789', 'DL001234567', true, NOW()),
('Jane Smith', '+232123456790', 'DL001234568', true, NOW()),
('Michael Johnson', '+232123456791', 'DL001234569', true, NOW()),
('Sarah Wilson', '+232123456792', 'DL001234570', true, NOW()),
('David Brown', '+232123456793', 'DL001234571', true, NOW()),
('Lisa Davis', '+232123456794', 'DL001234572', true, NOW()),
('Robert Miller', '+232123456795', 'DL001234573', true, NOW()),
('Emily Taylor', '+232123456796', 'DL001234574', true, NOW());

-- Insert sample bus locations
INSERT INTO gps_tracking_buslocation (bus_id, driver_id, latitude, longitude, speed, heading, timestamp, route_id) VALUES
(1, 1, 8.4841, -13.2300, 0, 0, NOW(), 1),
(2, 2, 7.9553, -11.7398, 45, 180, NOW(), 2),
(3, 3, 8.8833, -12.0500, 35, 90, NOW(), 3),
(4, 4, 7.8768, -11.1902, 50, 270, NOW(), 4),
(5, 5, 8.6500, -10.9667, 40, 45, NOW(), 5),
(6, 6, 8.7667, -12.7833, 30, 135, NOW(), 6),
(7, 7, 8.4841, -13.2300, 0, 0, NOW(), 7),
(8, 8, 7.9553, -11.7398, 55, 225, NOW(), 1);

-- Insert sample geofence areas
INSERT INTO gps_tracking_geofencearea (name, center_latitude, center_longitude, radius, is_active, created_at) VALUES
('Freetown Terminal Zone', 8.4841, -13.2300, 500, true, NOW()),
('Bo Terminal Zone', 7.9553, -11.7398, 500, true, NOW()),
('Kenema Terminal Zone', 7.8768, -11.1902, 500, true, NOW()),
('Makeni Terminal Zone', 8.8833, -12.0500, 500, true, NOW()),
('Highway Speed Zone', 8.2000, -12.5000, 1000, true, NOW());

-- Insert sample route progress
INSERT INTO gps_tracking_routeprogress (bus_id, route_id, current_stop, next_stop, progress_percentage, estimated_arrival, timestamp) VALUES
(1, 1, 'Freetown Central Terminal', 'Bo Terminal', 0, NOW() + INTERVAL '3 hours', NOW()),
(2, 2, 'Bo Terminal', 'Kenema Terminal', 25, NOW() + INTERVAL '45 minutes', NOW()),
(3, 3, 'Freetown Central Terminal', 'Makeni Terminal', 15, NOW() + INTERVAL '1 hour 15 minutes', NOW()),
(4, 4, 'Makeni Terminal', 'Koidu Terminal', 60, NOW() + INTERVAL '30 minutes', NOW()),
(5, 5, 'Freetown Central Terminal', 'Port Loko Terminal', 80, NOW() + INTERVAL '10 minutes', NOW());

-- Create a superuser account (you'll need to set a password)
-- Note: This creates the user record, but you'll need to set the password through Django admin
INSERT INTO accounts_user (password, username, first_name, last_name, email, is_staff, is_active, is_superuser, date_joined, phone_number, user_type) VALUES
('pbkdf2_sha256$720000$dummy$dummy', 'admin', 'System', 'Administrator', 'admin@abtrs.com', true, true, true, NOW(), '+232123456700', 'admin');

-- Insert sample regular users
INSERT INTO accounts_user (password, username, first_name, last_name, email, is_staff, is_active, is_superuser, date_joined, phone_number, user_type) VALUES
('pbkdf2_sha256$720000$dummy$dummy', 'john_doe', 'John', 'Doe', 'john.doe@email.com', false, true, false, NOW(), '+232123456701', 'passenger'),
('pbkdf2_sha256$720000$dummy$dummy', 'jane_smith', 'Jane', 'Smith', 'jane.smith@email.com', false, true, false, NOW(), '+232123456702', 'passenger'),
('pbkdf2_sha256$720000$dummy$dummy', 'mike_wilson', 'Michael', 'Wilson', 'mike.wilson@email.com', false, true, false, NOW(), '+232123456703', 'passenger');

-- Insert sample bookings
INSERT INTO bookings_booking (booking_id, user_id, route_id, bus_id, seat_id, passenger_name, passenger_phone, booking_date, travel_date, price, status, payment_method, created_at, updated_at) VALUES
('BK001', 2, 1, 1, 1, 'John Doe', '+232123456701', NOW(), CURRENT_DATE + INTERVAL '1 day', 45.00, 'confirmed', 'mobile_money', NOW(), NOW()),
('BK002', 3, 2, 2, 25, 'Jane Smith', '+232123456702', NOW(), CURRENT_DATE + INTERVAL '2 days', 25.00, 'confirmed', 'card', NOW(), NOW()),
('BK003', 4, 3, 3, 50, 'Michael Wilson', '+232123456703', NOW(), CURRENT_DATE + INTERVAL '3 days', 35.00, 'pending', 'mobile_money', NOW(), NOW());

-- Update seat availability for booked seats
UPDATE buses_seat SET is_available = false WHERE id IN (1, 25, 50);

-- Insert sample speed alerts
INSERT INTO gps_tracking_speedalert (bus_id, speed, max_speed, location_latitude, location_longitude, timestamp, is_resolved) VALUES
(1, 85, 80, 8.4841, -13.2300, NOW() - INTERVAL '1 hour', false),
(2, 95, 80, 7.9553, -11.7398, NOW() - INTERVAL '30 minutes', true),
(3, 90, 80, 8.8833, -12.0500, NOW() - INTERVAL '15 minutes', false);

-- Insert sample emergency alerts
INSERT INTO gps_tracking_emergencyalert (bus_id, driver_id, alert_type, message, location_latitude, location_longitude, timestamp, is_resolved) VALUES
(1, 1, 'breakdown', 'Engine overheating, need assistance', 8.4841, -13.2300, NOW() - INTERVAL '2 hours', false),
(2, 2, 'medical', 'Passenger feeling unwell', 7.9553, -11.7398, NOW() - INTERVAL '1 hour', true),
(3, 3, 'security', 'Suspicious activity reported', 8.8833, -12.0500, NOW() - INTERVAL '45 minutes', false);

-- Update the admin user password (you'll need to hash this properly in Django)
-- For now, this is a placeholder - you should set the password through Django admin or management command
UPDATE accounts_user SET password = 'pbkdf2_sha256$720000$dummy$dummy' WHERE username = 'admin';

-- Show summary of inserted data
SELECT 
    'Terminals' as table_name, COUNT(*) as count FROM terminals_terminal
UNION ALL
SELECT 'Routes', COUNT(*) FROM routes_route
UNION ALL  
SELECT 'Buses', COUNT(*) FROM buses_bus
UNION ALL
SELECT 'Seats', COUNT(*) FROM buses_seat
UNION ALL
SELECT 'Drivers', COUNT(*) FROM gps_tracking_driver
UNION ALL
SELECT 'Users', COUNT(*) FROM accounts_user
UNION ALL
SELECT 'Bookings', COUNT(*) FROM bookings_booking
UNION ALL
SELECT 'Bus Locations', COUNT(*) FROM gps_tracking_buslocation
UNION ALL
SELECT 'Geofence Areas', COUNT(*) FROM gps_tracking_geofencearea
UNION ALL
SELECT 'Route Progress', COUNT(*) FROM gps_tracking_routeprogress
UNION ALL
SELECT 'Speed Alerts', COUNT(*) FROM gps_tracking_speedalert
UNION ALL
SELECT 'Emergency Alerts', COUNT(*) FROM gps_tracking_emergencyalert;
