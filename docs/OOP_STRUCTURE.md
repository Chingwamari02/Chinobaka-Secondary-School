# OOP Structure — Chinobaka Secondary School

## Why OOP was introduced

The project now separates the website into objects with clear responsibilities. This makes the system easier to extend without putting all logic inside route functions.

```text
Browser
   |
   v
PublicController
   |
   v
SchoolContentService
   |
   v
SQLAlchemy Model Objects
   |
   v
SQLite / MySQL database
```

## Main classes

### `PublicController`
Located in `app/routes/public.py`.

Responsible for receiving public web requests and selecting the correct template.

Examples:
- `home()`
- `boarding()`
- `achievements()`
- `student_hierarchy()`
- `contact()`

### `SchoolContentService`
Located in `app/services/school_service.py`.

Responsible for collecting and preparing school content. The controller does not need to know how records are queried.

### Model classes
Located in `app/models.py`.

Examples:
- `SiteSetting`
- `News`
- `Event`
- `BoardingFacility`
- `Achievement`
- `StudentHierarchyMember`

Each model is an object representing a type of information in the system.

## Benefits

1. **Encapsulation** — related data and behaviour are kept in classes.
2. **Reusability** — the service can be reused by other controllers or APIs.
3. **Maintainability** — changes to content retrieval are isolated from page presentation.
4. **Scalability** — new modules can be added as new models/services without rewriting the entire application.
5. **Separation of concerns** — routes, business logic, database models and templates have different responsibilities.

## New modules

- `BoardingFacility` → boarding facilities
- `Achievement` → school achievements
- `StudentHierarchyMember` → student leadership hierarchy
- `SchoolContentService` → retrieves these objects
- `PublicController` → exposes them through public pages
