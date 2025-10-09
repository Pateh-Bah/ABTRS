#!/usr/bin/env python
"""
Script to insert sample data into Supabase database
"""

import os
import sys
import django
from pathlib import Path
from django.utils import timezone
from datetime import datetime, timedelta

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings')

# Setup Django
django.setup()

from django.contrib.auth import get_user_model
from django.core.management import call_command
from accounts.models import User
from routes.models import Route, Terminal
from buses.models import Bus, Seat
from bookings.models import Booking
from gps_tracking.models import Driver, BusLocation, SpeedAlert, RouteProgress, GeofenceArea, EmergencyAlert
from core.models import SiteSettings

def create_sample_data():
    """Create sample data for the database"""
    print("🚀 Creating sample data for ABTRS...")
    print("=" * 50)
    
    # Create superuser
    print("👤 Creating superuser...")
    try:
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@abtrs.com',
            password='admin123',
            first_name='System',
            last_name='Administrator',
            phone_number='+232123456700',
            user_type='admin'
        )
        print("✅ Superuser created: admin/admin123")
    except Exception as e:
        print(f"⚠️  Superuser might already exist: {e}")
        admin_user = User.objects.get(username='admin')
    
    # Create site settings
    print("\n🏢 Creating site settings...")
    site_settings, created = SiteSettings.objects.get_or_create(
        defaults={
            'site_name': 'ABTRS',
            'site_description': 'Advanced Bus Ticket Reservation System',
            'header_color': '#1f2937',
            'header_text_color': '#ffffff',
            'sidebar_color': '#374151',
            'top_nav_text_color': '#ffffff'
        }
    )
    if created:
        print("✅ Site settings created")
    else:
        print("✅ Site settings already exist")
    
    # Create terminals
    print("\n🚏 Creating terminals...")
    terminals_data = [
        ('Freetown Central Terminal', 'Freetown City Center', 8.4841, -13.2300),
        ('Bo Terminal', 'Bo City Center', 7.9553, -11.7398),
        ('Kenema Terminal', 'Kenema City Center', 7.8768, -11.1902),
        ('Makeni Terminal', 'Makeni City Center', 8.8833, -12.0500),
        ('Koidu Terminal', 'Koidu City Center', 8.6500, -10.9667),
        ('Port Loko Terminal', 'Port Loko City Center', 8.7667, -12.7833),
    ]
    
    terminals = {}
    for name, location, lat, lng in terminals_data:
        terminal, created = Terminal.objects.get_or_create(
            name=name,
            defaults={
                'location': location,
                'latitude': lat,
                'longitude': lng
            }
        )
        terminals[name] = terminal
        if created:
            print(f"✅ Created terminal: {name}")
        else:
            print(f"✅ Terminal already exists: {name}")
    
    # Create routes
    print("\n🛣️  Creating routes...")
    routes_data = [
        ('Freetown to Bo', 'Freetown Central Terminal', 'Bo Terminal', 250.5, 180, 45.00),
        ('Bo to Kenema', 'Bo Terminal', 'Kenema Terminal', 85.2, 60, 25.00),
        ('Freetown to Makeni', 'Freetown Central Terminal', 'Makeni Terminal', 120.8, 90, 35.00),
        ('Makeni to Koidu', 'Makeni Terminal', 'Koidu Terminal', 95.3, 75, 30.00),
        ('Freetown to Port Loko', 'Freetown Central Terminal', 'Port Loko Terminal', 65.4, 45, 20.00),
        ('Bo to Makeni', 'Bo Terminal', 'Makeni Terminal', 180.6, 120, 40.00),
        ('Kenema to Koidu', 'Kenema Terminal', 'Koidu Terminal', 110.7, 80, 32.00),
    ]
    
    routes = {}
    for name, origin_name, dest_name, distance, duration, price in routes_data:
        route, created = Route.objects.get_or_create(
            name=name,
            defaults={
                'origin_terminal': terminals[origin_name],
                'destination_terminal': terminals[dest_name],
                'distance': distance,
                'duration': duration,
                'price': price
            }
        )
        routes[name] = route
        if created:
            print(f"✅ Created route: {name}")
        else:
            print(f"✅ Route already exists: {name}")
    
    # Create buses
    print("\n🚌 Creating buses...")
    buses_data = [
        ('AB001', 50, 'Mercedes-Benz Sprinter', 'John Doe', '+232123456789'),
        ('AB002', 45, 'Toyota Coaster', 'Jane Smith', '+232123456790'),
        ('AB003', 55, 'Isuzu NPR', 'Michael Johnson', '+232123456791'),
        ('AB004', 48, 'Nissan Civilian', 'Sarah Wilson', '+232123456792'),
        ('AB005', 52, 'Mitsubishi Rosa', 'David Brown', '+232123456793'),
        ('AB006', 46, 'Hino Rainbow', 'Lisa Davis', '+232123456794'),
        ('AB007', 50, 'Mercedes-Benz Sprinter', 'Robert Miller', '+232123456795'),
        ('AB008', 44, 'Toyota Coaster', 'Emily Taylor', '+232123456796'),
    ]
    
    buses = {}
    for bus_number, capacity, model, driver_name, driver_phone in buses_data:
        bus, created = Bus.objects.get_or_create(
            bus_number=bus_number,
            defaults={
                'capacity': capacity,
                'model': model,
                'current_driver_name': driver_name,
                'current_driver_phone': driver_phone
            }
        )
        buses[bus_number] = bus
        if created:
            print(f"✅ Created bus: {bus_number}")
        else:
            print(f"✅ Bus already exists: {bus_number}")
    
    # Create seats for buses
    print("\n💺 Creating seats...")
    seat_count = 0
    for bus in buses.values():
        # Create seats for this bus
        for row in range(1, (bus.capacity // 4) + 2):
            for col in ['A', 'B', 'C', 'D']:
                seat_number = f"{row}{col}"
                seat, created = Seat.objects.get_or_create(
                    bus=bus,
                    seat_number=seat_number,
                    defaults={'is_available': True}
                )
                if created:
                    seat_count += 1
        print(f"✅ Created seats for bus {bus.bus_number}")
    
    print(f"✅ Total seats created: {seat_count}")
    
    # Create drivers
    print("\n👨‍💼 Creating drivers...")
    drivers_data = [
        ('John Doe', '+232123456789', 'DL001234567'),
        ('Jane Smith', '+232123456790', 'DL001234568'),
        ('Michael Johnson', '+232123456791', 'DL001234569'),
        ('Sarah Wilson', '+232123456792', 'DL001234570'),
        ('David Brown', '+232123456793', 'DL001234571'),
        ('Lisa Davis', '+232123456794', 'DL001234572'),
        ('Robert Miller', '+232123456795', 'DL001234573'),
        ('Emily Taylor', '+232123456796', 'DL001234574'),
    ]
    
    # Create driver users first
    driver_users = {}
    for name, phone, license_number in drivers_data:
        first_name, last_name = name.split(' ', 1)
        username = f"{first_name.lower()}_{last_name.lower()}"
        email = f"{username}@abtrs.com"
        
        try:
            driver_user = User.objects.create_user(
                username=username,
                email=email,
                password='driver123',
                first_name=first_name,
                last_name=last_name,
                phone_number=phone,
                user_type='driver'
            )
            driver_users[name] = driver_user
            print(f"✅ Created driver user: {username}")
        except Exception as e:
            print(f"⚠️  Driver user might already exist: {username}")
            driver_users[name] = User.objects.get(username=username)
    
    # Create driver profiles
    drivers = {}
    for name, phone, license_number in drivers_data:
        driver, created = Driver.objects.get_or_create(
            user=driver_users[name],
            defaults={
                'license_number': license_number,
                'phone_number': phone,
                'emergency_contact': f"Emergency Contact for {name}",
                'emergency_contact_phone': f"+232{phone[-9:]}",
                'is_active': True
            }
        )
        drivers[name] = driver
        if created:
            print(f"✅ Created driver profile: {name}")
        else:
            print(f"✅ Driver profile already exists: {name}")
    
    # Create sample users
    print("\n👥 Creating sample users...")
    users_data = [
        ('john_doe', 'John', 'Doe', 'john.doe@email.com', '+232123456701'),
        ('jane_smith', 'Jane', 'Smith', 'jane.smith@email.com', '+232123456702'),
        ('mike_wilson', 'Michael', 'Wilson', 'mike.wilson@email.com', '+232123456703'),
    ]
    
    sample_users = {}
    for username, first_name, last_name, email, phone in users_data:
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password='passenger123',
                first_name=first_name,
                last_name=last_name,
                phone_number=phone,
                user_type='passenger'
            )
            sample_users[username] = user
            print(f"✅ Created user: {username}")
        except Exception as e:
            print(f"⚠️  User might already exist: {username}")
            sample_users[username] = User.objects.get(username=username)
    
    # Create sample bookings
    print("\n🎫 Creating sample bookings...")
    bookings_data = [
        ('john_doe', 'Freetown to Bo', 'AB001', '1A', 'John Doe', '+232123456701', 45.00, 'confirmed'),
        ('jane_smith', 'Bo to Kenema', 'AB002', '25A', 'Jane Smith', '+232123456702', 25.00, 'confirmed'),
        ('mike_wilson', 'Freetown to Makeni', 'AB003', '50A', 'Michael Wilson', '+232123456703', 35.00, 'pending'),
    ]
    
    for username, route_name, bus_number, seat_number, passenger_name, passenger_phone, price, status in bookings_data:
        try:
            user = sample_users[username]
            route = routes[route_name]
            bus = buses[bus_number]
            seat = Seat.objects.get(bus=bus, seat_number=seat_number)
            
            booking_id = f"BK{Booking.objects.count() + 1:03d}"
            
            booking = Booking.objects.create(
                booking_id=booking_id,
                user=user,
                route=route,
                bus=bus,
                seat=seat,
                passenger_name=passenger_name,
                passenger_phone=passenger_phone,
                booking_date=timezone.now(),
                travel_date=timezone.now().date() + timedelta(days=1),
                price=price,
                status=status,
                payment_method='mobile_money'
            )
            
            # Mark seat as unavailable
            seat.is_available = False
            seat.save()
            
            print(f"✅ Created booking: {booking_id}")
        except Exception as e:
            print(f"⚠️  Could not create booking: {e}")
    
    # Create GPS data
    print("\n📍 Creating GPS tracking data...")
    
    # Bus locations
    for i, bus in enumerate(list(buses.values())[:4]):
        BusLocation.objects.create(
            bus=bus,
            driver=list(drivers.values())[i],
            latitude=8.4841 + (i * 0.1),
            longitude=-13.2300 + (i * 0.1),
            speed=45 + (i * 5),
            heading=90 + (i * 45),
            route=list(routes.values())[i % len(routes)]
        )
    print("✅ Created bus locations")
    
    # Geofence areas
    geofence_data = [
        ('Freetown Terminal Zone', 8.4841, -13.2300, 500),
        ('Bo Terminal Zone', 7.9553, -11.7398, 500),
        ('Kenema Terminal Zone', 7.8768, -11.1902, 500),
        ('Highway Speed Zone', 8.2000, -12.5000, 1000),
    ]
    
    for name, lat, lng, radius in geofence_data:
        GeofenceArea.objects.get_or_create(
            name=name,
            defaults={
                'center_latitude': lat,
                'center_longitude': lng,
                'radius_meters': radius,
                'is_active': True
            }
        )
    print("✅ Created geofence areas")
    
    # Speed alerts
    for i, bus in enumerate(list(buses.values())[:3]):
        SpeedAlert.objects.create(
            bus=bus,
            speed=85 + i,
            max_speed=80,
            location_latitude=8.4841 + i,
            location_longitude=-13.2300 + i,
            is_resolved=(i % 2 == 0)
        )
    print("✅ Created speed alerts")
    
    print("\n🎉 Sample data creation completed!")
    print("\n📋 Summary:")
    print(f"  - Terminals: {Terminal.objects.count()}")
    print(f"  - Routes: {Route.objects.count()}")
    print(f"  - Buses: {Bus.objects.count()}")
    print(f"  - Seats: {Seat.objects.count()}")
    print(f"  - Drivers: {Driver.objects.count()}")
    print(f"  - Users: {User.objects.count()}")
    print(f"  - Bookings: {Booking.objects.count()}")
    print(f"  - Bus Locations: {BusLocation.objects.count()}")
    print(f"  - Geofence Areas: {GeofenceArea.objects.count()}")
    print(f"  - Speed Alerts: {SpeedAlert.objects.count()}")
    
    print("\n🔑 Login Credentials:")
    print("  Admin: admin/admin123")
    print("  Driver: john_doe/driver123")
    print("  Passenger: john_doe/passenger123")

if __name__ == '__main__':
    create_sample_data()
