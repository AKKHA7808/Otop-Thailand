# Otop-Thailand

เว็บแอป Django สำหรับค้นหา/สำรวจข้อมูลสินค้า OTOP ทั่วประเทศไทย พร้อมหน้าแผนที่และ API พร้อมใช้งาน และเตรียม deploy บน Vercel

## คุณสมบัติหลัก (Features)
- รายการสินค้า OTOP, ค้นหา, หน้าแผนที่, หน้ารายละเอียดจังหวัด
- API: `/api/products.json`, `/api/products.geojson`
- Health check: `/healthz`
- พร้อมใช้งานกับ Vercel (serverless-friendly)

## โครงสร้างที่สำคัญ
- `project_settings.py` — การตั้งค่า Django หลัก (ฐานข้อมูล, static, security)
- `api/wsgi.py` — WSGI entry สำหรับ Vercel (มี auto-migrate/seed แบบเลือกเปิดได้)
- `otop_search_thailand/` — แอปหลัก (models, views, admin, management commands)
- `templates/`, `static/` — เทมเพลตและไฟล์ static
- `vercel.json` — คอนฟิก deploy Vercel

## เริ่มต้นใช้งาน (Local Dev)
```powershell
git clone https://github.com/AKKHA7808/Otop-Thailand.git
cd "Otop-Thailand"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# ตั้งค่า env (ตัวอย่างอยู่ใน .env.example)
copy .env.example .env  # ปรับค่าเพิ่มตามต้องการ

python manage.py migrate --noinput
python manage.py import_otop_json -i "D:\\Django\\otop\\otop.json"  # หรือใช้ OTOP_JSON_URL

$env:DJANGO_DEBUG='1'
python manage.py runserver 0.0.0.0:8000
```

ตรวจสอบ: `http://127.0.0.1:8000/healthz`, `http://127.0.0.1:8000/api/products.json`

## การทดสอบ (Tests)
```powershell
pip install pytest pytest-django
pytest -q
```

## Deploy บน Vercel
1) ตั้งค่า Environment Variables (Production)
- `DJANGO_SECRET_KEY` = คีย์สุ่มยาวๆ
- `DJANGO_DEBUG` = `0`
- `ALLOWED_HOSTS` = `<your>.vercel.app,.vercel.app`
- `AUTO_MIGRATE` = `1`, `AUTO_SEED` = `1` (หลัง seed แล้วปรับเป็น `0`)
- `OTOP_JSON_URL` = URL ไฟล์ JSON (เช่นจาก GitHub Raw)
- `DATABASE_URL` = (ไม่ต้องใส่ หากยังใช้ SQLite ชั่วคราว; ใส่เมื่อใช้ Supabase/Postgres)
- `MAP_PROVIDER` = `leaflet` (หรือ `google` ถ้ามีคีย์)
- `GOOGLE_MAPS_API_KEY` = (ถ้ามี)

2) Deploy ด้วย `vercel.json` ปัจจุบัน
- ใช้ `@vercel/python` กับ `api/wsgi.py`
- buildCommand จะรัน `migrate` + `collectstatic`
- routes ตั้งค่า `/static` → `staticfiles/` และที่เหลือไป `api/wsgi.py`

3) ตรวจหลัง deploy
- `/healthz` = OK
- `/api/products.json` คืนข้อมูล
- หน้าเว็บหลักและ `/map/` แสดงผล

## Contributing
- เปิด PR เป็นส่วนๆ ขนาดเล็ก เน้นมีเทสต์ประกอบ
- รัน `pre-commit` ก่อน commit: `pip install pre-commit && pre-commit install`

## License
[MIT](LICENSE)
