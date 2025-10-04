#!/usr/bin/env python
"""
Script to create a comprehensive migration setup for Supabase
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Set Django settings module to development (SQLite)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings')

# Setup Django
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection
from django.apps import apps
from django.core import serializers

def create_migration_setup():
    """Create comprehensive migration setup"""
    print("🚀 Creating Supabase Migration Setup")
    print("=" * 50)
    
    # Show all Django models
    print("\n📱 Django Apps and Models:")
    all_models = []
    for app_config in apps.get_app_configs():
        print(f"\n  App: {app_config.name}")
        for model in app_config.get_models():
            print(f"    - {model._meta.label}")
            all_models.append(model)
    
    # Create migration files
    print(f"\n📋 Creating migration files for {len(all_models)} models...")
    
    # Run makemigrations to ensure all migrations exist
    print("\n🔧 Running makemigrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    # Show existing migrations
    print("\n📋 Existing migration files:")
    for app_config in apps.get_app_configs():
        migrations_dir = Path(app_config.path) / 'migrations'
        if migrations_dir.exists():
            migration_files = list(migrations_dir.glob('*.py'))
            if migration_files:
                print(f"\n  {app_config.name}:")
                for migration_file in migration_files:
                    if migration_file.name != '__init__.py':
                        print(f"    - {migration_file.name}")
    
    # Create a comprehensive migration script for Vercel
    print("\n📝 Creating Vercel migration script...")
    
    migration_script = '''import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings_production')

# Import Django
import django
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection

def run_migrations():
    """Run all Django migrations"""
    try:
        print("🚀 Running Django migrations on Supabase...")
        
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection successful!")
        
        # Run migrations
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=2'])
        
        # Show created tables
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            print(f"\\n📋 Created {len(tables)} tables:")
            for table in tables:
                print(f"  - {table[0]}")
        
        print("\\n✅ All migrations completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == '__main__':
    run_migrations()
'''
    
    with open('vercel_migrate.py', 'w') as f:
        f.write(migration_script)
    
    print("✅ Created vercel_migrate.py")
    
    # Create SQL schema export
    print("\n📝 Creating SQL schema export...")
    try:
        with connection.cursor() as cursor:
            # Get all table creation SQL
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            with open('database_schema.sql', 'w') as f:
                f.write("-- Django Database Schema for Supabase\\n")
                f.write("-- This file contains the SQL schema from your SQLite database\\n\\n")
                
                for table in tables:
                    if table[0]:  # Skip None values
                        f.write(table[0] + ";\\n\\n")
            
            print("✅ Created database_schema.sql")
            
    except Exception as e:
        print(f"⚠️  Could not export SQL schema: {e}")
    
    print("\n🎉 Migration setup completed!")
    print("\n📋 Next steps:")
    print("1. Deploy to Vercel with the environment variables")
    print("2. Visit your-vercel-url.vercel.app/api/migrate")
    print("3. Or run: python vercel_migrate.py (if you can connect locally)")
    print("4. Check your Supabase dashboard to see all tables created")

if __name__ == '__main__':
    create_migration_setup()
