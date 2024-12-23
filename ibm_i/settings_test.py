from .settings import *

DEBUG = True  # Developers may need to debug
ALLOWED_HOSTS = ['api-test.yourdomain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_db',
        'USER': 'test_user',
        'PASSWORD': 'test_password',
        'HOST': 'test-db-host',
        'PORT': '5432',
    }
}

# Use a different secret key for testing
SECRET_KEY = 'your-test-secret-key'

# Reduce security for ease of testing (ensure HTTPS for production-like tests)
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

