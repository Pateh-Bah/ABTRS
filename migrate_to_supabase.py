#!/usr/bin/env python
"""
Script to migrate data from SQLite to Supabase PostgreSQL
Run this script locally to transfer your data to Supabase
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings')

# Setup Django
django.setup()

from django.core.management import execute_from_command_line
from django.db import connections
from django.core.management.commands.migrate import Command as MigrateCommand

def migrate_to_supabase():
    """Migrate database to Supabase"""
    print("🚀 Starting migration to Supabase...")
    
    # First, run migrations on the new database
    print("📋 Running Django migrations...")
    execute_from_command_line(['manage.py', 'migrate', '--settings=wakafine_bus.settings_production'])
    
    print("✅ Migration completed!")
    print("📝 Next steps:")
    print("1. Go to your Supabase dashboard")
    print("2. Check the 'Table Editor' to see your tables")
    print("3. You may need to create initial data manually or run your seed scripts")
    print("4. Test your Vercel deployment")

if __name__ == '__main__':
    migrate_to_supabase()
