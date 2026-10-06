# Chinobaka Website — Feature & Security Checklist

## Public features
- Contact/enquiry form stored in the database.
- News and announcements with admin publishing.
- Teachers and staff directory.
- Online admissions enquiry/application form.
- Gallery and downloadable documents.
- Events calendar plus upcoming events.
- Site-wide search across major content areas.
- Boarding facilities.
- Achievements.
- Student leadership hierarchy.
- Responsive navigation and layouts for phone, tablet and desktop.

## Admin CMS
Administrators can manage news, events, gallery items, staff, documents, messages, admissions applications, boarding facilities, achievements, student leaders, school settings and the administrator account.

## Security measures
- Flask-WTF CSRF protection for forms.
- Passwords stored using Werkzeug password hashing.
- Login-attempt throttling after repeated failures.
- HTTP-only and SameSite session cookies.
- Optional Secure cookies for HTTPS deployments.
- Upload extension validation and randomized filenames.
- Maximum request content length.
- Security response headers including X-Content-Type-Options, X-Frame-Options, Referrer-Policy and Permissions-Policy.
- HSTS is enabled automatically when debug mode is off.

## Production checklist
1. Set a strong `SECRET_KEY` in `.env`.
2. Set `FLASK_DEBUG=0`.
3. Deploy behind HTTPS and set `SESSION_COOKIE_SECURE=1`.
4. Back up the SQLite database or use a managed database for production.
5. Replace placeholder school contact information with verified information.
