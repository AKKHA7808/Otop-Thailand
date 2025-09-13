import json
import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Convert raw OTOP data to JSON (placeholder/sample)'

    def add_arguments(self, parser):
        parser.add_argument('--output', '-o', help='Output JSON path', default='data/otop.json')

    def handle(self, *args, **options):
        out_path = options['output']
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        # If a real raw source exists, convert it here. For now create a small sample.
        sample = [
            {
                'name': 'สินค้า OTOP ตัวอย่าง 1',
                'province': 'Bangkok',
                'category': 'Food',
                'rating': 4.5,
                'price': 120.0,
                'description': 'ตัวอย่างสินค้า OTOP',
                'image_url': '',
                'address': 'Bangkok',
                'phone': '0123456789',
                'latitude': 13.736717,
                'longitude': 100.523186,
            }
        ]

        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(sample, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f'Wrote sample OTOP JSON to {out_path}'))
