# Chinobaka Website — Upgrade & Troubleshooting

## Internal Server Error after replacing an older project

The application now includes a lightweight SQLite schema upgrade. You can keep an
older `instance/chinobaka.db` when moving to this version. On startup the app:

1. Creates any missing tables.
2. Adds missing columns for additive model changes.
3. Creates default school settings when none exist.
4. Activates legacy administrator accounts when `is_active` was newly added.
5. Repairs missing news slugs and publication status values.

If a database was manually corrupted, back it up first and remove the local
`instance/chinobaka.db` so a clean database can be created.

## CSRF protection

All POST forms in the public site, authentication pages and admin dashboard now
include a CSRF token. Keep `SECRET_KEY` stable between restarts so existing
sessions and CSRF tokens remain valid.

## First run

```powershell
py -m pip install -r requirements.txt
py run.py
```

Then open:

`http://127.0.0.1:5000/`

For a fresh database, create the first administrator at:

`http://127.0.0.1:5000/admin/setup`

## Production

Set a strong `SECRET_KEY`, keep `FLASK_DEBUG=0`, use HTTPS, and set
`SESSION_COOKIE_SECURE=1`.
