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
from django.db import connection
from django.apps import apps

def setup_database():
    """Set up the Supabase database with all Django tables"""
    print("🚀 Setting up Supabase database...")
    print("=" * 50)
    
    try:
        # Test database connection
        print("🔗 Testing database connection...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful!")
        
        # Show current tables (before migrations)
        print("\n📋 Current tables in database:")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            if tables:
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("  (No tables found)")
        
        # Run migrations
        print("\n📋 Running Django migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
        
        # Show tables after migrations
        print("\n📋 Tables after migrations:")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            if tables:
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("  (No tables found)")
        
        # Show Django apps and models
        print("\n📱 Django Apps and Models:")
        for app_config in apps.get_app_configs():
            print(f"\n  App: {app_config.name}")
            for model in app_config.get_models():
                print(f"    - {model._meta.label}")
        
        print("\n✅ Database setup completed successfully!")
        print("🎉 All Django tables have been created in Supabase!")
        
        # Ask about creating superuser
        print("\n👤 Do you want to create a superuser? (y/n)")
        create_superuser = input().lower().strip()
        
        if create_superuser == 'y':
            print("\n🔐 Creating superuser...")
            execute_from_command_line(['manage.py', 'createsuperuser'])
            print("✅ Superuser created successfully!")
        
        print("\n🚀 Next steps:")
        print("1. Your database is ready for Vercel deployment")
        print("2. All tables are created in Supabase")
        print("3. You can now deploy to Vercel")
        print("4. Visit your-vercel-url.vercel.app/admin to access Django admin")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        print("\n🔍 Troubleshooting:")
        print("1. Check your Supabase project is active")
        print("2. Verify your database credentials")
        print("3. Make sure your internet connection is working")
        return False
    
    return True

if __name__ == '__main__':
    setup_database()