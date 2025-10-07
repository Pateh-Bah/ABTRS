import os
import sys
from pathlib import Path
import logging
from urllib.parse import urlparse

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

try:
    import django
    from django.core.wsgi import get_wsgi_application
    from django.core.management import execute_from_command_line
    
    django.setup()
    wsgi_app = get_wsgi_application()
    logger.info('Django setup completed successfully')
    
    def handler(event, context):
        try:
            # Log the incoming request
            logger.info(f"Handling request: {event.get('path', 'unknown path')}")
            
            # Handle /api/migrate endpoint
            if event.get('path') == '/api/migrate':
                try:
                    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
                    return {
                        'statusCode': 200,
                        'body': 'Migrations completed successfully',
                        'headers': {'Content-Type': 'text/plain'}
                    }
                except Exception as e:
                    logger.error(f'Migration error: {str(e)}')
                    return {
                        'statusCode': 500,
                        'body': f'Migration failed: {str(e)}',
                        'headers': {'Content-Type': 'text/plain'}
                    }
            
            # Handle /api/health endpoint
            if event.get('path') == '/api/health':
                return {
                    'statusCode': 200,
                    'body': 'Healthy',
                    'headers': {'Content-Type': 'text/plain'}
                }
            
            # Convert Vercel event to WSGI environ
            path = event.get('path', '/')
            query = event.get('query', {})
            method = event.get('method', 'GET')
            headers = event.get('headers', {})
            body = event.get('body', '')
            
            parsed = urlparse(path)
            environ = {
                'REQUEST_METHOD': method,
                'SCRIPT_NAME': '',
                'PATH_INFO': parsed.path,
                'QUERY_STRING': '&'.join(f'{k}={v}' for k, v in query.items()),
                'SERVER_PROTOCOL': 'HTTP/1.1',
                'wsgi.version': (1, 0),
                'wsgi.url_scheme': 'https',
                'wsgi.input': body.encode() if body else b'',
                'wsgi.errors': sys.stderr,
                'wsgi.multithread': False,
                'wsgi.multiprocess': False,
                'wsgi.run_once': False,
            }
            
            # Add headers
            for key, value in headers.items():
                key = key.upper().replace('-', '_')
                if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                    key = f'HTTP_{key}'
                environ[key] = value
            
            # Call the WSGI app
            response_body = []
            
            def start_response(status, response_headers, exc_info=None):
                return response_body.append
            
            result = wsgi_app(environ, start_response)
            response_body.extend(result)
            
            return {
                'statusCode': int(response_body[0].split()[0]),
                'headers': dict(response_headers),
                'body': b''.join(response_body[1:]).decode('utf-8')
            }
            
        except Exception as e:
            logger.error(f'Request error: {str(e)}')
            import traceback
            logger.error(traceback.format_exc())
            return {
                'statusCode': 500,
                'body': 'Internal server error',
                'headers': {'Content-Type': 'text/plain'}
            }
    
    # For local development
    app = wsgi_app
    
except Exception as e:
    logger.error(f'Startup error: {str(e)}')
    import traceback
    logger.error(traceback.format_exc())
    
    def handler(event, context):
        return {
            'statusCode': 500,
            'body': f'Application startup failed: {str(e)}',
            'headers': {'Content-Type': 'text/plain'}
        }
    
    app = None
