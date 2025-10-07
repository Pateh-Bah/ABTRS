from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
import sys
import os

def debug_view(request):
    """Diagnostic view to check database connection and environment"""
    try:
        # Test database connection
        db_conn = connections['default']
        db_conn.ensure_connection()
        db_status = "Connected"
        
        # Get table list
        with db_conn.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = [row[0] for row in cursor.fetchall()]
        
        # Collect environment info
        env_vars = {
            'DB_NAME': os.getenv('DB_NAME'),
            'DB_HOST': os.getenv('DB_HOST'),
            'DB_PORT': os.getenv('DB_PORT'),
            'DJANGO_SETTINGS_MODULE': os.getenv('DJANGO_SETTINGS_MODULE'),
            'PYTHON_PATH': sys.path,
            'ALLOWED_HOSTS': os.getenv('ALLOWED_HOSTS'),
        }
        
        return JsonResponse({
            'status': 'ok',
            'database': {
                'status': db_status,
                'tables': tables,
                'backend': connections.databases['default']['ENGINE']
            },
            'environment': env_vars
        })
        
    except OperationalError as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'type': 'database',
            'environment': {
                'DB_NAME': os.getenv('DB_NAME'),
                'DB_HOST': os.getenv('DB_HOST'),
                'DB_PORT': os.getenv('DB_PORT'),
                'DJANGO_SETTINGS_MODULE': os.getenv('DJANGO_SETTINGS_MODULE'),
            }
        }, status=500)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'type': 'general'
        }, status=500)