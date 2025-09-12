import os
import re
import sys
import time
from urllib.request import urlopen

BASE = os.environ.get('OTOP_BASE_URL', 'http://127.0.0.1:8000')

def mask(key: str) -> str:
    if not key:
        return '(empty)'
    if len(key) <= 10:
        return '***'
    return key[:6] + '...' + key[-4:]

def main():
    url = BASE.rstrip('/') + '/map/'
    last_err = None
    for i in range(10):
        try:
            with urlopen(url) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
            break
        except Exception as e:
            last_err = e
            time.sleep(0.5)
    else:
        print('ERR: fetch failed ->', last_err)
        sys.exit(1)

    m = re.search(r'maps\.googleapis\.com/maps/api/js\?key=([A-Za-z0-9_\-]+)', html)
    found = m.group(1) if m else ''
    env_key = os.environ.get('GOOGLE_MAPS_API_KEY', '')

    print('Rendered key (masked):', mask(found))
    print('Env key (masked):     ', mask(env_key))
    print('Match:', bool(found and env_key and (found == env_key)))

if __name__ == '__main__':
    main()
