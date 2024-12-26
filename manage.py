#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv

def main():
    # Load .env variables
    load_dotenv()
    
    # Get host and port from .env or use defaults
    host = os.getenv('DJANGO_HOST', '127.0.0.1')
    port = os.getenv('DJANGO_PORT', '8000')
    
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ibm_i.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
        
    # Replace the default runserver command with your custom host and port
    args = sys.argv
    if len(args) > 1 and args[1] == 'runserver':
        args = [args[0], 'runserver', f'{host}:{port}']
        
    execute_from_command_line(args)

if __name__ == '__main__':
    main()
