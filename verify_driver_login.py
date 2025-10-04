import os
import sys
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings')
django.setup()

from accounts.models import User
from gps_tracking.models import Driver
from django.contrib.auth import authenticate

def test_driver_login_credentials():
    print("🔐 Testing driver login credentials...")
    
    # Test the created driver accounts
    test_credentials = [
        ('driver1', 'password123'),
        ('driver2', 'password123'),
        ('driver3', 'password123'),
    ]
    
    for username, password in test_credentials:
        print(f"\n👤 Testing login for: {username}")
        
        # Test authentication
        user = authenticate(username=username, password=password)
        if user:
            print(f"   ✅ Authentication successful")
            print(f"   Name: {user.first_name} {user.last_name}")
            print(f"   Email: {user.email}")
            
            # Check if driver profile exists
            try:
                driver = Driver.objects.get(user=user)
                print(f"   🚛 Driver Profile: {driver.license_number}")
                
                if driver.assigned_bus:
                    bus = driver.assigned_bus
                    print(f"   🚌 Assigned Bus: {bus.bus_name} ({bus.bus_number}) - ID: {bus.id}")
                    print(f"   📍 This bus should appear on the map with ID {bus.id}")
                else:
                    print(f"   ❌ No bus assigned")
                    
            except Driver.DoesNotExist:
                print(f"   ❌ No driver profile found")
        else:
            print(f"   ❌ Authentication failed")
    
    print("\n" + "="*50)
    print("🗺️  GPS MAP TEST SUMMARY:")
    print("="*50)
    
    # Check which buses should be visible on map
    drivers_with_buses = Driver.objects.exclude(assigned_bus=None)
    
    print(f"Drivers with assigned buses: {drivers_with_buses.count()}")
    
    for driver in drivers_with_buses:
        bus = driver.assigned_bus
        print(f"  🚌 {bus.bus_name} (ID: {bus.id}) - Driver: {driver.user.first_name}")
        print(f"     Login: {driver.user.username} / password123")
        print(f"     Map should show bus icon with ID {bus.id}")
    
    print("\n📱 To test:")
    print("1. Login as any of the drivers above")
    print("2. Visit /gps/ to see the map")
    print("3. Bus icons should display with bus IDs visible")
    print("4. Clicking on icons shows bus details including driver name")

if __name__ == '__main__':
    test_driver_login_credentials()