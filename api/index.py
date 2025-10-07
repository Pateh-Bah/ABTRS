import os
import sys
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

try:
    # Add the project root to Python path
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    logger.info(f'Added {project_root} to Python path')

    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings_production')
    logger.info(f'Using settings module: {os.environ["DJANGO_SETTINGS_MODULE"]}')

    # Import Django and setup
    import django
    django.setup()
    logger.info('Django setup completed')

    # Import WSGI application
    from wakafine_bus.wsgi import application
    logger.info('WSGI application imported successfully')

    # Create handler for Vercel
    def handler(request):
        try:
            if request.get('path', '').startswith('/api/health'):
                return {
                    'statusCode': 200,
                    'body': 'Healthy',
                    'headers': {'Content-Type': 'text/plain'}
                }

            return application(request)
        except Exception as e:
            logger.error(f'Request handler error: {str(e)}')
            return {
                'statusCode': 500,
                'body': 'Internal server error',
                'headers': {'Content-Type': 'text/plain'}
            }

    # Export the handler
    app = application

except Exception as e:
    logger.error(f'Startup error: {str(e)}')
    def handler(request):
        return {
            'statusCode': 500,
            'body': f'Application startup failed: {str(e)}',
            'headers': {'Content-Type': 'text/plain'}
        }
    app = handler
