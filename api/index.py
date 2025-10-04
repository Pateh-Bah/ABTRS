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

# Import WSGI application
from wakafine_bus.wsgi import application

# Export the WSGI application
app = application
