# Database additions

The application automatically creates these tables on startup through SQLAlchemy.

## boarding_facility
- id
- name
- description
- capacity
- facilities
- image_filename
- status
- sort_order
- created_at

## achievement
- id
- title
- category
- year
- description
- image_filename
- sort_order
- created_at

## student_hierarchy_member
- id
- level
- title
- description
- sort_order
- created_at

Existing tables are preserved. The application does not delete the existing SQLite database.
