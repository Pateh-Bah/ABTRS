import os
import sys
import django
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings')
django.setup()

from buses.models import Bus
from gps_tracking.models import BusLocation

# Test the API data
def test_api_data():
    print("🔍 Testing GPS API data...")
    
    # Get the most recent location for each active bus
    latest_locations = []
    active_buses = Bus.objects.filter(is_active=True)
    
    print(f"Active buses found: {active_buses.count()}")
    
    for bus in active_buses:
        latest_location = BusLocation.objects.filter(bus=bus).order_by('-timestamp').first()
        if latest_location:
            latest_locations.append(latest_location)
            print(f"✅ {bus.bus_name} ({bus.bus_number}) - Last location: {latest_location.timestamp}")
        else:
            print(f"❌ {bus.bus_name} ({bus.bus_number}) - No location data")
    
    print(f"\nBuses with location data: {len(latest_locations)}")
    
    # Format data like the API
    data = []
    for location in latest_locations:
        # Check if location is recent (within last 10 minutes)
        time_diff = timezone.now() - location.timestamp
        is_online = time_diff.total_seconds() < 600  # 10 minutes
        
        bus_data = {
            'bus_id': location.bus.id,
            'bus_number': location.bus.bus_number,
            'bus_name': location.bus.bus_name,
            'latitude': float(location.latitude),
            'longitude': float(location.longitude),
            'speed': float(location.speed),
            'heading': float(location.heading) if location.heading else 0,
            'timestamp': location.timestamp.isoformat(),
            'is_moving': location.is_moving,
            'is_online': is_online,
            'accuracy': float(location.accuracy) if location.accuracy else None,
            'route_name': location.bus.assigned_route.name if location.bus.assigned_route else None,
            'minutes_ago': int(time_diff.total_seconds() / 60),
            'driver_name': location.bus.current_driver_name if location.bus.current_driver_name else None,
        }
        data.append(bus_data)
    
    api_response = {
        'success': True,
        'buses': data,
        'total_buses': len(data),
        'online_buses': sum(1 for bus in data if bus['is_online']),
        'timestamp': timezone.now().isoformat()
    }
    
    print(f"\n📊 API Response Structure:")
    print(f"Success: {api_response['success']}")
    print(f"Total buses: {api_response['total_buses']}")
    print(f"Online buses: {api_response['online_buses']}")
    
    if data:
        print(f"\n🚌 Sample bus data:")
        sample = data[0]
        for key, value in sample.items():
            print(f"  {key}: {value}")
    
    return api_response

if __name__ == '__main__':
    test_api_data()