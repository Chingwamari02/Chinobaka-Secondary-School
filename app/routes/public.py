from datetime import date, datetime
import calendar
from flask import Blueprint,render_template,request,redirect,url_for,flash,send_from_directory,current_app
from ..extensions import db
from ..models import *
from ..services.school_service import SchoolContentService

public_bp=Blueprint('public',__name__)
def settings(): return SchoolContentService.settings()

@public_bp.get('/')
def home():
    return render_template('public/home.html',settings=settings(),news=News.query.filter_by(status='published').order_by(News.published_at.desc()).limit(3).all(),events=Event.query.order_by(Event.event_date.asc()).limit(3).all(),gallery=GalleryItem.query.order_by(GalleryItem.created_at.desc()).limit(6).all(),achievements=Achievement.query.order_by(Achievement.created_at.desc()).limit(3).all())
@public_bp.get('/about')
def about(): return render_template('public/about.html',settings=settings())
@public_bp.get('/academics')
def academics(): return render_template('public/academics.html',settings=settings())
@public_bp.route('/admissions',methods=['GET','POST'])
def admissions():
    s=settings()
    if request.method=='POST':
        required=['applicant_name','guardian_name','email','phone','grade']
        if any(not request.form.get(x,'').strip() for x in required):
            flash('Please complete all required admission fields.','error')
        else:
            app=AdmissionApplication(applicant_name=request.form['applicant_name'].strip(),guardian_name=request.form['guardian_name'].strip(),email=request.form['email'].strip(),phone=request.form['phone'].strip(),grade=request.form['grade'].strip(),gender=request.form.get('gender','').strip(),previous_school=request.form.get('previous_school','').strip(),message=request.form.get('message','').strip(),boarding=request.form.get('boarding')=='yes')
            dob=request.form.get('date_of_birth','').strip()
            if dob:
                try: app.date_of_birth=datetime.strptime(dob,'%Y-%m-%d').date()
                except ValueError: flash('Please provide a valid date of birth.','error'); return render_template('public/admissions.html',settings=s)
            db.session.add(app); db.session.commit(); flash('Your admission enquiry/application has been received. The school can now review it from the administration dashboard.','success'); return redirect(url_for('public.admissions'))
    return render_template('public/admissions.html',settings=s)
@public_bp.get('/student-life')
def student_life(): return render_template('public/student_life.html',settings=settings())
@public_bp.get('/boarding')
def boarding(): return render_template('public/boarding.html',settings=settings(),items=BoardingFacility.query.order_by(BoardingFacility.sort_order,BoardingFacility.title).all())
@public_bp.get('/achievements')
def achievements(): return render_template('public/achievements.html',settings=settings(),items=Achievement.query.order_by(Achievement.achievement_date.desc().nullslast(),Achievement.created_at.desc()).all())
@public_bp.get('/students-hierarchy')
def students_hierarchy(): return render_template('public/student_hierarchy.html',settings=settings(),items=StudentHierarchyMember.query.order_by(StudentHierarchyMember.sort_order,StudentHierarchyMember.name).all())
@public_bp.get('/news')
def news(): return render_template('public/news.html',settings=settings(),items=News.query.filter_by(status='published').order_by(News.published_at.desc()).all())
@public_bp.get('/news/<slug>')
def news_detail(slug): return render_template('public/news_detail.html',settings=settings(),item=News.query.filter_by(slug=slug,status='published').first_or_404())
@public_bp.get('/events')
def events():
    now=datetime.utcnow()
    items=Event.query.order_by(Event.event_date.asc()).all()
    calendar_rows=calendar.monthcalendar(now.year,now.month)
    event_days={}
    for item in items:
        if item.event_date.year==now.year and item.event_date.month==now.month:
            event_days.setdefault(item.event_date.day,[]).append(item)
    return render_template('public/events.html',settings=settings(),items=items,calendar_rows=calendar_rows,calendar_year=now.year,calendar_month=now.month,month_name=calendar.month_name[now.month],event_days=event_days)
@public_bp.get('/gallery')
def gallery(): return render_template('public/gallery.html',settings=settings(),items=GalleryItem.query.order_by(GalleryItem.created_at.desc()).all())
@public_bp.get('/leadership')
def leadership(): return render_template('public/leadership.html',settings=settings(),items=StaffMember.query.order_by(StaffMember.sort_order,StaffMember.name).all())
@public_bp.get('/downloads')
def downloads(): return render_template('public/downloads.html',settings=settings(),items=Download.query.order_by(Download.created_at.desc()).all())
@public_bp.get('/search')
def search():
    q=request.args.get('q','').strip()
    results=SchoolContentService.search(q) if len(q)>=2 else []
    return render_template('public/search.html',settings=settings(),q=q,results=results)
@public_bp.route('/contact',methods=['GET','POST'])
def contact():
    s=settings()
    if request.method=='POST':
        m=ContactMessage(name=request.form.get('name','').strip(),email=request.form.get('email','').strip(),phone=request.form.get('phone','').strip(),subject=request.form.get('subject','').strip(),message=request.form.get('message','').strip())
        if not m.name or not m.email or not m.message: flash('Please complete the required fields.','error')
        else: db.session.add(m); db.session.commit(); flash('Your message has been received.','success'); return redirect(url_for('public.contact'))
    return render_template('public/contact.html',settings=s)
@public_bp.get('/uploads/images/<path:filename>')
def image(filename): return send_from_directory(current_app.config['UPLOAD_IMAGE_FOLDER'],filename)
@public_bp.get('/uploads/documents/<path:filename>')
def document(filename): return send_from_directory(current_app.config['UPLOAD_DOCUMENT_FOLDER'],filename,as_attachment=True)
