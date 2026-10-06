from pathlib import Path

from flask import Flask
from config import Config

from .extensions import db, login_manager, csrf
from .database import initialize_database


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    @app.after_request
    def security_headers(response):
        response.headers.setdefault('X-Content-Type-Options', 'nosniff')
        response.headers.setdefault('X-Frame-Options', 'SAMEORIGIN')
        response.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
        response.headers.setdefault('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
        if not app.debug:
            response.headers.setdefault('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
        return response

    # Keep uploaded files in the project-level uploads directory.
    project_root = Path(app.root_path).parent
    app.config["UPLOAD_IMAGE_FOLDER"] = str(project_root / "uploads" / "images")
    app.config["UPLOAD_DOCUMENT_FOLDER"] = str(project_root / "uploads" / "documents")

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    Path(app.config["UPLOAD_IMAGE_FOLDER"]).mkdir(parents=True, exist_ok=True)
    Path(app.config["UPLOAD_DOCUMENT_FOLDER"]).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from .routes.public import public_bp
    from .routes.auth import auth_bp
    from .routes.admin import admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_site_settings():
        from .models import SiteSetting
        return {"site_settings": SiteSetting.query.first()}

    with app.app_context():
        initialize_database()

    return app


@login_manager.user_loader
def load_user(user_id):
    from .models import AdminUser

    try:
        return db.session.get(AdminUser, int(user_id))
    except (TypeError, ValueError):
        return None
