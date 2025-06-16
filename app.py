# ===================================================================
# 1. IMPORTS
# ===================================================================
import os
import json
import re
import logging
from flask import Flask, render_template, send_from_directory, url_for, redirect, flash, request
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

# --- Local Application Imports ---
# Job Portal
from routes.auth_routes import auth_bp
from routes.candidate_routes import candidate_bp
from routes.admin_routes import admin_bp
from routes.company_routes import company_bp
from google_auth import google_auth
from database import init_db
from auth import setup_auth
# UTMT Site
from ateam import team_members, support_pillars

# ===================================================================
# 2. INITIALIZATION AND CONFIGURATION
# ===================================================================
load_dotenv()
logging.basicConfig(level=logging.INFO)
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get("SESSION_SECRET", "a_strong_default_secret_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Cloudinary Config
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True
)

# ===================================================================
# 3. EXTENSIONS AND DATABASE SETUP
# ===================================================================
# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'google_auth.login'
setup_auth(login_manager)

# Job Portal Database
with app.app_context():
    init_db()

# ===================================================================
# 4. BLUEPRINT REGISTRATION
# ===================================================================
PORTAL_PREFIX = '/portal'
app.register_blueprint(auth_bp, url_prefix=f'{PORTAL_PREFIX}/auth')
app.register_blueprint(candidate_bp, url_prefix=f'{PORTAL_PREFIX}/candidate')
app.register_blueprint(admin_bp, url_prefix=f'{PORTAL_PREFIX}/admin')
app.register_blueprint(company_bp, url_prefix=f'{PORTAL_PREFIX}/company')
app.register_blueprint(google_auth, url_prefix=PORTAL_PREFIX)

# ===================================================================
# 5. DATA LOADING & HELPER FUNCTIONS
# ===================================================================
def load_course_data(filename):
    """Loads a JSON data file from the 'data' directory."""
    try:
        filepath = os.path.join(os.path.dirname(__file__), 'data', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Could not load or parse {filename}: {e}")
        return {"topics": [], "course_title": f"Error: {filename} Not Found"}

def extract_youtube_video_id(url):
    """Extracts the YouTube video ID from various URL formats."""
    if not url: return None
    patterns = [
        r"(?:https?://)?(?:www\.)?(?:m\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=|embed/|v/|)([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match: return match.group(1)
    return None

def find_video_details(video_id_str, data_source):
    """Finds a video, its topic, and the next/prev videos in a course."""
    if not video_id_str: return None, None, None, None

    all_videos = []
    for topic in data_source.get('topics', []):
        for video in topic.get('videos', []):
            video['topic_name'] = topic.get('name')
            all_videos.append(video)
    
    try:
        current_index = next(i for i, v in enumerate(all_videos) if str(v.get('id')) == video_id_str)
    except StopIteration:
        return None, None, None, None

    current_video = all_videos[current_index]
    current_video['youtube_id'] = extract_youtube_video_id(current_video.get('youtube_url'))
    current_topic_name = current_video.get('topic_name')
    
    prev_video = all_videos[current_index - 1] if current_index > 0 else None
    next_video = all_videos[current_index + 1] if current_index + 1 < len(all_videos) else None
    
    return current_video, current_topic_name, prev_video, next_video

# Load all course data at startup
PYTHON_DATA = load_course_data('python_learning_data.json')
ML_DATA = load_course_data('machine_learning_data.json')
DL_DATA = load_course_data('deep_learning_data.json')
ALGORITHMS_DATA = load_course_data('algorithms_data.json')
INTERVIEW_PREP_DATA = load_course_data('interview_prep_data.json')

# ===================================================================
# 6. ROUTE DEFINITIONS
# ===================================================================

# --- Main UTMT Site Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/learning-hub')
def learning_hub():
    return render_template('learning_hub.html')

@app.route('/team')
def team():
    return render_template('team.html', 
                         team_members=team_members, 
                         support_pillars=support_pillars)

# --- Dynamic Course Page Route ---
def course_route_template(data_source, endpoint_name):
    """A template function to create course routes, avoiding repeated code."""
    first_video_id = None
    if data_source.get('topics') and data_source['topics'][0].get('videos'):
        first_video_id = data_source['topics'][0]['videos'][0].get('id')
    
    video_id_to_find = request.args.get('video_id')

    # If no video_id is provided, redirect to the first video of the course
    if not video_id_to_find:
        if first_video_id is not None:
            return redirect(url_for(endpoint_name, video_id=first_video_id))
        else:
            flash(f"No content available for this course yet.", "warning")
            # Render the page with no video selected
            return render_template('course_page.html', course_data=data_source, current_video=None, current_topic_name=None, prev_video=None, next_video=None)

    current_video, current_topic_name, prev_video, next_video = find_video_details(video_id_to_find, data_source)
    
    if not current_video:
        flash(f"The requested lesson was not found. Showing the first lesson instead.", "danger")
        return redirect(url_for(endpoint_name, video_id=first_video_id))

    return render_template('course_page.html',
                           course_data=data_source,
                           current_video=current_video,
                           current_topic_name=current_topic_name,
                           prev_video=prev_video,
                           next_video=next_video)

# --- Create all the course routes using the template function ---
@app.route('/python-learning')
@app.route('/python-learning/<video_id>')
def python_learning(video_id=None):
    return course_route_template(PYTHON_DATA, 'python_learning')

@app.route('/machine-learning')
@app.route('/machine-learning/<video_id>')
def machine_learning(video_id=None):
    return course_route_template(ML_DATA, 'machine_learning')

@app.route('/deep-learning-ai')
@app.route('/deep-learning-ai/<video_id>')
def deep_learning_ai(video_id=None):
    return course_route_template(DL_DATA, 'deep_learning_ai')

@app.route('/algorithms')
@app.route('/algorithms/<video_id>')
def algorithms(video_id=None):
    return course_route_template(ALGORITHMS_DATA, 'algorithms')

@app.route('/interview-preparation')
@app.route('/interview-preparation/<video_id>')
def interview_preparation(video_id=None):
    return course_route_template(INTERVIEW_PREP_DATA, 'interview_preparation')

# --- English Learning and other static-like routes ---
@app.route('/english-learning')
def english_learning():
    return render_template('english_learning.html')

# --- Job Portal Main Route ---
@app.route(f'{PORTAL_PREFIX}/')
@app.route(f'{PORTAL_PREFIX}/index')
def job_portal_index():
    from flask_login import current_user
    if current_user.is_authenticated:
        if current_user.role == 'candidate': return redirect(url_for('candidate_routes.dashboard'))
        if current_user.role == 'admin': return redirect(url_for('admin_routes.dashboard'))
        if current_user.role == 'company': return redirect(url_for('company_routes.dashboard'))
    return render_template('job_portal/index.html')

# ===================================================================
# 7. ERROR HANDLERS
# ===================================================================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404 # It's better to have a dedicated 404 page

@app.errorhandler(500)
def server_error(e):
    logging.error(f"Server Error: {e}", exc_info=True)
    return render_template('500.html'), 500 # And a dedicated 500 page

# ===================================================================
# 8. APP RUNNER
# ===================================================================
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
