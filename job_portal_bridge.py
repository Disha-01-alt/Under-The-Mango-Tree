
import sys
import os
from flask import Flask, render_template, send_from_directory, request
from flask_login import LoginManager

# Set up environment for job portal to run independently
sys.path.insert(0, os.path.abspath('jobportal'))
os.environ['PYTHONPATH'] = os.path.abspath('jobportal')

# Import the job portal app and required modules
from jobportal.app import app as job_portal_app
from jobportal.routes.candidate_routes import candidate_bp
from jobportal.routes.admin_routes import admin_bp
from jobportal.routes.company_routes import company_bp
from jobportal.routes.auth_routes import auth_bp
from jobportal.database import init_db
from jobportal.auth import setup_auth

# Configure upload directories
upload_dirs = ['uploads/cvs', 'uploads/id_cards', 'uploads/marksheets']
for directory in upload_dirs:
    os.makedirs(directory, exist_ok=True)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(job_portal_app)
login_manager.login_view = 'jp_auth.login'

# Register blueprints with unique names and proper URL prefixes
job_portal_app.register_blueprint(auth_bp, url_prefix='/auth', name='jp_auth')
job_portal_app.register_blueprint(candidate_bp, url_prefix='/candidate', name='jp_candidate')
job_portal_app.register_blueprint(admin_bp, url_prefix='/admin', name='jp_admin')
job_portal_app.register_blueprint(company_bp, url_prefix='/company', name='jp_company')

# Initialize database
with job_portal_app.app_context():
    init_db()

# Setup authentication
setup_auth(login_manager)

# Make the app available for import
app = job_portal_app
