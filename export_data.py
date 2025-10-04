#!/usr/bin/env python
"""
Script to export data from SQLite for import into Supabase
"""

import os
import sys
import django
import json
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings')

# Setup Django
django.setup()

from django.core import serializers
from django.contrib.auth import get_user_model
from routes.models import Route, Terminal
from buses.models import Bus
from bookings.models import Booking

User = get_user_model()

def export_data():
    """Export data from SQLite database"""
    print("📤 Exporting data from SQLite...")
    
    # Export users
    users = User.objects.all()
    users_data = serializers.serialize('json', users)
    
    # Export routes
    routes = Route.objects.all()
    routes_data = serializers.serialize('json', routes)
    
    # Export terminals
    terminals = Terminal.objects.all()
    terminals_data = serializers.serialize('json', terminals)
    
    # Export buses
    buses = Bus.objects.all()
    buses_data = serializers.serialize('json', buses)
    
    # Export bookings
    bookings = Booking.objects.all()
    bookings_data = serializers.serialize('json', bookings)
    
    # Save to files
    with open('exported_users.json', 'w') as f:
        f.write(users_data)
    
    with open('exported_routes.json', 'w') as f:
        f.write(routes_data)
    
    with open('exported_terminals.json', 'w') as f:
        f.write(terminals_data)
    
    with open('exported_buses.json', 'w') as f:
        f.write(buses_data)
    
    with open('exported_bookings.json', 'w') as f:
        f.write(bookings_data)
    
    print("✅ Data exported successfully!")
    print("📁 Files created:")
    print("  - exported_users.json")
    print("  - exported_routes.json")
    print("  - exported_terminals.json")
    print("  - exported_buses.json")
    print("  - exported_bookings.json")
    print("\n📝 Next steps:")
    print("1. After setting up Supabase, you can import this data")
    print("2. Or recreate your data using your existing seed scripts")

if __name__ == '__main__':
    export_data()
