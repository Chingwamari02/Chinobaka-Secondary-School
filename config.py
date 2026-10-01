import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR=Path(__file__).resolve().parent
load_dotenv(BASE_DIR/'.env')
class Config:
 SECRET_KEY=os.getenv('SECRET_KEY','dev-change-me')
 SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL',f'sqlite:///{BASE_DIR}/instance/chinobaka.db')
 SQLALCHEMY_TRACK_MODIFICATIONS=False
 MAX_CONTENT_LENGTH=int(os.getenv('MAX_CONTENT_LENGTH',16*1024*1024))
 UPLOAD_IMAGE_EXTENSIONS={'png','jpg','jpeg','webp','gif'}
 UPLOAD_DOCUMENT_EXTENSIONS={'pdf','doc','docx','xls','xlsx','ppt','pptx'}
 DEBUG=os.getenv('FLASK_DEBUG','1')=='1'
