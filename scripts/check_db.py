import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_settings')

try:
    import dj_database_url  # noqa: F401
except Exception:
    pass

try:
    django.setup()
except Exception as e:
    print('Django setup failed:', e)
    sys.exit(1)

from django.db import connections  # noqa: E402
from django.db.utils import OperationalError  # noqa: E402

alias = 'default'
conn = connections[alias]
print('DATABASE_URL =', os.environ.get('DATABASE_URL', '(not set)'))
try:
    cursor = conn.cursor()
    cursor.execute('SELECT 1;')
    row = cursor.fetchone()
    print('DB connection ok; SELECT 1 ->', row)
    cursor.close()
except OperationalError as e:
    print('OperationalError:', e)
    sys.exit(2)
except Exception as e:
    print('Error querying DB:', e)
    sys.exit(3)
