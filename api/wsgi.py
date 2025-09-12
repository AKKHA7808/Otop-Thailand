import os
import sys
from pathlib import Path

# Ensure project root is on sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Use the project's settings module created during setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_settings")

from django.core.wsgi import get_wsgi_application

# Vercel expects the WSGI app callable to be named `app`
app = get_wsgi_application()
