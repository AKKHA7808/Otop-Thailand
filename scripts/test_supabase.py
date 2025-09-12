import os
import requests

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    print('Missing SUPABASE_URL or SUPABASE_ANON_KEY in environment')
    raise SystemExit(1)

headers = {
    'apikey': SUPABASE_ANON_KEY,
    'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
}

# Try both with and without trailing slash
for path in ("/rest/v1/", "/rest/v1"):
    try:
        r = requests.get(f"{SUPABASE_URL}{path}", headers=headers, timeout=10)
        print(f'GET {path} ->', r.status_code)
        if r.status_code != 200:
            print('Response body (truncated):', r.text[:500])
    except Exception as e:
        print(f'GET {path} failed:', e)

print('\nNote: a 200 on /rest/v1/ usually means PostgREST is reachable. A 404 may mean no public tables or the anon key lacks permissions.')

print('\nIf you want Django to use Supabase Postgres as its DB, set the full Postgres connection string in DATABASE_URL (in .env) and run migrations:')
print('  DATABASE_URL=postgres://user:password@host:5432/database')
print("  python manage.py migrate")
