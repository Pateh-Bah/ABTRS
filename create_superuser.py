#!/usr/bin/env python
"""
Script to create Django superuser for Supabase database
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Set environment variables for Supabase connection
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings_production')
os.environ.setdefault('DB_HOST', 'db.ydexeftnucyjnorycrpd.supabase.co')
os.environ.setdefault('DB_NAME', 'postgres')
os.environ.setdefault('DB_USER', 'postgres')
os.environ.setdefault('DB_PASSWORD', 'Abtrs@2025')
os.environ.setdefault('DB_PORT', '5432')
os.environ.setdefault('SECRET_KEY', ')G2(AjgvT6Rc7@oY(laWNKW&!JuRnl+SMz9J17aiUjf#kcZOBz')
os.environ.setdefault('DEBUG', 'False')

# Setup Django
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser():
    """Create a Django superuser"""
    print("Creating Django superuser...")
    print("=" * 40)
    
    try:
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("Database connection successful!")
        
        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            print("Superuser already exists!")
            superuser = User.objects.filter(is_superuser=True).first()
            print(f"Username: {superuser.username}")
            print(f"Email: {superuser.email}")
        else:
            print("No superuser found. Creating one...")
            execute_from_command_line(['manage.py', 'createsuperuser'])
            print("Superuser created successfully!")
        
        print("\nAdmin access:")
        print("- URL: /admin")
        print("- Use your superuser credentials to login")
        
    except Exception as e:
        print(f"Error creating superuser: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure migrations have been run first")
        print("2. Check your database connection")
        print("3. Verify environment variables are correct")

if __name__ == '__main__':
    create_superuser()
