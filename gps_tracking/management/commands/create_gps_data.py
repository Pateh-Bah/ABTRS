from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from buses.models import Bus
from routes.models import Route
from gps_tracking.models import Driver, BusLocation, SpeedAlert, RouteProgress, GeofenceArea
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test GPS data for development and testing'

    def handle(self, *args, **options):
        self.stdout.write("🚌 Creating GPS Test Data...")
        
        # Create or get admin user
        try:
            admin_user = User.objects.get(email='admin@wakafine.com')
            self.stdout.write(f"✅ Found existing admin user: {admin_user.email}")
        except User.DoesNotExist:
            admin_user = User.objects.create_user(
                username='gps_admin',
                email='admin@wakafine.com',
                password='admin123',
                first_name='GPS',
                last_name='Admin',
                phone_number='+23276123456',
                role='admin',
                is_staff=True,
                is_superuser=True,
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Created admin user: {admin_user.email}"))
        
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
        ]
        
        created_drivers = []
        for driver_data in drivers_data:
            try:
                user = User.objects.get(email=driver_data['email'])
                self.stdout.write(f"✅ Found existing driver user: {user.email}")
            except User.DoesNotExist:
                user = User.objects.create_user(
                    username=driver_data['email'].split('@')[0] + '_driver',
                    email=driver_data['email'],
                    password='driver123',
                    first_name=driver_data['first_name'],
                    last_name=driver_data['last_name'],
                    phone_number=driver_data['phone_number'],
                    role='staff',  # Drivers are staff members
                )
                self.stdout.write(f"✅ Created driver user: {user.email}")
            
            # Create driver profile
            driver, created = Driver.objects.get_or_create(
                user=user,
                defaults={
                    'license_number': driver_data['license_number'],
                    'phone_number': driver_data['phone_number'],
                    'is_active': True,
                }
            )
            created_drivers.append(driver)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created driver profile: {driver.user.first_name} {driver.user.last_name}"))
        
        # Get or create buses
        buses = list(Bus.objects.all())
        if not buses:
            self.stdout.write(self.style.ERROR("❌ No buses found. Please create buses first."))
            return
        
        # Assign drivers to buses and add GPS data
        freetown_coords = (8.4657, -13.2317)  # Freetown coordinates
        
        for i, bus in enumerate(buses[:2]):  # Limit to 2 buses for testing
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
                
                self.stdout.write(self.style.SUCCESS(f"✅ Updated bus {bus.bus_name} with driver {driver.user.first_name}"))
                
                # Create location history for the last hour
                now = timezone.now()
                for j in range(12):  # 12 points over 1 hour (every 5 minutes)
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
        
        # Create geofence area
        geofence, created = GeofenceArea.objects.get_or_create(
            name='Freetown City Center',
            defaults={
                'center_latitude': 8.4657,
                'center_longitude': -13.2317,
                'radius_meters': 5000,  # 5km radius
                'area_type': 'terminal'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"🎯 Created geofence: {geofence.name}"))
        
        self.stdout.write(self.style.SUCCESS("\n🎉 GPS Test Data Creation Complete!"))
        self.stdout.write("Test credentials:")
        self.stdout.write("Admin: admin@wakafine.com / admin123")
        self.stdout.write("Driver: driver1@wakafine.com / driver123")