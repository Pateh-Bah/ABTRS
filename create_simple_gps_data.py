#!/usr/bin/env python
"""
Create sample GPS test data for demonstration
"""
import os
import sys
import django

# Add the current directory to the path
sys.path.append('.')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings')

# Setup Django
django.setup()

from buses.models import Bus
from gps_tracking.models import Driver, BusLocation
from django.contrib.auth.models import User
from datetime import datetime
import random

def create_gps_test_data():
    """Create sample GPS test data"""
    print("🚀 Creating GPS Test Data...")
    print("=" * 40)

    # Create some test buses
    buses_data = [
        {"bus_number": "WF001", "bus_name": "Freetown Express 1", "bus_type": "standard", "seat_capacity": 25},
        {"bus_number": "WF002", "bus_name": "Freetown Express 2", "bus_type": "standard", "seat_capacity": 25},
        {"bus_number": "WF003", "bus_name": "Freetown Express 3", "bus_type": "large", "seat_capacity": 35},
        {"bus_number": "WF004", "bus_name": "Freetown Express 4", "bus_type": "mini", "seat_capacity": 14},
        {"bus_number": "WF005", "bus_name": "Freetown Express 5", "bus_type": "standard", "seat_capacity": 25}
    ]

    created_buses = []
    for bus_data in buses_data:
        bus, created = Bus.objects.get_or_create(
            bus_number=bus_data["bus_number"],
            defaults={
                "bus_name": bus_data["bus_name"],
                "bus_type": bus_data["bus_type"],
                "seat_capacity": bus_data["seat_capacity"],
                "is_active": True
            }
        )
        status = "Created" if created else "Found"
        print(f"✅ {status} bus: {bus.bus_number} - {bus.bus_name}")
        created_buses.append(bus)

    print(f"\n📊 Total buses in system: {Bus.objects.count()}")

    # Create sample locations for buses (around Freetown area)
    freetown_locations = [
        (8.4606, -13.2317),  # Central Freetown
        (8.4657, -13.2317),  # East End
        (8.4556, -13.2417),  # West End
        (8.4706, -13.2217),  # Hill Station
        (8.4506, -13.2517),  # Aberdeen
    ]

    print("\n📍 Creating bus locations...")
    
    # Clear existing locations to avoid duplicates
    BusLocation.objects.all().delete()
    print("✅ Cleared existing bus locations")
    
    for i, bus in enumerate(created_buses[:5]):
        lat, lng = freetown_locations[i]
        # Add some random variation
        lat += random.uniform(-0.01, 0.01)
        lng += random.uniform(-0.01, 0.01)
        
        location = BusLocation.objects.create(
            bus=bus,
            latitude=lat,
            longitude=lng,
            speed=random.uniform(0, 60),
            heading=random.uniform(0, 360),
            accuracy=random.uniform(5, 20),
            is_moving=random.choice([True, False])
        )
        
        print(f"✅ Created location for {bus.bus_number}: ({lat:.4f}, {lng:.4f})")

    print(f"\n📊 Total bus locations: {BusLocation.objects.count()}")
    print("\n🎉 GPS test data creation completed!")
    print("\nYou can now view buses on the map at:")
    print("- Public Map: http://127.0.0.1:8000/gps/")
    print("- All authenticated users will see the GPS nav component")

if __name__ == '__main__':
    create_gps_test_data()