import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings')
django.setup()

from buses.models import Bus
from gps_tracking.models import BusLocation, Driver
from accounts.models import User
from django.utils import timezone

def create_simple_gps_data():
    print("Creating simple GPS test data...")
    
    # Get first 3 buses
    buses = Bus.objects.all()[:3]
    
    if not buses:
        print("ERROR: No buses found! Please create buses first.")
        return
    
    # Create some driver users if they don't exist
    for i, bus in enumerate(buses):
        driver_username = f"driver{i+1}"
        
        # Create driver user if doesn't exist
        user, created = User.objects.get_or_create(
            username=driver_username,
            defaults={
                'first_name': ['Mohamed', 'Aminata', 'Ibrahim'][i],
                'last_name': ['Kamara', 'Sesay', 'Mansaray'][i],
                'email': f'{driver_username}@wakafine.com'
            }
        )
        
        if created:
            user.set_password('password123')
            user.save()
            print("SUCCESS: Created user: {} {}".format(user.first_name, user.last_name))
        
        # Create driver profile if doesn't exist
        driver, created = Driver.objects.get_or_create(
            user=user,
            defaults={
                'license_number': f'SL{10000 + i}',
                'phone_number': f'+232-76-{random.randint(100000, 999999)}',
                'emergency_contact': f'Emergency Contact {i+1}',
                'emergency_contact_phone': f'+232-77-{random.randint(100000, 999999)}',
            }
        )
        
        if created:
            print("SUCCESS: Created driver profile: {}".format(user.first_name))
        
        # Assign driver to bus
        if not bus.current_driver_name:
            bus.current_driver_name = f"{user.first_name} {user.last_name}"
            bus.current_driver_phone = driver.phone_number
            bus.save()
            print("SUCCESS: Assigned {} to {}".format(user.first_name, bus.bus_name))
        
        # Also update the driver's assigned bus
        if not driver.assigned_bus:
            driver.assigned_bus = bus
            driver.save()
    
    # Create recent bus locations for the first 3 buses
    freetown_routes = [
        # Route 1: Central Freetown to Hastings
        [(8.4857, -13.2317), (8.4640, -13.2280), (8.4420, -13.2240), (8.4200, -13.2200), (8.3980, -13.1960), (8.3733, -13.1341)],
        # Route 2: Freetown to Waterloo  
        [(8.4857, -13.2317), (8.4700, -13.2250), (8.4500, -13.2100), (8.4300, -13.1950), (8.4100, -13.1800), (8.3900, -13.1650)],
        # Route 3: Freetown to Aberdeen
        [(8.4857, -13.2317), (8.4800, -13.2200), (8.4750, -13.2100), (8.4700, -13.2000), (8.4650, -13.1900), (8.4600, -13.1800)]
    ]
    
    for i, bus in enumerate(buses[:3]):
        route_points = freetown_routes[i]
        
        # Create location history over the last 30 minutes (more recent)
        for j, (lat, lng) in enumerate(route_points):
            timestamp = timezone.now() - timedelta(minutes=30) + timedelta(minutes=j * 5)
            speed = random.uniform(25, 60)  # km/h
            
            location = BusLocation.objects.create(
                bus=bus,
                latitude=Decimal(str(lat)),
                longitude=Decimal(str(lng)),
                speed=speed,
                heading=random.uniform(0, 360),
                accuracy=random.uniform(5, 15),
                is_moving=speed > 5,
                timestamp=timestamp
            )
            
        print("SUCCESS: Created location history for {}".format(bus.bus_name))
    
    print("\nGPS test data created successfully!")
    print("You should now see bus icons on the map at /gps/")

if __name__ == '__main__':
    create_simple_gps_data()