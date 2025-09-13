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
CSRF_TRUSTED_ORIGINS = [o if o.startswith(('http://', 'https://')) else f"https://{o.lstrip('.')}" for o in ALLOWED_HOSTS if o and o != '*']

# Honor X-Forwarded-Proto/SSL from Vercel
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', '1') in ('1','true','True')
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', '1') in ('1','true','True')
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '0' if DEBUG else '3600'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('SECURE_HSTS_INCLUDE_SUBDOMAINS', '0') in ('1','true','True')
SECURE_HSTS_PRELOAD = os.environ.get('SECURE_HSTS_PRELOAD', '0') in ('1','true','True')

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

        cfg = dj_database_url.parse(db_url, conn_max_age=600)
        eng = cfg.get('ENGINE', '')
        if 'postgresql' in eng or 'postgres' in eng:
            opts = cfg.setdefault('OPTIONS', {})
            opts.setdefault('sslmode', 'require')
        DATABASES['default'] = cfg
    except Exception:
        # Fallback to SQLITE if dj_database_url is not available
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
else:
    is_serverless = bool(os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'))
    sqlite_path = '/tmp/db.sqlite3' if is_serverless else (BASE_DIR / 'db.sqlite3')
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': sqlite_path,
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
