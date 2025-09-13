import os
import sys

import django

# Ensure project root is on sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Detect settings module: try 'project_settings', fallback to 'settings'
settings_module = 'project_settings'
try:
    __import__(settings_module)
except ModuleNotFoundError:
    settings_module = 'settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
django.setup()

from otop_search_thailand.models import Product


def show_products(limit=10):
    qs = Product.objects.select_related('province').all().order_by('id')[:limit]
    for p in qs:
        province_name = p.province.name if getattr(p, 'province', None) else 'None'
        print(f"ID: {p.id} | Name: {p.name!r} | Province: {province_name}")


if __name__ == '__main__':
    show_products()
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_settings')
import django

django.setup()

from otop_search_thailand.models import Product

qs = Product.objects.select_related('province').all()[:10]
for p in qs:
    province = getattr(p, 'province', None)
    province_name = province.name if province else '(no province)'
    updated = getattr(p, 'updated_at', None)
    print(p.id, repr(p.name)[:80], province_name, updated)

print('Total products:', Product.objects.count())
