# Chinobaka Secondary School Website

This is the current working Flask version of the Chinobaka Secondary School website/system.

## Start the project

From this folder:

```powershell
py -m pip install -r requirements.txt
py run.py
```

Then open `http://127.0.0.1:5000`.

First-time administrator setup: `/admin/setup`.

This version intentionally does **not** require Flask-Migrate commands. The SQLite database tables are created automatically when the application starts.

## Important structure

The Flask package is `app/`. There must not be an `app/app/` folder.

## Current modules

- Public school pages
- Admin login and first-time setup
- News management
- Events management
- Gallery management
- Staff/leadership management
- Downloads management
- Contact messages
- School settings/branding
- Image and document uploads
