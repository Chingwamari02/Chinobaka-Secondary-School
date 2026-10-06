# Chinobaka Secondary School Website — OOP Edition

A Flask + SQLAlchemy school website with a public-facing site and secure administration dashboard.

## Features

1. Contact and enquiry messaging
2. News and announcements
3. Teachers and staff directory
4. Online admissions application/enquiry
5. Admin CMS
6. School gallery
7. Downloads/documents
8. Events calendar/list
9. Site-wide search
10. Security hardening (CSRF, secure cookies, password hashing, login throttling, upload validation and security headers)
11. Responsive mobile/tablet/desktop layouts
12. Boarding facilities
13. Achievements
14. Student leadership hierarchy

## OOP structure

- `app/models.py` — domain classes mapped to database tables
- `app/services/school_service.py` — reusable application/service layer
- `app/routes/` — controller/route layer
- `app/templates/` — presentation layer
- `app/static/` — CSS and JavaScript

## Run

```powershell
py -m pip install -r requirements.txt
py run.py
```

Open `http://127.0.0.1:5000`.

First-time setup: `/admin/setup`.

### Production security

Set a strong random `SECRET_KEY`, set `FLASK_DEBUG=0`, and use HTTPS with `SESSION_COOKIE_SECURE=1`.
