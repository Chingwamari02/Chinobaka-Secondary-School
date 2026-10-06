from flask import Blueprint,render_template,request,redirect,url_for,flash,session
from flask_login import login_user,logout_user,current_user
from ..extensions import db
from ..models import AdminUser
auth_bp=Blueprint('auth',__name__)
@auth_bp.route('/admin/setup',methods=['GET','POST'])
def setup():
 if AdminUser.query.first():return redirect(url_for('auth.login'))
 if request.method=='POST':
  u=request.form.get('username','').strip(); p=request.form.get('password',''); c=request.form.get('confirm_password','')
  if len(u)<3:flash('Username must be at least 3 characters.','error')
  elif len(p)<12:flash('Password must be at least 12 characters.','error')
  elif p!=c:flash('Passwords do not match.','error')
  else:
   a=AdminUser(username=u);a.set_password(p);db.session.add(a);db.session.commit();flash('Administrator account created.','success');return redirect(url_for('auth.login'))
 return render_template('auth/setup.html')
@auth_bp.route('/admin/login',methods=['GET','POST'])
def login():
 if current_user.is_authenticated:return redirect(url_for('admin.dashboard'))
 if not AdminUser.query.first():return redirect(url_for('auth.setup'))
 if request.method=='POST':
  now=__import__('time').time(); window=session.get('login_window',0); attempts=session.get('login_attempts',0)
  if now-window>300: attempts=0; window=now
  if attempts>=5: flash('Too many login attempts. Please wait five minutes and try again.','error'); return render_template('auth/login.html')
  session['login_window']=window; session['login_attempts']=attempts+1
  a=AdminUser.query.filter_by(username=request.form.get('username','').strip()).first()
  if a and a.is_active and a.check_password(request.form.get('password','')):
   session['login_attempts']=0; login_user(a, remember=False); return redirect(url_for('admin.dashboard'))
  flash('Invalid username or password.','error')
 return render_template('auth/login.html')
@auth_bp.post('/admin/logout')
def logout():logout_user();return redirect(url_for('auth.login'))
