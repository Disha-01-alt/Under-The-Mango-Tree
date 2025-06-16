import os
import sys
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import Flask, render_template, send_from_directory, url_for, redirect, send_file, flash, request
import importlib.util
import logging
import json
import re
from flask_login import LoginManager, current_user
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# --- Local Application Imports ---
from routes.auth_routes import auth_bp
from routes.candidate_routes import candidate_bp
from routes.admin_routes import admin_bp
from routes.company_routes import company_bp
from google_auth import google_auth
from database import init_db
from auth import setup_auth
from ateam import team_members, support_pillars # Assuming ateam.py exists

# Configure logging
logging.basicConfig(level=logging.INFO) # Use INFO for production, DEBUG for development

# Create the Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# --- App Configuration ---
app.secret_key = os.environ.get("SESSION_SECRET", "a_very_strong_default_secret_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

# Cloudinary Configuration
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True
)
logging.info("Cloudinary configured.")

# --- Extensions and Database Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'google_auth.login'
login_manager.login_message = 'Please log in to access this page.'
setup_auth(login_manager)

with app.app_context():
    init_db()

# --- Create required directories ---
os.makedirs('static/english/images', exist_ok=True)
upload_dirs = ['uploads/cvs', 'uploads/id_cards', 'uploads/marksheets', 'uploads/temp_cvs']
for directory in upload_dirs:
    os.makedirs(directory, exist_ok=True)
logging.info("Required directories created or already exist.")

# --- Blueprint Registration ---
PORTAL_PREFIX = '/portal'
app.register_blueprint(auth_bp, url_prefix=f'{PORTAL_PREFIX}/auth')
app.register_blueprint(candidate_bp, url_prefix=f'{PORTAL_PREFIX}/candidate')
app.register_blueprint(admin_bp, url_prefix=f'{PORTAL_PREFIX}/admin')
app.register_blueprint(company_bp, url_prefix=f'{PORTAL_PREFIX}/company')
app.register_blueprint(google_auth, url_prefix=PORTAL_PREFIX)
logging.info("All blueprints registered.")

# --- Data Loading and Helper Functions ---
def load_course_data(filename):
    """A robust function to load a JSON data file from the 'data' directory."""
    try:
        filepath = os.path.join(os.path.dirname(__file__), 'data', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"CRITICAL ERROR: Could not load or parse {filename}: {e}")
        return {"topics": [], "course_title": f"Error: {filename} Not Found"}

#===================================================================
# NEW HELPER FUNCTION TO FIND VIDEO DETAILS
#===================================================================
def find_video_details(video_id_str, data_source):
    """
    Finds a video and its context (topic, prev/next videos) within a course.
    Returns: current_video, current_topic_name, prev_video, next_video
    """
    def extract_youtube_id(url):
        if not url: return None
        # This regex handles most standard, shortened, and embed URLs
        patterns = [r"(?:v=|\/|youtu\.be\/|embed\/)([a-zA-Z0-9_-]{11})"]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match: return match.group(1)
        return None

    if not video_id_str:
        return None, None, None, None

    # Create a single, flat list of all videos in the correct order to find next/prev
    all_videos_in_order = [
        video for topic in data_source.get('topics', []) 
        for video in topic.get('videos', [])
    ]
    
    # Find the numerical index of the current video in the flat list
    try:
        current_index = next(i for i, v in enumerate(all_videos_in_order) if str(v.get('id')) == video_id_str)
    except StopIteration:
        # The video_id from the URL doesn't exist in our data
        return None, None, None, None

    # Get the current video object and add the clean embeddable ID
    current_video = all_videos_in_order[current_index]
    current_video['youtube_id'] = extract_youtube_id(current_video.get('youtube_url'))
    
    # Find the topic name for the current video
    current_topic_name = None
    for topic in data_source.get('topics', []):
        if any(str(v.get('id')) == video_id_str for v in topic.get('videos', [])):
            current_topic_name = topic.get('name')
            break
            
    # Find the previous video if we're not at the beginning of the list
    prev_video = all_videos_in_order[current_index - 1] if current_index > 0 else None
    
    # Find the next video if we're not at the end of the list
    next_video = all_videos_in_order[current_index + 1] if current_index + 1 < len(all_videos_in_order) else None
    
    return current_video, current_topic_name, prev_video, next_video

# Load all course data at startup
PYTHON_DATA = load_course_data('python_learning_data.json')
ML_DATA = load_course_data('machine_learning_data.json')
DL_DATA = load_course_data('deep_learning_data.json')
ALGORITHMS_DATA = load_course_data('algorithms_data.json')
INTERVIEW_PREP_DATA = load_course_data('interview_prep_data.json')
PROJECTS_DATA = load_course_data('projects_data.json')
TEAM_DATA = load_course_data('team_data.json')
logging.info("All course and site data loaded.")

# --- Route Definitions ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/learning-hub')
def learning_hub():
    return render_template('learning_hub.html')

@app.route('/team')
def team():
    return render_template('team.html', 
                         team_members=TEAM_DATA.get('team_members', []), 
                         support_pillars=TEAM_DATA.get('support_pillars', []))

# --- Job Portal Routes ---
@app.route(PORTAL_PREFIX)
def job_portal_index():
    return redirect(url_for('job_portal_main_page'))

@app.route(f'{PORTAL_PREFIX}/index')
def job_portal_main_page():
    if current_user.is_authenticated:
        if current_user.role == 'candidate': return redirect(url_for('candidate_routes.dashboard'))
        elif current_user.role == 'admin': return redirect(url_for('admin_routes.dashboard'))
        elif current_user.role == 'company': return redirect(url_for('company_routes.dashboard'))
    return render_template('job_portal/index.html')

# --- English Learning (Static) Routes ---
@app.route('/english-learning')
def english_learning():
    return render_template('english_learning.html')

# (Your static english file routes are preserved here)
@app.route('/HinToEng.html')
def hin_to_eng(): return send_from_directory('static/english', 'HinToEng.html')
# ... all other static english routes ...

# --- Dynamic Course Routes (Updated to use the new helper) ---

@app.route('/python-learning/')
@app.route('/python-learning/<video_id>')
def python_learning(video_id=None):
    if not video_id:
        first_video_id = PYTHON_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id')
        return redirect(url_for('python_learning', video_id=first_video_id)) if first_video_id is not None else render_template('python_learning.html', course_data=PYTHON_DATA)
    
    current_video, topic_name, prev_video, next_video = find_video_details(video_id, PYTHON_DATA)
    if not current_video:
        return redirect(url_for('python_learning'))
        
    return render_template('python_learning.html', course_data=PYTHON_DATA, current_video=current_video, current_topic_name=topic_name, prev_video=prev_video, next_video=next_video)

@app.route('/machine-learning/')
@app.route('/machine-learning/<video_id>')
def machine_learning(video_id=None):
    if not video_id:
        first_video_id = ML_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id')
        return redirect(url_for('machine_learning', video_id=first_video_id)) if first_video_id is not None else render_template('machine_learning.html', course_data=ML_DATA)

    current_video, topic_name, prev_video, next_video = find_video_details(video_id, ML_DATA)
    if not current_video:
        return redirect(url_for('machine_learning'))
        
    return render_template('machine_learning.html', course_data=ML_DATA, current_video=current_video, current_topic_name=topic_name, prev_video=prev_video, next_video=next_video)

@app.route('/deep-learning-ai/')
@app.route('/deep-learning-ai/<video_id>')
def deep_learning_ai(video_id=None):
    if not video_id:
        first_video_id = DL_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id')
        return redirect(url_for('deep_learning_ai', video_id=first_video_id)) if first_video_id is not None else render_template('deep_learning_ai.html', course_data=DL_DATA)

    current_video, topic_name, prev_video, next_video = find_video_details(video_id, DL_DATA)
    if not current_video:
        return redirect(url_for('deep_learning_ai'))

    return render_template('deep_learning_ai.html', course_data=DL_DATA, current_video=current_video, current_topic_name=topic_name, prev_video=prev_video, next_video=next_video)

@app.route('/algorithms/')
@app.route('/algorithms/<video_id>')
def algorithms(video_id=None):
    if not video_id:
        first_video_id = ALGORITHMS_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id')
        return redirect(url_for('algorithms', video_id=first_video_id)) if first_video_id is not None else render_template('algorithms_course_page.html', course_data=ALGORITHMS_DATA)

    current_video, topic_name, prev_video, next_video = find_video_details(video_id, ALGORITHMS_DATA)
    if not current_video:
        return redirect(url_for('algorithms'))

    return render_template('algorithms_course_page.html', course_data=ALGORITHMS_DATA, current_video=current_video, current_topic_name=topic_name, prev_video=prev_video, next_video=next_video)

@app.route('/interview-preparation/')
@app.route('/interview-preparation/<video_id>')
def interview_preparation(video_id=None):
    if not video_id:
        first_video_id = INTERVIEW_PREP_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id')
        return redirect(url_for('interview_preparation', video_id=first_video_id)) if first_video_id is not None else render_template('interview_prep_course_page.html', course_data=INTERVIEW_PREP_DATA)
        
    current_video, topic_name, prev_video, next_video = find_video_details(video_id, INTERVIEW_PREP_DATA)
    if not current_video:
        return redirect(url_for('interview_preparation'))
        
    return render_template('interview_prep_course_page.html', course_data=INTERVIEW_PREP_DATA, current_video=current_video, current_topic_name=topic_name, prev_video=prev_video, next_video=next_video)

@app.route('/projects')
def projects():
    return render_template('projects.html', 
                         projects=PROJECTS_DATA.get('projects', []),
                         page_title=PROJECTS_DATA.get('page_title', 'Projects'),
                         hero_image=PROJECTS_DATA.get('hero_image_url', ''))

# --- Error Handlers ---
@app.errorhandler(404)
def page_not_found(e):
    # It's better to have a dedicated 404.html template
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    logging.error(f"Server Error: {e}", exc_info=True)
    # It's better to have a dedicated 500.html template
    return render_template('index.html'), 500

# --- App Runner ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
