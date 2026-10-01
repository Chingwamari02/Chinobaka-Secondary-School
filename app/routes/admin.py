from datetime import datetime
from flask import Blueprint,render_template,request,redirect,url_for,flash
from flask_login import current_user
from ..extensions import db
from ..models import *
from ..utils import unique_slug,save_upload
admin_bp=Blueprint('admin',__name__,url_prefix='/admin')
@admin_bp.before_request
def require_admin_login():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
@admin_bp.get('/')
def dashboard():return render_template('admin/dashboard.html',counts={'news':News.query.count(),'events':Event.query.count(),'gallery':GalleryItem.query.count(),'staff':StaffMember.query.count(),'downloads':Download.query.count(),'messages':ContactMessage.query.filter_by(is_read=False).count()},messages=ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all())
def crud(model,template,newurl,fields,upload=None,required_upload=False):
 @admin_bp.route(newurl,methods=['GET','POST'])
 @admin_bp.route(newurl+'/<int:item_id>/edit',methods=['GET','POST'])
 def handler(item_id=None):
  item=model.query.get_or_404(item_id) if item_id else None
  if request.method=='POST':
   if not item:item=model()
   for f in fields:
    v=request.form.get(f,'').strip()
    if f=='event_date':
     try:v=datetime.fromisoformat(v)
     except:flash('Invalid date and time.','error');return render_template(template,item=item)
    if f=='sort_order':v=int(v or 0)
    setattr(item,f,v)
   try:
    if upload:
     up=save_upload(request.files.get(upload),'image' if upload!='document' else 'document')
     if up:setattr(item,'image_filename' if upload=='image' else 'filename',up)
     elif required_upload and not getattr(item,'image_filename' if upload=='image' else 'filename',None):raise ValueError('A file is required.')
   except ValueError as e:flash(str(e),'error');return render_template(template,item=item)
   if not item.id:db.session.add(item)
   db.session.commit();flash('Saved successfully.','success');return redirect(url_for(newurl.strip('/').replace('/','.')+'_list'))
  return render_template(template,item=item)
 return handler
# Explicit routes keep endpoint names predictable
@admin_bp.get('/news')
def news_list():return render_template('admin/news_list.html',items=News.query.order_by(News.created_at.desc()).all())
@admin_bp.route('/news/new',methods=['GET','POST'])
@admin_bp.route('/news/<int:item_id>/edit',methods=['GET','POST'])
def news_form(item_id=None):
 item=News.query.get_or_404(item_id) if item_id else None
 if request.method=='POST':
  if not item:item=News()
  item.title=request.form.get('title','').strip();item.slug=unique_slug(News,item.title,item.id);item.excerpt=request.form.get('excerpt','').strip();item.body=request.form.get('body','').strip();item.status=request.form.get('status','published')
  try:
   up=save_upload(request.files.get('image'),'image')
   if up:item.image_filename=up
  except ValueError as e:flash(str(e),'error');return render_template('admin/news_form.html',item=item)
  if not item.id:db.session.add(item)
  db.session.commit();flash('News saved.','success');return redirect(url_for('admin.news_list'))
 return render_template('admin/news_form.html',item=item)
@admin_bp.post('/news/<int:item_id>/delete')
def news_delete(item_id):db.session.delete(News.query.get_or_404(item_id));db.session.commit();flash('News deleted.','success');return redirect(url_for('admin.news_list'))
@admin_bp.get('/events')
def events_list():return render_template('admin/events_list.html',items=Event.query.order_by(Event.event_date.asc()).all())
@admin_bp.route('/events/new',methods=['GET','POST'])
@admin_bp.route('/events/<int:item_id>/edit',methods=['GET','POST'])
def events_form(item_id=None):
 item=Event.query.get_or_404(item_id) if item_id else None
 if request.method=='POST':
  if not item:item=Event()
  item.title=request.form.get('title','').strip();item.description=request.form.get('description','').strip();item.location=request.form.get('location','').strip()
  try:item.event_date=datetime.fromisoformat(request.form.get('event_date',''))
  except:flash('Invalid date and time.','error');return render_template('admin/event_form.html',item=item)
  try:
   up=save_upload(request.files.get('image'),'image')
   if up:item.image_filename=up
  except ValueError as e:flash(str(e),'error');return render_template('admin/event_form.html',item=item)
  if not item.id:db.session.add(item)
  db.session.commit();flash('Event saved.','success');return redirect(url_for('admin.events_list'))
 return render_template('admin/event_form.html',item=item)
@admin_bp.post('/events/<int:item_id>/delete')
def events_delete(item_id):db.session.delete(Event.query.get_or_404(item_id));db.session.commit();return redirect(url_for('admin.events_list'))
@admin_bp.get('/gallery')
def gallery_list():return render_template('admin/gallery_list.html',items=GalleryItem.query.order_by(GalleryItem.created_at.desc()).all())
@admin_bp.route('/gallery/new',methods=['GET','POST'])
@admin_bp.route('/gallery/<int:item_id>/edit',methods=['GET','POST'])
def gallery_form(item_id=None):
 item=GalleryItem.query.get_or_404(item_id) if item_id else None
 if request.method=='POST':
  if not item:item=GalleryItem()
  item.title=request.form.get('title','').strip();item.caption=request.form.get('caption','').strip();item.category=request.form.get('category','School').strip()
  try:
   up=save_upload(request.files.get('image'),'image')
   if up:item.image_filename=up
   if not item.image_filename:raise ValueError('An image is required.')
  except ValueError as e:flash(str(e),'error');return render_template('admin/gallery_form.html',item=item)
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
  try:
   up=save_upload(request.files.get('image'),'image')
   if up:item.image_filename=up
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
   if not item.filename:raise ValueError('A document is required.')
  except ValueError as e:flash(str(e),'error');return render_template('admin/download_form.html',item=item)
  if not item.id:db.session.add(item)
  db.session.commit();return redirect(url_for('admin.downloads_list'))
 return render_template('admin/download_form.html',item=item)
@admin_bp.post('/downloads/<int:item_id>/delete')
def download_delete(item_id):db.session.delete(Download.query.get_or_404(item_id));db.session.commit();return redirect(url_for('admin.downloads_list'))
@admin_bp.get('/messages')
def messages():return render_template('admin/messages.html',items=ContactMessage.query.order_by(ContactMessage.created_at.desc()).all())
@admin_bp.post('/messages/<int:item_id>/read')
def message_read(item_id):m=ContactMessage.query.get_or_404(item_id);m.is_read=True;db.session.commit();return redirect(url_for('admin.messages'))
@admin_bp.post('/messages/<int:item_id>/delete')
def message_delete(item_id):db.session.delete(ContactMessage.query.get_or_404(item_id));db.session.commit();return redirect(url_for('admin.messages'))
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
   if len(p)<8:flash('Password must be at least 8 characters.','error');return render_template('admin/account.html',user=u)
   u.set_password(p)
  db.session.commit();flash('Account updated.','success');return redirect(url_for('admin.account'))
 return render_template('admin/account.html',user=u)
