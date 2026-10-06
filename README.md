# Chinobaka Secondary School Website — OOP Edition

A Flask + SQLAlchemy school website designed with an object-oriented structure.

## Run

```powershell
py -m pip install -r requirements.txt
py run.py
```

Open `http://127.0.0.1:5000`.

First-time admin setup: `http://127.0.0.1:5000/admin/setup`

## New public sections

- `/boarding` — Boarding Facilities
- `/achievements` — School Achievements
- `/students-hierarchy` — Student Leadership / Hierarchy

## OOP structure

```text
app/
├── models.py                    # SQLAlchemy domain classes
├── services/
│   └── school_service.py        # SchoolContentService business logic
├── routes/
│   ├── public.py                # PublicController + route registration
│   ├── auth.py
│   └── admin.py
├── templates/
│   └── public/
│       ├── boarding.html
│       ├── achievements.html
│       └── student_hierarchy.html
└── static/
```

### Main OOP classes

- `AdminUser`, `SiteSetting`, `News`, `Event`, `GalleryItem`, `StaffMember`, `Download`, `ContactMessage`
- `BoardingFacility`
- `Achievement`
- `StudentHierarchyMember`
- `SchoolContentService`
- `PublicController`

The controller handles web requests, while `SchoolContentService` handles assembling school content. SQLAlchemy model classes represent the application's data/domain objects.

## Database

The project uses SQLite by default and automatically creates new tables when the application starts. Existing databases are not deleted.

## Notes

The three new sections use safe placeholder content when no records have been entered yet. This prevents the website from appearing broken while the school administration is preparing official information.
