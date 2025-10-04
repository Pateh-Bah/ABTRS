-- Django Tables for Supabase Database
-- Run these commands in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Django Content Types
CREATE TABLE django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model)
);

-- Django Sessions
CREATE TABLE django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Django Migrations
CREATE TABLE django_migrations (
    id SERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Django Admin Log
CREATE TABLE django_admin_log (
    id SERIAL PRIMARY KEY,
    action_time TIMESTAMP WITH TIME ZONE NOT NULL,
    object_id TEXT,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT NOT NULL CHECK (action_flag >= 0),
    change_message TEXT NOT NULL,
    content_type_id INTEGER REFERENCES django_content_type(id),
    user_id BIGINT NOT NULL,
    CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED
);

-- Auth Groups
CREATE TABLE auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

-- Auth Permissions
CREATE TABLE auth_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL REFERENCES django_content_type(id),
    codename VARCHAR(100) NOT NULL,
    CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename)
);

-- Custom User Model (accounts_user)
CREATE TABLE accounts_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
    phone_number VARCHAR(20),
    user_type VARCHAR(20) NOT NULL DEFAULT 'passenger'
);

-- Auth Group Permissions
CREATE TABLE auth_group_permissions (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES auth_group(id),
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id),
    CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id)
);

-- User Groups
CREATE TABLE accounts_user_groups (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES accounts_user(id),
    group_id INTEGER NOT NULL REFERENCES auth_group(id),
    CONSTRAINT accounts_user_groups_user_id_group_id_59c1b48e_uniq UNIQUE (user_id, group_id)
);

-- User Permissions
CREATE TABLE accounts_user_user_permissions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES accounts_user(id),
    permission_id INTEGER NOT NULL REFERENCES auth_permission(id),
    CONSTRAINT accounts_user_user_permissions_user_id_permission_id_51e3b769_uniq UNIQUE (user_id, permission_id)
);

-- Terminals
CREATE TABLE terminals_terminal (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(200) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Routes
CREATE TABLE routes_route (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    origin_terminal_id INTEGER NOT NULL REFERENCES terminals_terminal(id),
    destination_terminal_id INTEGER NOT NULL REFERENCES terminals_terminal(id),
    distance DECIMAL(8, 2),
    duration INTEGER,
    price DECIMAL(10, 2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Buses
CREATE TABLE buses_bus (
    id SERIAL PRIMARY KEY,
    bus_number VARCHAR(20) NOT NULL UNIQUE,
    capacity INTEGER NOT NULL,
    model VARCHAR(100),
    current_driver_name VARCHAR(100),
    current_driver_phone VARCHAR(20),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Seats
CREATE TABLE buses_seat (
    id SERIAL PRIMARY KEY,
    bus_id INTEGER NOT NULL REFERENCES buses_bus(id),
    seat_number VARCHAR(10) NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    seat_type VARCHAR(20) NOT NULL DEFAULT 'standard',
    CONSTRAINT buses_seat_bus_id_seat_number_4c8b8b8b_uniq UNIQUE (bus_id, seat_number)
);

-- Bookings
CREATE TABLE bookings_booking (
    id SERIAL PRIMARY KEY,
    booking_id VARCHAR(20) NOT NULL UNIQUE,
    user_id BIGINT NOT NULL REFERENCES accounts_user(id),
    route_id INTEGER NOT NULL REFERENCES routes_route(id),
    bus_id INTEGER NOT NULL REFERENCES buses_bus(id),
    seat_id INTEGER NOT NULL REFERENCES buses_seat(id),
    passenger_name VARCHAR(100) NOT NULL,
    passenger_phone VARCHAR(20) NOT NULL,
    booking_date TIMESTAMP WITH TIME ZONE NOT NULL,
    travel_date DATE NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'confirmed',
    payment_method VARCHAR(20),
    mobile_money_number VARCHAR(20),
    card_number VARCHAR(20),
    card_cvc VARCHAR(5),
    card_expiry VARCHAR(10),
    card_holder_name VARCHAR(100),
    is_return_trip BOOLEAN NOT NULL DEFAULT FALSE,
    return_bus_id INTEGER REFERENCES buses_bus(id),
    return_seat_id INTEGER REFERENCES buses_seat(id),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- GPS Tracking - Drivers
CREATE TABLE gps_tracking_driver (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    license_number VARCHAR(50),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- GPS Tracking - Bus Locations
CREATE TABLE gps_tracking_buslocation (
    id SERIAL PRIMARY KEY,
    bus_id INTEGER NOT NULL REFERENCES buses_bus(id),
    driver_id INTEGER REFERENCES gps_tracking_driver(id),
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    speed DECIMAL(5, 2),
    heading DECIMAL(5, 2),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    route_id INTEGER REFERENCES routes_route(id)
);

-- GPS Tracking - Speed Alerts
CREATE TABLE gps_tracking_speedalert (
    id SERIAL PRIMARY KEY,
    bus_id INTEGER NOT NULL REFERENCES buses_bus(id),
    speed DECIMAL(5, 2) NOT NULL,
    max_speed DECIMAL(5, 2) NOT NULL,
    location_latitude DECIMAL(10, 8),
    location_longitude DECIMAL(11, 8),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_resolved BOOLEAN NOT NULL DEFAULT FALSE
);

-- GPS Tracking - Route Progress
CREATE TABLE gps_tracking_routeprogress (
    id SERIAL PRIMARY KEY,
    bus_id INTEGER NOT NULL REFERENCES buses_bus(id),
    route_id INTEGER NOT NULL REFERENCES routes_route(id),
    current_stop VARCHAR(100),
    next_stop VARCHAR(100),
    progress_percentage DECIMAL(5, 2),
    estimated_arrival TIMESTAMP WITH TIME ZONE,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- GPS Tracking - Geofence Areas
CREATE TABLE gps_tracking_geofencearea (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    center_latitude DECIMAL(10, 8) NOT NULL,
    center_longitude DECIMAL(11, 8) NOT NULL,
    radius DECIMAL(8, 2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- GPS Tracking - Emergency Alerts
CREATE TABLE gps_tracking_emergencyalert (
    id SERIAL PRIMARY KEY,
    bus_id INTEGER NOT NULL REFERENCES buses_bus(id),
    driver_id INTEGER REFERENCES gps_tracking_driver(id),
    alert_type VARCHAR(50) NOT NULL,
    message TEXT,
    location_latitude DECIMAL(10, 8),
    location_longitude DECIMAL(11, 8),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    is_resolved BOOLEAN NOT NULL DEFAULT FALSE
);

-- Core Site Settings
CREATE TABLE core_sitesettings (
    id SERIAL PRIMARY KEY,
    site_name VARCHAR(100) NOT NULL DEFAULT 'ABTRS',
    site_description TEXT,
    header_color VARCHAR(7) NOT NULL DEFAULT '#1f2937',
    header_text_color VARCHAR(7) NOT NULL DEFAULT '#ffffff',
    sidebar_color VARCHAR(7) NOT NULL DEFAULT '#374151',
    top_nav_text_color VARCHAR(7) NOT NULL DEFAULT '#ffffff',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Insert default site settings
INSERT INTO core_sitesettings (site_name, site_description) 
VALUES ('ABTRS', 'Advanced Bus Ticket Reservation System');

-- Create indexes for better performance
CREATE INDEX django_session_expire_date_a5c62663 ON django_session(expire_date);
CREATE INDEX accounts_user_username_6821ab7c_like ON accounts_user(username);
CREATE INDEX routes_route_origin_terminal_id_2c8b8b8b ON routes_route(origin_terminal_id);
CREATE INDEX routes_route_destination_terminal_id_2c8b8b8b ON routes_route(destination_terminal_id);
CREATE INDEX buses_seat_bus_id_4c8b8b8b ON buses_seat(bus_id);
CREATE INDEX bookings_booking_user_id_59c1b48e ON bookings_booking(user_id);
CREATE INDEX bookings_booking_route_id_2c8b8b8b ON bookings_booking(route_id);
CREATE INDEX bookings_booking_bus_id_4c8b8b8b ON bookings_booking(bus_id);
CREATE INDEX bookings_booking_seat_id_4c8b8b8b ON bookings_booking(seat_id);
CREATE INDEX gps_tracking_buslocation_bus_id_4c8b8b8b ON gps_tracking_buslocation(bus_id);
CREATE INDEX gps_tracking_buslocation_timestamp_4c8b8b8b ON gps_tracking_buslocation(timestamp);
