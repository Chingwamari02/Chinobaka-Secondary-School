from sqlalchemy import or_
from ..extensions import db
from ..models import SiteSetting, News, Event, GalleryItem, StaffMember, Download, BoardingFacility, Achievement, StudentHierarchyMember

class SchoolContentService:
    """Application service for reusable school-content operations."""
    @staticmethod
    def settings():
        item=SiteSetting.query.first()
        if not item:
            item=SiteSetting(); db.session.add(item); db.session.commit()
        return item

    @staticmethod
    def search(query):
        term=f"%{query.strip()}%"
        results=[]
        models=[(News,'News','title','body'),(Event,'Event','title','description'),(StaffMember,'Staff','name','position'),(GalleryItem,'Gallery','title','caption'),(Download,'Document','title','description'),(BoardingFacility,'Boarding','title','description'),(Achievement,'Achievement','title','description'),(StudentHierarchyMember,'Student Leadership','name','position')]
        for model,label,a,b in models:
            q=model.query
            if model is News: q=q.filter(News.status=='published')
            rows=q.filter(or_(getattr(model,a).ilike(term),getattr(model,b).ilike(term))).limit(20).all()
            for row in rows: results.append((label,row))
        return results

    @staticmethod
    def dashboard_counts(message_model, admission_model):
        return {
            'news':News.query.count(),'events':Event.query.count(),'gallery':GalleryItem.query.count(),
            'staff':StaffMember.query.count(),'downloads':Download.query.count(),
            'boarding':BoardingFacility.query.count(),'achievements':Achievement.query.count(),
            'leadership':StudentHierarchyMember.query.count(),
            'messages':message_model.query.filter_by(is_read=False).count(),
            'applications':admission_model.query.filter_by(status='New').count()
        }
