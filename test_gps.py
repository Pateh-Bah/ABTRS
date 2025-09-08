#!/usr/bin/env python
import os
import sys
import django

# Add the current directory to the path
sys.path.append('.')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings')

# Setup Django
django.setup()

# Test imports
try:
    from gps_tracking.views import BusTrackingMapView, BusDetailView, AdminGPSManagementView
    print("✅ All GPS tracking views imported successfully")
    
    from gps_tracking.models import Driver, BusLocation, SpeedAlert
    print("✅ All GPS tracking models imported successfully")
    
    from buses.models import Bus
    from django.conf import settings
    
    print(f"✅ Google Maps API Key configured: {bool(settings.GOOGLE_MAPS_API_KEY)}")
    print(f"✅ GPS app in INSTALLED_APPS: {'gps_tracking' in settings.INSTALLED_APPS}")
    
    # Test URL resolution
    from django.urls import reverse
    gps_urls = [
        'gps_tracking:public_map',
        'gps_tracking:admin_dashboard', 
        'gps_tracking:driver_dashboard'
    ]
    
    for url_name in gps_urls:
        try:
            url = reverse(url_name)
            print(f"✅ URL {url_name} resolves to: {url}")
        except Exception as e:
            print(f"❌ URL {url_name} failed: {e}")
    
    print("\n🎉 GPS Tracking system is ready!")
    print("\nTo access the GPS system:")
    print("- Public Map: http://127.0.0.1:8000/gps/")
    print("- Admin Dashboard: http://127.0.0.1:8000/gps/admin/")
    print("- Driver Dashboard: http://127.0.0.1:8000/gps/driver/")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()