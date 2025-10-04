#!/usr/bin/env python
"""
Script to set up Supabase database with Django migrations
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Set Django settings module to production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings_production')

# Setup Django
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection

def setup_database():
    """Set up the Supabase database"""
    print("🚀 Setting up Supabase database...")
    
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful!")
        
        # Run migrations
        print("📋 Running Django migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Create superuser (optional)
        print("\n👤 Do you want to create a superuser? (y/n)")
        create_superuser = input().lower().strip()
        
        if create_superuser == 'y':
            execute_from_command_line(['manage.py', 'createsuperuser'])
        
        print("\n✅ Database setup completed successfully!")
        print("🎉 Your Django app is now connected to Supabase!")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        print("\n🔍 Troubleshooting:")
        print("1. Check your environment variables")
        print("2. Verify your Supabase database credentials")
        print("3. Make sure your Supabase project is active")

if __name__ == '__main__':
    setup_database()
