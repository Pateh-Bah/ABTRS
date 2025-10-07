#!/usr/bin/env python
"""Test Supabase database connection"""
import os
import sys
import django
from django.db import connections
from django.db.utils import OperationalError

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wakafine_bus.settings")

# Configure database settings
os.environ['DB_HOST'] = 'db.ydexeftnucyjnorycrpd.supabase.co'
os.environ['DB_NAME'] = 'postgres'
os.environ['DB_USER'] = 'postgres'
os.environ['DB_PASSWORD'] = 'Abtrs@2025'
os.environ['DB_PORT'] = '5432'

def test_connection():
    """Test the database connection"""
    try:
        django.setup()
        connection = connections['default']
        connection.ensure_connection()
        print("✅ Successfully connected to Supabase!")
        
        # Get PostgreSQL version
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"\nPostgreSQL Version: {version}")
            
        # List all tables
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            if tables:
                print("\nExisting tables:")
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("\nNo tables found (this is normal for a fresh database)")
                
    except OperationalError as e:
        print("❌ Failed to connect to Supabase!")
        print(f"\nError: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check if your Supabase project is active")
        print("2. Verify your password is correct")
        print("3. Check if your IP is allowed in Supabase dashboard")
        sys.exit(1)
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    test_connection()