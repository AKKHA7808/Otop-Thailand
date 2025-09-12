import importlib

libs = ['django', 'requests', 'supabase']
for l in libs:
    try:
        importlib.import_module(l)
        print(f'OK: {l}')
    except Exception as e:
        print(f'ERR: {l} -> {e}')
