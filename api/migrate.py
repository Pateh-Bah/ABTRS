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

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wakafine_bus.settings_production')

def handler(event, context):
    """Handle database migrations on Vercel"""
    try:
        import django
        from django.core.management import execute_from_command_line
        
        # Setup Django
        django.setup()
        
        logger.info('Starting database migrations...')
        
        # Run migrations
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        
        logger.info('Database migrations completed successfully')
        
        return {
            'statusCode': 200,
            'body': 'Database migrations completed successfully',
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Origin': '*'
            }
        }
        
    except Exception as e:
        logger.error(f'Migration error: {str(e)}')
        import traceback
        logger.error(traceback.format_exc())
        
        return {
            'statusCode': 500,
            'body': f'Migration failed: {str(e)}',
            'headers': {
                'Content-Type': 'text/plain',
                'Access-Control-Allow-Origin': '*'
            }
        }