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

# Optional: auto-seed data on cold start when DB is empty.
try:
    if os.getenv("AUTO_SEED", "").lower() in ("1", "true", "yes", "on"):
        import django
        django.setup()
        from django.conf import settings as dj_settings
        from django.core.management import call_command
        from otop_search_thailand.models import Product
        import os as _os

        should_seed = False
        try:
            if not Product.objects.exists():
                should_seed = True
        except Exception:
            # If table missing, migration likely just created it; proceed to seed
            should_seed = True

        if should_seed:
            path = _os.getenv("OTOP_JSON_PATH") or getattr(dj_settings, "OTOP_JSON_PATH", "")
            if not (path and _os.path.exists(path)):
                url = _os.getenv("OTOP_JSON_URL", "")
                if url:
                    try:
                        import urllib.request
                        tmp_path = "/tmp/otop.json"
                        urllib.request.urlretrieve(url, tmp_path)
                        if _os.path.exists(tmp_path):
                            path = tmp_path
                    except Exception:
                        path = ""
            if path and _os.path.exists(path):
                try:
                    call_command("import_otop_json", "-i", path, verbosity=0)
                except Exception:
                    pass
except Exception:
    # Seeding is best-effort; never block startup
    pass

# Vercel expects the WSGI app callable to be named `app`
app = get_wsgi_application()
