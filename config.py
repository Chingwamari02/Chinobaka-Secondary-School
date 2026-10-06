import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR=Path(__file__).resolve().parent
load_dotenv(BASE_DIR/'.env')
class Config:
 SECRET_KEY=os.getenv('SECRET_KEY') or 'dev-only-change-this-secret-before-deployment'
 SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL',f'sqlite:///{BASE_DIR}/instance/chinobaka.db')
 SQLALCHEMY_TRACK_MODIFICATIONS=False
 MAX_CONTENT_LENGTH=int(os.getenv('MAX_CONTENT_LENGTH',16*1024*1024))
 UPLOAD_IMAGE_EXTENSIONS={'png','jpg','jpeg','webp','gif'}
 UPLOAD_DOCUMENT_EXTENSIONS={'pdf','doc','docx','xls','xlsx','ppt','pptx'}
 DEBUG=os.getenv('FLASK_DEBUG','0')=='1'
 SESSION_COOKIE_HTTPONLY=True
 SESSION_COOKIE_SAMESITE='Lax'
 SESSION_COOKIE_SECURE=os.getenv('SESSION_COOKIE_SECURE','0')=='1'
 REMEMBER_COOKIE_HTTPONLY=True
 REMEMBER_COOKIE_SAMESITE='Lax'
 REMEMBER_COOKIE_SECURE=os.getenv('SESSION_COOKIE_SECURE','0')=='1'
 WTF_CSRF_TIME_LIMIT=3600
 SEND_FILE_MAX_AGE_DEFAULT=3600
