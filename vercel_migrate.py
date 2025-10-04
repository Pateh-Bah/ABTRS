import os
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
        print("Running Django migrations on Supabase...")
        
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("Database connection successful!")
        
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
            print(f"Created {len(tables)} tables:")
            for table in tables:
                print(f"  - {table[0]}")
        
        print("All migrations completed successfully!")
        return True
        
    except Exception as e:
        print(f"Migration failed: {e}")
        return False

if __name__ == '__main__':
    run_migrations()
