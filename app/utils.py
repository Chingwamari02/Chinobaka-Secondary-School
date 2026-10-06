import re,uuid
from pathlib import Path
from flask import current_app
from werkzeug.utils import secure_filename
def slugify(s): return re.sub(r'[^a-zA-Z0-9]+','-',s.lower()).strip('-') or uuid.uuid4().hex[:8]
def unique_slug(model,title,current_id=None):
 base=slugify(title); slug=base; n=2
 while True:
  q=model.query.filter_by(slug=slug)
  if current_id:q=q.filter(model.id!=current_id)
  if not q.first():return slug
  slug=f'{base}-{n}'; n+=1
def save_upload(file,kind):
 if not file or not file.filename:return None
 name=secure_filename(file.filename)
 if '.' not in name:raise ValueError('The uploaded file has no extension.')
 ext=name.rsplit('.',1)[1].lower(); allowed=current_app.config['UPLOAD_IMAGE_EXTENSIONS' if kind=='image' else 'UPLOAD_DOCUMENT_EXTENSIONS']
 if ext not in allowed:raise ValueError(f'Unsupported {kind} file type: .{ext}')
 safe=f'{uuid.uuid4().hex}_{name}'; folder=Path(current_app.config['UPLOAD_IMAGE_FOLDER' if kind=='image' else 'UPLOAD_DOCUMENT_FOLDER']); folder.mkdir(parents=True,exist_ok=True); file.save(folder/safe); return safe
