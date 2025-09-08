#!/usr/bin/env python
"""
GPS Test Data Creation Script
Creates sample GPS data for testing the GPS tracking system
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine.settings')
django.setup()

from django.contrib.auth import get_user_model
from buses.models import Bus
from routes.models import Route, Terminal
from gps_tracking.models import Driver, BusLocation, SpeedAlert, RouteProgress, GeofenceArea

User = get_user_model()

def create_test_gps_data():
    """Create comprehensive GPS test data"""
    print("🚌 Creating GPS Test Data...")
    
    # Create or get admin user
    admin_user, created = User.objects.get_or_create(
        email='admin@wakafine.com',
        defaults={
            'first_name': 'GPS',
            'last_name': 'Admin',
            'phone_number': '+23276123456',
            'is_admin': True,
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✅ Created admin user: {admin_user.email}")
    
    # Create driver users
    drivers_data = [
        {
            'email': 'driver1@wakafine.com',
            'first_name': 'Mohamed',
            'last_name': 'Kamara',
            'phone_number': '+23276111111',
            'license_number': 'SL-DL-001',
        },
        {
            'email': 'driver2@wakafine.com',
            'first_name': 'Aminata',
            'last_name': 'Sesay',
            'phone_number': '+23276222222',
            'license_number': 'SL-DL-002',
        },
        {
            'email': 'driver3@wakafine.com',
            'first_name': 'Ibrahim',
            'last_name': 'Mansaray',
            'phone_number': '+23276333333',
            'license_number': 'SL-DL-003',
        }
    ]
    
    created_drivers = []
    for driver_data in drivers_data:
        user, created = User.objects.get_or_create(
            email=driver_data['email'],
            defaults={
                'first_name': driver_data['first_name'],
                'last_name': driver_data['last_name'],
                'phone_number': driver_data['phone_number'],
                'is_driver': True,
            }
        )
        if created:
            user.set_password('driver123')
            user.save()
        
        # Create driver profile
        driver, created = Driver.objects.get_or_create(
            user=user,
            defaults={
                'license_number': driver_data['license_number'],
                'license_expiry_date': timezone.now().date() + timedelta(days=365),
                'phone_number': driver_data['phone_number'],
                'is_active': True,
            }
        )
        created_drivers.append(driver)
        print(f"✅ Created driver: {driver.user.first_name} {driver.user.last_name}")
    
    # Get or create buses
    buses = list(Bus.objects.all())
    if not buses:
        print("❌ No buses found. Please create buses first using create_buses_for_routes.py")
        return
    
    # Assign drivers to buses and add GPS data
    freetown_coords = (8.4657, -13.2317)  # Freetown coordinates
    
    for i, bus in enumerate(buses[:3]):  # Limit to 3 buses for testing
        if i < len(created_drivers):
            driver = created_drivers[i]
            
            # Update bus with driver info and GPS device
            bus.current_driver_name = f"{driver.user.first_name} {driver.user.last_name}"
            bus.current_driver_phone = driver.phone_number
            bus.gps_device_id = f"GPS-{bus.bus_number}-{random.randint(1000, 9999)}"
            
            # Set initial location near Freetown with some variation
            lat_offset = random.uniform(-0.05, 0.05)
            lng_offset = random.uniform(-0.05, 0.05)
            bus.current_latitude = Decimal(str(freetown_coords[0] + lat_offset))
            bus.current_longitude = Decimal(str(freetown_coords[1] + lng_offset))
            bus.last_location_update = timezone.now()
            bus.save()
            
            print(f"✅ Updated bus {bus.bus_name} with driver {driver.user.first_name}")
            
            # Create location history for the last 2 hours
            now = timezone.now()
            for j in range(24):  # 24 points over 2 hours (every 5 minutes)
                timestamp = now - timedelta(minutes=j * 5)
                
                # Simulate movement along a route
                lat_change = random.uniform(-0.001, 0.001)
                lng_change = random.uniform(-0.001, 0.001)
                latitude = float(bus.current_latitude) + lat_change
                longitude = float(bus.current_longitude) + lng_change
                
                # Random speed between 0-80 km/h
                speed = random.uniform(0, 80)
                
                # Create location record
                BusLocation.objects.create(
                    bus=bus,
                    latitude=latitude,
                    longitude=longitude,
                    speed=speed,
                    accuracy=random.uniform(5, 15),
                    altitude=random.uniform(50, 200),
                    timestamp=timestamp,
                    is_moving=speed > 5
                )
            
            # Create some speed alerts for testing
            if random.choice([True, False]):
                SpeedAlert.objects.create(
                    bus=bus,
                    driver=driver,
                    recorded_speed=random.uniform(85, 120),
                    speed_limit=80,
                    location_latitude=latitude,
                    location_longitude=longitude,
                    severity='medium' if random.choice([True, False]) else 'high',
                    is_acknowledged=False
                )
                print(f"⚠️ Created speed alert for {bus.bus_name}")
    
    # Create geofence areas
    geofences = [
        {
            'name': 'Freetown City Center',
            'center_latitude': 8.4657,
            'center_longitude': -13.2317,
            'radius': 5000,  # 5km radius
            'geofence_type': 'city_limit'
        },
        {
            'name': 'Lungi Airport Zone',
            'center_latitude': 8.6164,
            'center_longitude': -13.1951,
            'radius': 2000,  # 2km radius
            'geofence_type': 'restricted'
        },
        {
            'name': 'Bo City Center',
            'center_latitude': 7.9644,
            'center_longitude': -11.7383,
            'radius': 3000,  # 3km radius
            'geofence_type': 'city_limit'
        }
    ]
    
    for geofence_data in geofences:
        geofence, created = GeofenceArea.objects.get_or_create(
            name=geofence_data['name'],
            defaults=geofence_data
        )
        if created:
            print(f"🎯 Created geofence: {geofence.name}")
    
    # Create route progress for active buses
    routes = list(Route.objects.all())
    if routes:
        for bus in buses[:2]:  # First 2 buses
            route = random.choice(routes)
            RouteProgress.objects.create(
                bus=bus,
                route=route,
                start_time=timezone.now() - timedelta(minutes=random.randint(30, 180)),
                progress_percentage=random.uniform(25, 75),
                distance_covered=random.uniform(10, 50),
                total_distance=random.uniform(60, 120),
                estimated_arrival_time=timezone.now() + timedelta(minutes=random.randint(30, 120)),
                status=random.choice(['in_transit', 'on_time', 'delayed'])
            )
            print(f"🛣️ Created route progress for {bus.bus_name} on {route.origin} → {route.destination}")
    
    print("\n🎉 GPS Test Data Creation Complete!")
    print("\nCreated:")
    print(f"- {len(created_drivers)} drivers with user accounts")
    print(f"- GPS data for {min(3, len(buses))} buses")
    print(f"- Location history (last 2 hours)")
    print(f"- Speed alerts and geofence areas")
    print(f"- Route progress tracking")
    print("\nYou can now:")
    print("1. Visit /gps/ to see the public tracking map")
    print("2. Login as admin to access GPS management")
    print("3. Login as driver to access driver dashboard")
    print("\nTest credentials:")
    print("Admin: admin@wakafine.com / admin123")
    print("Driver: driver1@wakafine.com / driver123")

if __name__ == "__main__":
    create_test_gps_data()