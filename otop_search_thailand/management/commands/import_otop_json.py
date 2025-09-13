import json
import os

from django.core.management.base import BaseCommand, CommandError
from django.db import DatabaseError, IntegrityError, transaction


class Command(BaseCommand):
    help = 'Import OTOP products from JSON into the database (upsert mode)'

    def add_arguments(self, parser):
        parser.add_argument('--input', '-i', help='Input JSON path', default='data/otop.json')
        parser.add_argument(
            '--dry-run', action='store_true', help='Simulate import without writing to the database'
        )

    def handle(self, *args, **options):
        in_path = options.get('input')
        dry_run = bool(options.get('dry_run'))

        if not in_path or not os.path.exists(in_path):
            raise CommandError(f'Input file not found: {in_path}')

        from otop_search_thailand.models import Product, Province

        with open(in_path, 'r', encoding='utf-8') as f:
            raw = json.load(f)

        # Normalize various possible JSON shapes to a list of dicts
        data = raw
        if isinstance(raw, dict):
            for k in ('items', 'products', 'data', 'results'):
                if k in raw and isinstance(raw[k], list):
                    data = raw[k]
                    break
            else:
                for v in raw.values():
                    if isinstance(v, list):
                        data = v
                        break
                else:
                    data = [raw]

        if not isinstance(data, list):
            raise CommandError('Unsupported JSON structure: expected list or object')

        created = 0
        updated = 0
        skipped = 0
        errors_log = []

        os.makedirs(os.path.dirname(in_path), exist_ok=True)
        err_log_path = os.path.join(os.path.dirname(in_path), 'import_errors.log')

        for idx, item in enumerate(data, start=1):
            # If the item is a JSON string, try to parse it
            if isinstance(item, str):
                try:
                    item = json.loads(item)
                except Exception as e:
                    skipped += 1
                    errors_log.append((idx, 'invalid_json_string', str(e), item))
                    continue

            if not isinstance(item, dict):
                skipped += 1
                errors_log.append((idx, 'not_a_object', 'Item is not a JSON object', repr(item)))
                continue

            try:
                # Use a transaction for each item to avoid partial writes on error
                with transaction.atomic():
                    prov_name = (
                        item.get('province')
                        or item.get('จังหวัด')
                        or item.get('province_name')
                        or item.get('อำเภอ')
                        or 'Unknown'
                    )
                    province, _ = Province.objects.get_or_create(name=prov_name)

                    def pick(*keys, default=''):
                        for k in keys:
                            if k in item and item[k] not in (None, ''):
                                return item[k]
                        return default

                    raw_name = pick('name', 'title', 'ชื่อสินค้า OTOP', 'ชื่อสินค้า', default='Unnamed')
                    raw_address = pick('address', 'ที่อยู่', 'ชื่อสถานที่จัดจำหน่าย', default='')
                    raw_phone = pick('phone', 'เบอร์โทรศัพท์', default='')
                    raw_lat = pick('latitude', 'LAT', 'lat', default=None)
                    raw_lng = pick('longitude', 'LONG', 'lng', default=None)

                    phone = ''
                    if raw_phone is not None:
                        phone = str(raw_phone).strip()

                    try:
                        latitude = float(raw_lat) if raw_lat not in (None, '') else None
                    except Exception:
                        latitude = None
                    try:
                        longitude = float(raw_lng) if raw_lng not in (None, '') else None
                    except Exception:
                        longitude = None

                    incoming = {
                        'category': str(pick('category', 'ชนิด', default='')),
                        'rating': float(pick('rating', 'คะแนน', default=0.0) or 0.0),
                        'price': float(pick('price', 'ราคา', default=0.0) or 0.0),
                        'description': str(pick('description', 'รายละเอียด', default='')),
                        'image_url': str(pick('image_url', 'image', 'รูปภาพ', default='')),
                        'address': str(raw_address),
                        'phone': phone,
                        'latitude': latitude,
                        'longitude': longitude,
                    }

                    product_name = str(raw_name)
                    if not product_name:
                        raise ValueError('Missing product name')

                    defaults = {k: v for k, v in incoming.items() if v not in (None, '')}

                    if dry_run:
                        exists = Product.objects.filter(
                            name=product_name, province=province
                        ).exists()
                        if exists:
                            if defaults:
                                updated += 1
                        else:
                            created += 1
                    else:
                        obj, created_flag = Product.objects.update_or_create(
                            name=product_name,
                            province=province,
                            defaults=defaults,
                        )

                        if created_flag:
                            created += 1
                        else:
                            if defaults:
                                updated += 1

            except IntegrityError as e:
                skipped += 1
                errors_log.append((idx, 'IntegrityError', str(e), item))
            except DatabaseError as e:
                skipped += 1
                errors_log.append((idx, 'DatabaseError', str(e), item))
            except Exception as e:
                skipped += 1
                errors_log.append((idx, type(e).__name__, str(e), item))

        # Write errors to log file for inspection
        if errors_log:
            try:
                with open(err_log_path, 'w', encoding='utf-8') as ef:
                    for rec in errors_log:
                        ef.write(
                            json.dumps(
                                {
                                    'index': rec[0],
                                    'error_type': rec[1],
                                    'message': rec[2],
                                    'item': rec[3],
                                },
                                ensure_ascii=False,
                            )
                        )
                        ef.write('\n')
                self.stdout.write(
                    self.style.WARNING(
                        f'Wrote {len(errors_log)} import error records to {err_log_path}'
                    )
                )
            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Failed to write error log: {e}'))

        self.stdout.write(
            self.style.SUCCESS(
                f'Imported {created} products. Updated {updated}. Skipped {skipped} invalid entries.'
            )
        )
