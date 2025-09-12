import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_settings')
django.setup()

from otop_search_thailand.models import Product


def show_products(limit=10):
    qs = Product.objects.select_related('province').all().order_by('id')[:limit]
    for p in qs:
        print(f"ID: {p.id} | Name: {p.name!r} | Province: {p.province.name if p.province else 'None'} | Updated: {p.updated_at if hasattr(p, 'updated_at') else 'N/A'}")


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
