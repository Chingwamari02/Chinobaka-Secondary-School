from datetime import datetime
from flask import Blueprint,render_template,request,redirect,url_for,flash,abort
from flask_login import current_user
from ..extensions import db
from ..models import *
from ..utils import unique_slug,save_upload
from ..services.school_service import SchoolContentService

admin_bp=Blueprint('admin',__name__,url_prefix='/admin')
@admin_bp.before_request
def require_admin_login():
    if not current_user.is_authenticated: return redirect(url_for('auth.login'))

@admin_bp.get('/')
def dashboard():
    return render_template('admin/dashboard.html',counts=SchoolContentService.dashboard_counts(ContactMessage,AdmissionApplication),messages=ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all(),applications=AdmissionApplication.query.order_by(AdmissionApplication.created_at.desc()).limit(5).all())

# News
@admin_bp.get('/news')
def news_list(): return render_template('admin/news_list.html',items=News.query.order_by(News.created_at.desc()).all())
@admin_bp.route('/news/new',methods=['GET','POST'])
@admin_bp.route('/news/<int:item_id>/edit',methods=['GET','POST'])
def news_form(item_id=None):
    item=News.query.get_or_404(item_id) if item_id else None
    if request.method=='POST':
        if not item: item=News()
        item.title=request.form.get('title','').strip(); item.slug=unique_slug(News,item.title,item.id); item.excerpt=request.form.get('excerpt','').strip(); item.body=request.form.get('body','').strip(); item.status=request.form.get('status','published')
        try:
            up=save_upload(request.files.get('image'),'image')
            if up: item.image_filename=up
        except ValueError as e: flash(str(e),'error'); return render_template('admin/news_form.html',item=item)
        if not item.id: db.session.add(item)
        db.session.commit(); flash('News saved.','success'); return redirect(url_for('admin.news_list'))
    return render_template('admin/news_form.html',item=item)
@admin_bp.post('/news/<int:item_id>/delete')
def news_delete(item_id): db.session.delete(News.query.get_or_404(item_id)); db.session.commit(); return redirect(url_for('admin.news_list'))

# Generic simple content manager helpers
def save_image_from_form(item):
    up=save_upload(request.files.get('image'),'image')
    if up: item.image_filename=up

@admin_bp.get('/events')
def events_list(): return render_template('admin/events_list.html',items=Event.query.order_by(Event.event_date.asc()).all())
@admin_bp.route('/events/new',methods=['GET','POST'])
@admin_bp.route('/events/<int:item_id>/edit',methods=['GET','POST'])
def events_form(item_id=None):
    item=Event.query.get_or_404(item_id) if item_id else None
    if request.method=='POST':
        if not item:item=Event()
        item.title=request.form.get('title','').strip();item.description=request.form.get('description','').strip();item.location=request.form.get('location','').strip()
        try:item.event_date=datetime.fromisoformat(request.form.get('event_date',''))
        except ValueError: flash('Invalid date and time.','error'); return render_template('admin/event_form.html',item=item)
        try: save_image_from_form(item)
        except ValueError as e: flash(str(e),'error'); return render_template('admin/event_form.html',item=item)
        if not item.id:db.session.add(item)
        db.session.commit();return redirect(url_for('admin.events_list'))
    return render_template('admin/event_form.html',item=item)
@admin_bp.post('/events/<int:item_id>/delete')
def events_delete(item_id): db.session.delete(Event.query.get_or_404(item_id));db.session.commit();return redirect(url_for('admin.events_list'))

@admin_bp.get('/gallery')
def gallery_list(): return render_template('admin/gallery_list.html',items=GalleryItem.query.order_by(GalleryItem.created_at.desc()).all())
@admin_bp.route('/gallery/new',methods=['GET','POST'])
@admin_bp.route('/gallery/<int:item_id>/edit',methods=['GET','POST'])
def gallery_form(item_id=None):
    item=GalleryItem.query.get_or_404(item_id) if item_id else None
    if request.method=='POST':
        if not item:item=GalleryItem()
        item.title=request.form.get('title','').strip();item.caption=request.form.get('caption','').strip();item.category=request.form.get('category','School').strip()
        try:save_image_from_form(item)
        except ValueError as e:flash(str(e),'error');return render_template('admin/gallery_form.html',item=item)
        if not item.image_filename:flash('An image is required.','error');return render_template('admin/gallery_form.html',item=item)
        if not item.id:db.session.add(item)
        db.session.commit();return redirect(url_for('admin.gallery_list'))
    return render_template('admin/gallery_form.html',item=item)
@admin_bp.post('/gallery/<int:item_id>/delete')
def gallery_delete(item_id):db.session.delete(GalleryItem.query.get_or_404(item_id));db.session.commit();return redirect(url_for('admin.gallery_list'))

@admin_bp.get('/staff')
def staff_list():return render_template('admin/staff_list.html',items=StaffMember.query.order_by(StaffMember.sort_order,StaffMember.name).all())
@admin_bp.route('/staff/new',methods=['GET','POST'])
@admin_bp.route('/staff/<int:item_id>/edit',methods=['GET','POST'])
def staff_form(item_id=None):
    item=StaffMember.query.get_or_404(item_id) if item_id else None
    if request.method=='POST':
        if not item:item=StaffMember()
        item.name=request.form.get('name','').strip();item.position=request.form.get('position','').strip();item.bio=request.form.get('bio','').strip();item.sort_order=int(request.form.get('sort_order') or 0)
        try:save_image_from_form(item)
        except ValueError as e:flash(str(e),'error');return render_template('admin/staff_form.html',item=item)
        if not item.id:db.session.add(item)
        db.session.commit();return redirect(url_for('admin.staff_list'))
    return render_template('admin/staff_form.html',item=item)
@admin_bp.post('/staff/<int:item_id>/delete')
def staff_delete(item_id):db.session.delete(StaffMember.query.get_or_404(item_id));db.session.commit();return redirect(url_for('admin.staff_list'))

@admin_bp.get('/downloads')
def downloads_list():return render_template('admin/downloads_list.html',items=Download.query.order_by(Download.created_at.desc()).all())
@admin_bp.route('/downloads/new',methods=['GET','POST'])
@admin_bp.route('/downloads/<int:item_id>/edit',methods=['GET','POST'])
def download_form(item_id=None):
    item=Download.query.get_or_404(item_id) if item_id else None
    if request.method=='POST':
        if not item:item=Download()
        item.title=request.form.get('title','').strip();item.description=request.form.get('description','').strip();item.category=request.form.get('category','General').strip()
        try:
            up=save_upload(request.files.get('document'),'document')
            if up:item.filename=up
        except ValueError as e:flash(str(e),'error');return render_template('admin/download_form.html',item=item)
        if not item.filename:flash('A document is required.','error');return render_template('admin/download_form.html',item=item)
        if not item.id:db.session.add(item)
        db.session.commit();return redirect(url_for('admin.downloads_list'))
    return render_template('admin/download_form.html',item=item)
@admin_bp.post('/downloads/<int:item_id>/delete')
def download_delete(item_id):db.session.delete(Download.query.get_or_404(item_id));db.session.commit();return redirect(url_for('admin.downloads_list'))

# Messages and applications
@admin_bp.get('/messages')
def messages():return render_template('admin/messages.html',items=ContactMessage.query.order_by(ContactMessage.created_at.desc()).all())
@admin_bp.post('/messages/<int:item_id>/read')
def message_read(item_id):m=ContactMessage.query.get_or_404(item_id);m.is_read=True;db.session.commit();return redirect(url_for('admin.messages'))
@admin_bp.post('/messages/<int:item_id>/delete')
def message_delete(item_id):db.session.delete(ContactMessage.query.get_or_404(item_id));db.session.commit();return redirect(url_for('admin.messages'))
@admin_bp.get('/applications')
def applications():return render_template('admin/applications.html',items=AdmissionApplication.query.order_by(AdmissionApplication.created_at.desc()).all())
@admin_bp.post('/applications/<int:item_id>/status')
def application_status(item_id):
    item=AdmissionApplication.query.get_or_404(item_id); item.status=request.form.get('status','New'); db.session.commit(); flash('Application status updated.','success'); return redirect(url_for('admin.applications'))
@admin_bp.post('/applications/<int:item_id>/delete')
def application_delete(item_id):db.session.delete(AdmissionApplication.query.get_or_404(item_id));db.session.commit();return redirect(url_for('admin.applications'))

# Boarding, achievements and student hierarchy
def simple_content_routes(model,list_template,form_template,list_endpoint,fields,upload=True,order_field=None):
    slug=list_endpoint.replace('_list','')
    @admin_bp.get('/'+slug, endpoint=list_endpoint)
    def listing(model=model,list_template=list_template,order_field=order_field):
        query=model.query
        if order_field:
            query=query.order_by(getattr(model,order_field), getattr(model,'title',getattr(model,'name',model.created_at)))
        else:
            query=query.order_by(model.created_at.desc())
        return render_template(list_template,items=query.all())
    @admin_bp.route('/'+slug+'/new',methods=['GET','POST'], endpoint=list_endpoint+'_form_new')
    @admin_bp.route('/'+slug+'/<int:item_id>/edit',methods=['GET','POST'], endpoint=list_endpoint+'_form_edit')
    def form(item_id=None,model=model,form_template=form_template,fields=fields):
        item=model.query.get_or_404(item_id) if item_id else None
        if request.method=='POST':
            if not item:item=model()
            for f in fields:
                value=request.form.get(f,'').strip()
                if f=='sort_order': value=int(value or 0)
                setattr(item,f,value)
            try:
                if upload:save_image_from_form(item)
            except ValueError as e:flash(str(e),'error');return render_template(form_template,item=item)
            if not item.id:db.session.add(item)
            db.session.commit();flash('Saved successfully.','success');return redirect(url_for(list_endpoint))
        return render_template(form_template,item=item)
    @admin_bp.post('/'+slug+'/<int:item_id>/delete', endpoint=list_endpoint+'_delete')
    def delete(item_id,model=model,list_endpoint=list_endpoint):
        db.session.delete(model.query.get_or_404(item_id));db.session.commit();return redirect(url_for(list_endpoint))

simple_content_routes(BoardingFacility,'admin/boarding_list.html','admin/boarding_form.html','boarding_list',['title','description','sort_order'])
simple_content_routes(Achievement,'admin/achievements_list.html','admin/achievement_form.html','achievements_list',['title','description','category'],upload=True)
simple_content_routes(StudentHierarchyMember,'admin/hierarchy_list.html','admin/hierarchy_form.html','hierarchy_list',['name','position','description','level','sort_order'])

@admin_bp.route('/settings',methods=['GET','POST'])
def settings():
    s=SiteSetting.query.first() or SiteSetting()
    if request.method=='POST':
        for f in ['school_name','motto','phone','email','address','about_text','hero_title','hero_text']:setattr(s,f,request.form.get(f,'').strip())
        try:
            logo=save_upload(request.files.get('logo'),'image');hero=save_upload(request.files.get('hero_image'),'image')
            if logo:s.logo_filename=logo
            if hero:s.hero_image_filename=hero
        except ValueError as e:flash(str(e),'error');return render_template('admin/settings.html',item=s)
        if not s.id:db.session.add(s)
        db.session.commit();flash('School settings updated.','success');return redirect(url_for('admin.settings'))
    return render_template('admin/settings.html',item=s)
@admin_bp.route('/account',methods=['GET','POST'])
def account():
    u=AdminUser.query.first()
    if request.method=='POST':
        u.username=request.form.get('username','').strip();p=request.form.get('password','')
        if p:
            if len(p)<12:flash('For stronger security, password must be at least 12 characters.','error');return render_template('admin/account.html',user=u)
            u.set_password(p)
        db.session.commit();flash('Account updated.','success');return redirect(url_for('admin.account'))
    return render_template('admin/account.html',user=u)
