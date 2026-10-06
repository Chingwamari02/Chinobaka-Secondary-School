from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from .extensions import db
class AdminUser(UserMixin,db.Model):
 id=db.Column(db.Integer,primary_key=True); username=db.Column(db.String(80),unique=True,nullable=False); password_hash=db.Column(db.String(255),nullable=False); role=db.Column(db.String(30),default='Administrator'); is_active=db.Column(db.Boolean,default=True); created_at=db.Column(db.DateTime,default=datetime.utcnow)
 def set_password(self,p): self.password_hash=generate_password_hash(p)
 def check_password(self,p): return check_password_hash(self.password_hash,p)
class SiteSetting(db.Model):
 id=db.Column(db.Integer,primary_key=True); school_name=db.Column(db.String(160),default='Chinobaka Secondary School',nullable=False); motto=db.Column(db.String(255),default='To be confirmed',nullable=False); phone=db.Column(db.String(80),default='To be confirmed'); email=db.Column(db.String(160),default='To be confirmed'); address=db.Column(db.String(255),default='To be confirmed'); about_text=db.Column(db.Text,default='Official school information will be published here after confirmation.'); hero_title=db.Column(db.String(255),default='Empowering learners. Building futures.'); hero_text=db.Column(db.Text,default='A welcoming secondary school community focused on learning, character and opportunity.'); logo_filename=db.Column(db.String(255)); hero_image_filename=db.Column(db.String(255)); updated_at=db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
class News(db.Model):
 id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(200),nullable=False); slug=db.Column(db.String(220),unique=True,nullable=False); excerpt=db.Column(db.Text); body=db.Column(db.Text,nullable=False); status=db.Column(db.String(20),default='published'); image_filename=db.Column(db.String(255)); published_at=db.Column(db.DateTime,default=datetime.utcnow); created_at=db.Column(db.DateTime,default=datetime.utcnow)
class Event(db.Model):
 id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(200),nullable=False); description=db.Column(db.Text); event_date=db.Column(db.DateTime,nullable=False); location=db.Column(db.String(200)); image_filename=db.Column(db.String(255)); created_at=db.Column(db.DateTime,default=datetime.utcnow)
class GalleryItem(db.Model):
 id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(200),nullable=False); caption=db.Column(db.Text); image_filename=db.Column(db.String(255),nullable=False); category=db.Column(db.String(80),default='School'); created_at=db.Column(db.DateTime,default=datetime.utcnow)
class StaffMember(db.Model):
 id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(160),nullable=False); position=db.Column(db.String(160),nullable=False); bio=db.Column(db.Text); image_filename=db.Column(db.String(255)); sort_order=db.Column(db.Integer,default=0); created_at=db.Column(db.DateTime,default=datetime.utcnow)
class Download(db.Model):
 id=db.Column(db.Integer,primary_key=True); title=db.Column(db.String(200),nullable=False); description=db.Column(db.Text); filename=db.Column(db.String(255),nullable=False); category=db.Column(db.String(100),default='General'); created_at=db.Column(db.DateTime,default=datetime.utcnow)
class ContactMessage(db.Model):
 id=db.Column(db.Integer,primary_key=True); name=db.Column(db.String(160),nullable=False); email=db.Column(db.String(160),nullable=False); phone=db.Column(db.String(80)); subject=db.Column(db.String(200)); message=db.Column(db.Text,nullable=False); is_read=db.Column(db.Boolean,default=False); created_at=db.Column(db.DateTime,default=datetime.utcnow)

class BoardingFacility(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    description=db.Column(db.Text,nullable=False)
    image_filename=db.Column(db.String(255))
    sort_order=db.Column(db.Integer,default=0)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

class Achievement(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    description=db.Column(db.Text,nullable=False)
    category=db.Column(db.String(100),default='General')
    achievement_date=db.Column(db.DateTime)
    image_filename=db.Column(db.String(255))
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

class StudentHierarchyMember(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(160),nullable=False)
    position=db.Column(db.String(160),nullable=False)
    description=db.Column(db.Text)
    image_filename=db.Column(db.String(255))
    level=db.Column(db.String(80),default='Student Leadership')
    sort_order=db.Column(db.Integer,default=0)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

class AdmissionApplication(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    applicant_name=db.Column(db.String(160),nullable=False)
    date_of_birth=db.Column(db.Date)
    gender=db.Column(db.String(40))
    guardian_name=db.Column(db.String(160),nullable=False)
    email=db.Column(db.String(160),nullable=False)
    phone=db.Column(db.String(80),nullable=False)
    grade=db.Column(db.String(80),nullable=False)
    boarding=db.Column(db.Boolean,default=False)
    previous_school=db.Column(db.String(200))
    message=db.Column(db.Text)
    status=db.Column(db.String(40),default='New')
    created_at=db.Column(db.DateTime,default=datetime.utcnow)
