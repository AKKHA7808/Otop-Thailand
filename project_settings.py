import os
from pathlib import Path

# Optionally load .env for local development
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret')

DEBUG = os.environ.get('DJANGO_DEBUG', '1') in ('1', 'true', 'True')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Third-party API keys (safe to keep empty by default)
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')
# Map provider: 'google' or 'leaflet'
MAP_PROVIDER = os.environ.get('MAP_PROVIDER', 'leaflet').lower()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'otop_search_thailand',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'otop_search_thailand.context_processors.global_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.app'

DATABASES = {}
# Prefer DATABASE_URL if provided (e.g., Supabase/Postgres)
db_url = os.environ.get('DATABASE_URL')
if db_url:
    try:
        import dj_database_url

        DATABASES['default'] = dj_database_url.parse(db_url, conn_max_age=600)
    except Exception:
        # Fallback to SQLITE if dj_database_url is not available
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'th'
TIME_ZONE = 'Asia/Bangkok'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Use BigAutoField to avoid auto-created primary key warnings
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
