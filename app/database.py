"""Database initialization and lightweight SQLite schema migration helpers.

The project is intentionally small and uses SQLite for local development.  The
helpers below make upgrades safer by creating newly-added tables and adding
missing columns when an older Chinobaka database is reused.
"""
from sqlalchemy import inspect, text

from .extensions import db
from .models import AdminUser, News, SiteSetting
from .utils import unique_slug


def _add_missing_columns():
    """Add model columns that are missing from an existing SQLite database.

    SQLAlchemy's ``create_all`` only creates missing tables; it does not alter
    existing tables.  This lightweight migration keeps the school project
    usable when a student copies a newer version over an older database.
    """
    inspector = inspect(db.engine)
    dialect = db.engine.dialect

    # SQLite supports ADD COLUMN, which is enough for the additive changes in
    # this project. Other databases simply skip this lightweight migration;
    # create_all still creates missing tables there.
    if dialect.name != "sqlite":
        return

    existing_tables = set(inspector.get_table_names())
    for table in db.Model.metadata.sorted_tables:
        if table.name not in existing_tables:
            continue

        existing_columns = {col["name"] for col in inspector.get_columns(table.name)}
        for column in table.columns:
            if column.name in existing_columns:
                continue

            # Keep migrations safe for databases that already contain rows.
            # The ORM supplies Python-side defaults for new records.
            column_type = column.type.compile(dialect=dialect)
            statement = f'ALTER TABLE "{table.name}" ADD COLUMN "{column.name}" {column_type}'
            db.session.execute(text(statement))

    db.session.commit()


def _backfill_legacy_data():
    """Repair small pieces of data that older versions may not have stored."""
    # Site settings are expected by the public layout and are created by the
    # service layer, but creating one here makes the first request deterministic.
    if SiteSetting.query.first() is None:
        db.session.add(SiteSetting())

    # Existing administrator accounts from an older build may have a newly
    # added is_active column containing NULL. NULL is treated as false by the
    # login guard, so explicitly activate legacy administrators.
    for user in AdminUser.query.filter(AdminUser.is_active.is_(None)).all():
        user.is_active = True
    for user in AdminUser.query.filter((AdminUser.role.is_(None)) | (AdminUser.role == "")).all():
        user.role = "Administrator"

    # Older News records may pre-date the slug/status fields.
    for item in News.query.filter((News.slug.is_(None)) | (News.slug == "")).all():
        item.slug = unique_slug(News, item.title, item.id)
    for item in News.query.filter((News.status.is_(None)) | (News.status == "")).all():
        item.status = "published"

    db.session.commit()


def initialize_database():
    """Create the schema and safely upgrade additive changes."""
    db.create_all()
    _add_missing_columns()
    # Re-run create_all after ALTER TABLE so SQLAlchemy sees all newly-added
    # tables/metadata consistently.
    db.create_all()
    _backfill_legacy_data()
