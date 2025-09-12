<!--
This file is generated to help AI coding agents become productive in this Django project.
Repository scan found no existing AI guidance files; please provide project-specific files
or point me to the codebase root to refine these instructions.
-->
# Copilot / AI agent instructions

Purpose
- Help an AI agent make high-value, low-risk contributions to this Django codebase.

What I need first (quick checks)
- Look for `manage.py`, `requirements.txt` or `pyproject.toml`, `settings.py`, and a top-level `apps/` or project package.
- If any of those are missing, ask the human for the correct project root.

Big picture (how to orient yourself)
- This is a Django web application. Key entry points are `manage.py` and the project's `settings.py`.
- Common directories to inspect: `project_name/` (Django settings & urls), `apps/` or app folders (models, views, templates), `templates/`, `static/`, `migrations/`.
- Dataflow: HTTP requests enter through `urls.py` → views (function or class-based) → serializers/forms → `models.py` → database via `ORM`.

Project layout (this repo)
- `manage.py` — Django CLI entrypoint.
- `settings.py`, `urls.py`, `wsgi.py` — project-level configuration (use these as the authoritative settings files).
- `otop_search_thailand/` — main app. Key files: `models.py`, `views.py`, `admin.py`, and `management/commands/` containing `import_otop_json.py`, `convert_otop_to_json.py`, `seed_th_provinces.py` (data pipeline and seeding commands).
- `templates/` — contains `base.html`, `home.html`, `about.html`, `products_list.html`, `provinces.html`, `province_detail.html`, `search.html`, `map.html`.
- `static/otop_search_thailand/` — styles and scripts plus `assets/img/otop_logo.png` (logo must keep this name where templates expect it).
- `api/wsgi.py` and `vercel.json` — this project is prepared for Vercel (the `api/wsgi.py` file is used for serverless WSGI on Vercel).
- `requirements.txt` — dependency manifest.

Developer workflows (explicit commands)
- Create virtualenv and install deps: `python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt`
- Run development server: `python manage.py runserver`
- Apply migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Run tests: prefer `pytest` if `pytest.ini` exists, otherwise `python manage.py test`.
- Collect static (production): `python manage.py collectstatic --noinput`
Additional repo-specific commands
- Seed Thai provinces: `python manage.py seed_th_provinces`
- Convert/import OTOP data: `python manage.py convert_otop_to_json` then `python manage.py import_otop_json` (check command docstrings for exact args).
- Local Vercel test: Vercel uses `api/wsgi.py`; for local dev prefer `python manage.py runserver`. To run a production-like server locally: `pip install gunicorn; gunicorn settings:wsgi` (adjust module path if needed).

Project-specific conventions (what to look for)
- Settings split: check for `settings/` package or `local_settings.py` — configuration may be environment-specific.
- Apps: each Django app should have `models.py`, `views.py`, `admin.py`, `tests.py`. Follow the existing tests structure when adding tests.
- Templates: prefer per-app `templates/<app>/...` plus a project-level `templates/` for shared layout.
- Static: serve from `static/` in apps; production pipelines usually run `collectstatic`.

Project-specific conventions
- App name: `otop_search_thailand` — maintain this name when adding templates/static paths and imports.
- Logo path: templates expect `static/otop_search_thailand/assets/img/otop_logo.png` — keep file name unchanged when replacing logo.
- Management commands implement the data import pipeline; treat them as the canonical data ingestion path.
- Vercel: `api/wsgi.py` is the entry used by `vercel.json`. Avoid removing `api/wsgi.py` unless you replace the deployment config.

Integration points & external dependencies
- Look for `requirements.txt`, `Pipfile`, `pyproject.toml` for third-party libraries (e.g., `celery`, `drf`, `gunicorn`, `psycopg2`).
- If `celery.py` or `celery` in requirements, treat background tasks as a separate service — avoid changing task signatures without checking consumers.
- If `Dockerfile` or `docker-compose.yml` exists, prefer reproducing commands with `docker-compose up --build` for environment parity.

Integration notes
- `vercel.json` + `api/wsgi.py` indicate deployment target is Vercel. When adjusting `settings.py`, keep an eye on allowed hosts, static handling, and WSGI settings used by Vercel.
- Data flow: the app's management commands are the primary import/transform steps; changes to their output shape require updates to `models.py` and any downstream templates/views.

Code patterns to follow (concrete examples)
- Database migrations: use `makemigrations` and commit migration files. For data migrations prefer `RunPython` in migrations.
- Views: follow existing style — if codebase uses class-based views (`View`/`APIView`), continue that pattern.
- Serializers/Forms: reuse field names and validations from existing serializers (search for `<ModelName>Serializer` or `forms.py`).
- Tests: mirror the structure and fixtures of existing tests. Use factories if `factory_boy` is present.

Safety and low-risk guidelines
- Small, self-contained changes only: prefer documentation, tests, and refactors that preserve public APIs.
- Avoid large-scale settings or database schema changes without human approval.
- When adding dependencies, add them to `requirements.txt` and update lock files if present; run tests.

<!--
ไฟล์นี้เป็นคู่มือสั้นสำหรับ AI coding agents ที่ทำงานกับโปรเจกต์ Django นี้
ปรับปรุงตามโครงสร้างที่มี: ถ้าไฟล์จริงต่างจากด้านล่าง กรุณาชี้ path ให้ผม
-->
# คู่มือสำหรับ Copilot / AI agent (ภาษาไทย)

ภาพรวมสั้น ๆ
- โปรเจกต์เป็นเว็บแอป Django — จุดเข้าใช้งานสำคัญคือ `manage.py` และ `settings.py`.
- แอปหลักคือ `otop_search_thailand/` มี `models.py`, `views.py`, `admin.py` และคำสั่งจัดการข้อมูลใน `management/commands/`.

โครงสร้างสำคัญใน repo นี้
- `manage.py` — CLI ของ Django
- `settings.py`, `urls.py`, `wsgi.py` — การตั้งค่าระดับโปรเจกต์
- `otop_search_thailand/` — แอปหลัก; ดู `management/commands/` สำหรับ pipeline ของข้อมูล (`convert_otop_to_json`, `import_otop_json`, `seed_th_provinces`).
- `templates/` — เทมเพลตหน้าเว็บ (`base.html`, `home.html`, `products_list.html`, `province_detail.html`, ฯลฯ)
- `static/otop_search_thailand/` — CSS/JS และ `assets/img/otop_logo.png` (เทมเพลตคาดว่าจะหาไฟล์นี้)
- `api/wsgi.py` + `vercel.json` — เตรียม deploy บน Vercel
- `requirements.txt` — รายการ dependency

คำสั่งงานที่ใช้บ่อย (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

คำสั่งเฉพาะ repo นี้
- `python manage.py seed_th_provinces`  — สร้างข้อมูลจังหวัดเริ่มต้น
- `python manage.py convert_otop_to_json` — แปลงข้อมูล OTOP เป็น JSON
- `python manage.py import_otop_json` — นำเข้า JSON เข้าฐานข้อมูล
(ตรวจดู docstring ของแต่ละคำสั่งใน `otop_search_thailand/management/commands/` สำหรับ args เพิ่มเติม)

ข้อควรปฏิบัติของโค้ดในโปรเจกต์
- ถ้าเพิ่ม/เปลี่ยน `models.py` ให้สร้าง migration (`makemigrations` → `migrate`) และทดสอบการนำเข้าข้อมูลอีกครั้ง
- ถ้าต้องเพิ่ม API/URL ให้แก้ `urls.py` และ `otop_search_thailand/views.py` ตามรูปแบบที่มีอยู่ (ส่วนใหญ่ใช้ views แบบธรรมดาหรือ CBV)
- เทมเพลตและ static: อย่าเปลี่ยนชื่อไฟล์โลโก้ (`otop_logo.png`) เพราะเทมเพลตอ้างถึงชื่อไฟล์นี้

การ deploy และข้อสังเกต
- Vercel ใช้ `api/wsgi.py` เป็น entrypoint — อย่าเอาไฟล์นี้ออกหากยังใช้ `vercel.json`
- ในการทดสอบตัวใกล้เคียง production ท้องถิ่น: `pip install gunicorn` แล้วรัน `gunicorn settings:wsgi` (ปรับโมดูลตาม path ถ้าจำเป็น)

แนวทางปลอดภัยสำหรับการเปลี่ยนแปลง
- ทำการเปลี่ยนแปลงเล็ก ๆ และแยกเป็น commit เด็ดชัด
- หลีกเลี่ยงการแก้ `settings.py` ครั้งใหญ่โดยไม่ปรึกษาเจ้าของโปรเจกต์
- เมื่อเพิ่ม dependency ให้เพิ่มใน `requirements.txt` และรันเทสต์

ตัวอย่างงานที่ผมช่วยได้ทันที
- เพิ่ม endpoint ใหม่: แก้ `otop_search_thailand/views.py`, เพิ่ม URL ใน `urls.py`, สร้างเทมเพลต/serializer และเขียน test เล็ก ๆ
- ปรับ pipeline นำเข้า: แก้สคริปต์ใน `management/commands/`, สร้าง data migration ถ้าจำเป็น แล้วรัน `import_otop_json` ใหม่

ถ้าต้องการให้ผมแก้ไขต่อ
- ให้ผมเปิดไฟล์ตัวอย่างใน `otop_search_thailand/management/commands/` เพื่อดึง usage ตัวอย่างและฝังลงในคู่มือนี้หรือ
- แปลไฟล์นี้เป็นภาษาอังกฤษ/ไทยฉบับสมบูรณ์ หรือสร้าง `AGENT.md` เพิ่มเติม

แจ้งผมว่าอยากให้ผมทำข้อไหนต่อ ผมจะดำเนินการให้ทันที

การเพิ่มแอป `otop_search_thailand` ในโปรเจกต์
- เพิ่มบรรทัดนี้ใน `settings.py` ถ้ายังไม่มี:
	```python
	INSTALLED_APPS += ["otop_search_thailand"]
	```
- หลังเพิ่มแล้วให้รันคำสั่งต่อไปนี้ (PowerShell):
	```powershell
	python manage.py makemigrations otop_search_thailand
	python manage.py migrate
	python manage.py createsuperuser  # ถ้าต้องการเข้าถึง admin
	```
- ถ้าเพิ่มโมเดลใหม่หรือแก้ schema: สร้าง migration แล้วรัน `migrate` อีกครั้ง ก่อนจะรัน `import_otop_json` เพื่อหลีกเลี่ยงข้อผิดพลาดจาก schema ไม่ตรงกัน
- ตรวจสอบ `otop_search_thailand/admin.py` เพื่อให้แน่ใจว่าโมเดลถูกลงทะเบียนใน Django admin (ถ้าต้องการ)

สิ่งที่ผมเพิ่มใน repo ตอนนี้
- สร้าง/แก้ไฟล์ `otop_search_thailand/models.py` (ปรับ `Province.save()` ให้สร้าง slug แบบ unique)
- สร้างไฟล์ `otop_search_thailand/admin.py` (ลงทะเบียน `Province` และ `Product` พร้อม ModelAdmin)

ถ้าคุณต้องการให้ผมรัน migrations และคำสั่ง data-import ให้ ทำเครื่องหมายอนุญาตแล้วผมจะรันคำสั่งต่อไปนี้ในเทอร์มินัล:

```powershell
python manage.py makemigrations otop_search_thailand
python manage.py migrate
python manage.py createsuperuser  # ถ้าต้องการ
python manage.py seed_th_provinces
python manage.py convert_otop_to_json
python manage.py import_otop_json
```

การตั้งค่า `settings.py` ที่สำคัญ (จากตัวอย่างที่ให้มา)
- ภาษา/โซนเวลา: `LANGUAGE_CODE = "th-th"`, `TIME_ZONE = "Asia/Bangkok"` — ให้ตั้งค่า locale-aware rendering และ timezone-aware datetime
- Templates/Static: `TEMPLATES[0]["DIRS"] = [BASE_DIR / "templates"]`, `STATICFILES_DIRS = [BASE_DIR / "static"]`, `STATIC_ROOT = BASE_DIR / "staticfiles"`
- ไฟล์ข้อมูล OTOP: `OTOP_JSON_PATH` — ค่าเริ่มต้นตัวอย่างคือ `D:\\Django\\otop\\otop.json` (ปรับตามเครื่อง)
- Google Maps: `GOOGLE_MAPS_API_KEY` — ถ้าใช้หน้า `/map/` ต้องตั้งค่านี้ใน env
- Vercel: `WSGI_APPLICATION = "api.wsgi.app"`, `ALLOWED_HOSTS` และ `CSRF_TRUSTED_ORIGINS` ควรมีค่า `.vercel.app` เมื่อ deploy

แนะนำตัวแปร environment ที่ควรมี
- `DJANGO_SECRET_KEY` — ห้ามใส่ใน repo
- `DATABASE_URL` — ถ้าใช้ `django-environ` หรือ `dj-database-url`
- `OTOP_JSON_PATH` — เส้นทางไฟล์ข้อมูล OTOP
- `GOOGLE_MAPS_API_KEY` — คีย์แผนที่

ไฟล์ตัวอย่าง `.env.example` อยู่ด้านล่าง (ผมจะสร้างไฟล์จริงใน repo):

```
DJANGO_SECRET_KEY=changeme
DATABASE_URL=sqlite:///db.sqlite3
OTOP_JSON_PATH=D:\\Django\\otop\\otop.json
GOOGLE_MAPS_API_KEY=
ALLOWED_HOSTS=127.0.0.1,.vercel.app
```
