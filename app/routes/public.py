from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory, current_app
from ..extensions import db
from ..models import ContactMessage, News, SiteSetting
from ..services.school_service import SchoolContentService

public_bp = Blueprint("public", __name__)


class PublicController:
    """Class-based controller for all public school pages."""

    def __init__(self, service):
        self.service = service

    def home(self):
        content = self.service.home_content()
        return render_template(
            "public/home.html",
            settings=self.service.settings(),
            **content,
        )

    def simple_page(self, template):
        return render_template(template, settings=self.service.settings())

    def news(self):
        return render_template(
            "public/news.html",
            settings=self.service.settings(),
            items=News.query.filter_by(status="published")
                .order_by(News.published_at.desc()).all(),
        )

    def news_detail(self, slug):
        item = News.query.filter_by(slug=slug, status="published").first_or_404()
        return render_template(
            "public/news_detail.html", settings=self.service.settings(), item=item
        )

    def events(self):
        from ..models import Event
        return render_template(
            "public/events.html",
            settings=self.service.settings(),
            items=Event.query.order_by(Event.event_date.asc()).all(),
        )

    def gallery(self):
        from ..models import GalleryItem
        return render_template(
            "public/gallery.html",
            settings=self.service.settings(),
            items=GalleryItem.query.order_by(GalleryItem.created_at.desc()).all(),
        )

    def leadership(self):
        from ..models import StaffMember
        return render_template(
            "public/leadership.html",
            settings=self.service.settings(),
            items=StaffMember.query.order_by(StaffMember.sort_order, StaffMember.name).all(),
        )

    def downloads(self):
        from ..models import Download
        return render_template(
            "public/downloads.html",
            settings=self.service.settings(),
            items=Download.query.order_by(Download.created_at.desc()).all(),
        )

    def boarding(self):
        return render_template(
            "public/boarding.html",
            settings=self.service.settings(),
            facilities=self.service.boarding_facilities(),
        )

    def achievements(self):
        return render_template(
            "public/achievements.html",
            settings=self.service.settings(),
            achievements=self.service.achievements(),
        )

    def student_hierarchy(self):
        return render_template(
            "public/student_hierarchy.html",
            settings=self.service.settings(),
            hierarchy=self.service.student_hierarchy(),
        )

    def contact(self):
        settings = self.service.settings()
        if request.method == "POST":
            message = ContactMessage(
                name=request.form.get("name", "").strip(),
                email=request.form.get("email", "").strip(),
                phone=request.form.get("phone", "").strip(),
                subject=request.form.get("subject", "").strip(),
                message=request.form.get("message", "").strip(),
            )
            if not message.name or not message.email or not message.message:
                flash("Please complete the required fields.", "error")
            else:
                db.session.add(message)
                db.session.commit()
                flash("Your message has been received.", "success")
                return redirect(url_for("public.contact"))
        return render_template("public/contact.html", settings=settings)


controller = PublicController(SchoolContentService(db))

# Register the controller methods as Flask endpoints.
public_bp.add_url_rule("/", "home", controller.home)
public_bp.add_url_rule("/about", "about", lambda: controller.simple_page("public/about.html"))
public_bp.add_url_rule("/academics", "academics", lambda: controller.simple_page("public/academics.html"))
public_bp.add_url_rule("/admissions", "admissions", lambda: controller.simple_page("public/admissions.html"))
public_bp.add_url_rule("/student-life", "student_life", lambda: controller.simple_page("public/student_life.html"))
public_bp.add_url_rule("/news", "news", controller.news)
public_bp.add_url_rule("/news/<slug>", "news_detail", controller.news_detail)
public_bp.add_url_rule("/events", "events", controller.events)
public_bp.add_url_rule("/gallery", "gallery", controller.gallery)
public_bp.add_url_rule("/leadership", "leadership", controller.leadership)
public_bp.add_url_rule("/downloads", "downloads", controller.downloads)
public_bp.add_url_rule("/boarding", "boarding", controller.boarding)
public_bp.add_url_rule("/achievements", "achievements", controller.achievements)
public_bp.add_url_rule("/students-hierarchy", "student_hierarchy", controller.student_hierarchy)
public_bp.add_url_rule("/contact", "contact", controller.contact, methods=["GET", "POST"])


@public_bp.get("/uploads/images/<path:filename>")
def image(filename):
    return send_from_directory(current_app.config["UPLOAD_IMAGE_FOLDER"], filename)


@public_bp.get("/uploads/documents/<path:filename>")
def document(filename):
    return send_from_directory(current_app.config["UPLOAD_DOCUMENT_FOLDER"], filename)
