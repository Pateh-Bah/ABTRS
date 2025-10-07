import os
import sys
from pathlib import Path
import logging
from urllib.parse import urlparse
import io

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

# We'll capture startup errors and expose them in the handler so Vercel doesn't crash silently.
startup_exception = None
wsgi_app = None
try:
    import django
    from django.core.wsgi import get_wsgi_application
    from django.core.management import execute_from_command_line

    django.setup()
    wsgi_app = get_wsgi_application()
    logger.info('Django setup completed successfully')
except Exception as e:
    # Record startup problem; handler will return a helpful message instead of crashing
    startup_exception = e
    logger.error(f'Startup error: {str(e)}')
    import traceback
    logger.error(traceback.format_exc())


def _build_environ(event):
    # Convert Vercel event to a WSGI environ dict
    path = event.get('path', '/')
    query = event.get('query', {}) or {}
    method = event.get('method', 'GET')
    headers = event.get('headers', {}) or {}
    body = event.get('body', '') or ''

    parsed = urlparse(path)
    body_bytes = body.encode('utf-8') if isinstance(body, str) else (body or b'')
    environ = {
        'REQUEST_METHOD': method,
        'SCRIPT_NAME': '',
        'PATH_INFO': parsed.path,
        'QUERY_STRING': '&'.join(f'{k}={v}' for k, v in query.items()),
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': headers.get('x-forwarded-proto', 'https'),
        'wsgi.input': io.BytesIO(body_bytes),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'CONTENT_LENGTH': str(len(body_bytes)) if body_bytes else '0',
    }

    # Add headers
    for key, value in headers.items():
        hk = key.upper().replace('-', '_')
        if hk in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[hk] = value
        else:
            environ[f'HTTP_{hk}'] = value

    return environ


def handler(event, context):
    # Top-level handler called by Vercel
    try:
        # If startup failed, return the recorded startup exception to aid debugging
        if startup_exception is not None:
            msg = f'Application startup failed: {startup_exception!s}'
            logger.error(msg)
            import traceback
            logger.error(traceback.format_exc())
            return {
                'statusCode': 500,
                'body': msg,
                'headers': {'Content-Type': 'text/plain'}
            }

        # Lazy import execute_from_command_line here so migrations endpoint works even if setup delayed
        from django.core.management import execute_from_command_line

        # Quick endpoints that shouldn't require full WSGI handling
        path = event.get('path')
        if path == '/api/migrate':
            try:
                execute_from_command_line(['manage.py', 'migrate', '--noinput'])
                return {'statusCode': 200, 'body': 'Migrations completed successfully', 'headers': {'Content-Type': 'text/plain'}}
            except Exception as e:
                logger.error(f'Migration error: {e!s}')
                return {'statusCode': 500, 'body': f'Migration failed: {e!s}', 'headers': {'Content-Type': 'text/plain'}}

        if path == '/api/health':
            return {'statusCode': 200, 'body': 'Healthy', 'headers': {'Content-Type': 'text/plain'}}

        # Construct WSGI environ and call the application
        environ = _build_environ(event)

        status_headers = {'status': None, 'headers': []}
        body_chunks = []

        def start_response(status, response_headers, exc_info=None):
            status_headers['status'] = status
            status_headers['headers'] = response_headers

            def write(data):
                body_chunks.append(data if isinstance(data, (bytes, bytearray)) else data.encode('utf-8'))

            return write

        result = wsgi_app(environ, start_response)
        try:
            for part in result:
                if isinstance(part, (bytes, bytearray)):
                    body_chunks.append(part)
                else:
                    body_chunks.append(str(part).encode('utf-8'))
        finally:
            if hasattr(result, 'close'):
                try:
                    result.close()
                except Exception:
                    pass

        status_line = status_headers.get('status') or '500 INTERNAL SERVER ERROR'
        try:
            status_code = int(status_line.split()[0])
        except Exception:
            status_code = 500

        # Convert headers to dict (last value wins)
        headers = {k: v for k, v in status_headers.get('headers', [])}

        body = b''.join(body_chunks).decode('utf-8', errors='replace')

        return {'statusCode': status_code, 'headers': headers, 'body': body}

    except Exception as e:
        logger.error(f'Request error: {e!s}')
        import traceback
        logger.error(traceback.format_exc())
        return {'statusCode': 500, 'body': 'Internal server error', 'headers': {'Content-Type': 'text/plain'}}


# For local development convenience
app = wsgi_app
