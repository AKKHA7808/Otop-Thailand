import urllib.request

url = 'http://127.0.0.1:8000/about/'
try:
    with urllib.request.urlopen(url, timeout=5) as r:
        data = r.read(1000)
        print(data.decode('utf-8', errors='replace'))
except Exception as e:
    print('ERROR:', e)
