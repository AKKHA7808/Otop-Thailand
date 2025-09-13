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
try:
    if os.getenv("AUTO_MIGRATE", "").lower() in ("1", "true", "yes", "on"): 
        # Optionally run migrations on cold start (useful on serverless)
        import django
        django.setup()
        from django.core.management import call_command
        call_command("migrate", interactive=False, run_syncdb=True)
except Exception:
    # Avoid crashing the cold start if migrations fail; logs go to stderr
    pass

# Vercel expects the WSGI app callable to be named `app`
app = get_wsgi_application()
