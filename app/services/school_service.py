from ..models import (
    SiteSetting, News, Event, GalleryItem, BoardingFacility,
    Achievement, StudentHierarchyMember
)


class SchoolContentService:
    """Application service responsible for assembling public school content."""

    def __init__(self, db):
        self.db = db

    def settings(self):
        school = SiteSetting.query.first()
        if school is None:
            school = SiteSetting()
            self.db.session.add(school)
            self.db.session.commit()
        return school

    def home_content(self):
        return {
            "news": News.query.filter_by(status="published")
                .order_by(News.published_at.desc()).limit(3).all(),
            "events": Event.query.order_by(Event.event_date.asc()).limit(3).all(),
            "gallery": GalleryItem.query.order_by(
                GalleryItem.created_at.desc()
            ).limit(6).all(),
            "achievements": Achievement.query.order_by(
                Achievement.sort_order, Achievement.year.desc()
            ).limit(3).all(),
        }

    def boarding_facilities(self):
        return BoardingFacility.query.order_by(
            BoardingFacility.sort_order, BoardingFacility.name
        ).all()

    def achievements(self):
        return Achievement.query.order_by(
            Achievement.sort_order, Achievement.year.desc(), Achievement.title
        ).all()

    def student_hierarchy(self):
        return StudentHierarchyMember.query.order_by(
            StudentHierarchyMember.sort_order
        ).all()
