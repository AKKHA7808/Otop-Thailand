import json
from pathlib import Path

path = Path(r'D:\Django\otop\otop.json')
if not path.exists():
    print('FILE_NOT_FOUND', path)
    raise SystemExit(1)

with path.open('rb') as f:
    raw = f.read()
try:
    s = raw.decode('utf-8')
except Exception:
    try:
        s = raw.decode('latin-1')
    except Exception:
        s = raw.decode('utf-8', errors='replace')

data = json.loads(s)
if isinstance(data, dict):
    # try to find list container
    for k in ('items', 'products', 'data', 'results'):
        if k in data and isinstance(data[k], list):
            data = data[k]
            break
    else:
        # find first list value
        for v in data.values():
            if isinstance(v, list):
                data = v
                break

print('TOTAL_ITEMS', len(data) if isinstance(data, list) else 1)

def show_item(i, item):
    print('\n--- ITEM', i, '---')
    if isinstance(item, dict):
        for k, v in list(item.items())[:20]:
            print(repr(k), ':', repr(v)[:120])
    else:
        print('NON_DICT_ITEM:', repr(item)[:200])

if isinstance(data, list):
    for i, item in enumerate(data[:5], start=1):
        show_item(i, item)
else:
    show_item(1, data)
