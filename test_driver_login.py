import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings')
django.setup()

from accounts.models import User
from gps_tracking.models import Driver, BusLocation
from buses.models import Bus
from django.utils import timezone
from decimal import Decimal
import random

def test_driver_login():
    print("🔐 Testing driver login and bus visibility...")
    
    # Get test drivers
    drivers = Driver.objects.all()[:3]
    
    for driver in drivers:
        print(f"\n👤 Driver: {driver.user.first_name} {driver.user.last_name}")
        print(f"   Username: {driver.user.username}")
        print(f"   License: {driver.license_number}")
        
        # Check assigned bus
        if driver.assigned_bus:
            bus = driver.assigned_bus
            print(f"   🚌 Assigned Bus: {bus.bus_name} ({bus.bus_number})")
            print(f"      Bus ID: {bus.id}")
            print(f"      Driver on Bus: {bus.current_driver_name}")
            
            # Get latest location
            latest_location = BusLocation.objects.filter(bus=bus).order_by('-timestamp').first()
            if latest_location:
                time_diff = timezone.now() - latest_location.timestamp
                is_online = time_diff.total_seconds() < 600  # 10 minutes
                print(f"      📍 Location: {latest_location.latitude}, {latest_location.longitude}")
                print(f"      ⏱️  Last Update: {int(time_diff.total_seconds() / 60)} minutes ago")
                print(f"      🟢 Online: {'Yes' if is_online else 'No'}")
                print(f"      🏃 Moving: {'Yes' if latest_location.is_moving else 'No'}")
                print(f"      💨 Speed: {latest_location.speed:.1f} km/h")
            else:
                print(f"      ❌ No location data")
        else:
            print(f"   ❌ No bus assigned")
    
    print("\n📊 Summary:")
    total_drivers = Driver.objects.count()
    drivers_with_buses = Driver.objects.exclude(assigned_bus=None).count()
    buses_with_locations = Bus.objects.filter(location_history__isnull=False).distinct().count()
    
    print(f"   Total Drivers: {total_drivers}")
    print(f"   Drivers with Buses: {drivers_with_buses}")
    print(f"   Buses with GPS Data: {buses_with_locations}")

if __name__ == '__main__':
    test_driver_login()