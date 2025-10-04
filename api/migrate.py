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
from django.http import JsonResponse

def handler(request):
    """Handle migration requests"""
    try:
        # Run migrations
        execute_from_command_line(['manage.py', 'migrate'])
        
        return JsonResponse({
            'status': 'success',
            'message': 'Migrations completed successfully'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
