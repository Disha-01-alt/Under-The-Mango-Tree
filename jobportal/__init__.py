from flask import Blueprint
from .routes.auth_routes import auth_bp
from .routes.candidate_routes import candidate_bp
from .routes.admin_routes import admin_bp
from .routes.company_routes import company_bp
from .auth import setup_auth
from .database import init_db
from .google_auth import setup_google_auth  # If you use OAuth

def create_job_portal(login_manager, app=None):
    job_portal = Blueprint(
        'job_portal', __name__,
        template_folder='templates',
        static_folder='static',
        static_url_path='/jobportal/static'
    )

    # Register blueprints
    job_portal.register_blueprint(auth_bp, url_prefix='/auth')
    job_portal.register_blueprint(candidate_bp, url_prefix='/candidate')
    job_portal.register_blueprint(admin_bp, url_prefix='/admin')
    job_portal.register_blueprint(company_bp, url_prefix='/company')

    # Auth & Google Login
    setup_auth(login_manager)
    if app:
        setup_google_auth(app)

    return job_portal
