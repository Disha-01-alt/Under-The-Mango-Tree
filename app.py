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
# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# --- App Configuration ---
app.secret_key = os.environ.get("SESSION_SECRET", "utmt_default_secret_key")
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
        # Construct the full path to the file
        filepath = os.path.join(os.path.dirname(__file__), 'data', filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL ERROR: Could not load or parse {filename}: {e}")
        # Return a safe, empty structure so the app can still run
        return {"topics": [], "course_title": f"Error: {filename} Not Found"}

PYTHON_DATA = load_course_data('python_learning_data.json')
ML_DATA = load_course_data('machine_learning_data.json')
DL_DATA = load_course_data('deep_learning_data.json')
ALGORITHMS_DATA = load_course_data('algorithms_data.json')
INTERVIEW_PREP_DATA = load_course_data('interview_prep_data.json')
PROJECTS_DATA = load_course_data('projects_data.json')
TEAM_DATA = load_course_data('team_data.json')

def extract_youtube_video_id(url):
    """
    Extracts the YouTube video ID from various YouTube URL formats.
    Handles watch?v=, youtu.be/, and embed/ URLs.
    """
    if not url:
        return None
    # This regex is robust for most common YouTube URL formats
    patterns = [
        # Standard watch URLs (www.youtube.com/watch?v=VIDEO_ID)
        r"(?:https?://)?(?:www\.)?(?:m\.)?(?:youtube\.com)/(?:watch\?v=|embed/|v/|)([a-zA-Z0-9_-]{11})(?:\S+)?",
        # Shortened youtu.be URLs (youtu.be/VIDEO_ID)
        r"(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]{11})(?:\S+)?"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1) # Group 1 is the 11-character video ID
    return None # No video ID found

def find_video_by_id(video_id, data_source):
    """
    Helper function to find a specific video and its topic from any course data.
    Adds a 'youtube_id' field to the video dictionary for easy template use.
    """
    if not video_id:
        return None, None
    for topic in data_source.get('topics', []):
        for video in topic.get('videos', []):
            if str(video.get('id')) == str(video_id):
                # Add the extracted YouTube ID to the video dictionary
                video['youtube_id'] = extract_youtube_video_id(video.get('youtube_url'))
                return video, topic.get('name')  # Return the video object and its topic name
    return None, None  # Return None if not found

# --- Route Definitions ---

# --- Main Site Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/learning-hub')
def learning_hub():
    return render_template('learning_hub.html')

@app.route('/team')
def team():
    team_members_data = TEAM_DATA.get('team_members', [])
    support_pillars_data = TEAM_DATA.get('support_pillars', [])
    return render_template('team.html', 
                           team_members=team_members_data, 
                           support_pillars=support_pillars_data)

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

@app.route('/HinToEng.html')
def hin_to_eng(): return send_from_directory('static/english', 'HinToEng.html')
@app.route('/PicToEng.html')
def pic_to_eng(): return send_from_directory('static/english', 'PicToEng.html')
@app.route('/SentCorrect.html')
def sent_correct(): return send_from_directory('static/english', 'SentCorrect.html')
@app.route('/QnA.html')
def qna(): return send_from_directory('static/english', 'QnA.html')
@app.route('/guessWord.html')
def guess_word(): return send_from_directory('static/english', 'guessWord.html')
@app.route('/PrepositionGame.html')
def preposition_game(): return send_from_directory('static/english', 'PrepositionGame.html')
@app.route('/Synonyms.html')
def synonyms(): return send_from_directory('static/english', 'Synonyms.html')
@app.route('/odd_one_out.html')
def odd_one_out(): return send_from_directory('static/english', 'odd_one_out.html')

@app.route('/HinToEng.json')
def hin_to_eng_json(): return send_from_directory('static/english', 'HinToEng.json')
@app.route('/PicToEng.json')
def pic_to_eng_json(): return send_from_directory('static/english', 'PicToEng.json')
@app.route('/SentCorrect.json')
def sent_correct_json(): return send_from_directory('static/english', 'SentCorrect.json')
@app.route('/QnA.json')
def qna_json(): return send_from_directory('static/english', 'QnA.json')
@app.route('/guessWord.json')
def guess_word_json(): return send_from_directory('static/english', 'guessWord.json')
@app.route('/Prepositions.json')
def prepositions_json(): return send_from_directory('static/english', 'Prepositions.json')
@app.route('/Synonym.json')
def synonym_json(): return send_from_directory('static/english', 'Synonym.json')
@app.route('/odd_one_out.json')
def odd_one_out_json(): return send_from_directory('static/english', 'odd_one_out.json')

# --- Dynamic Course Routes ---

@app.route('/python-learning')
@app.route('/python-learning/<video_id>')
def python_learning(video_id=None):
    if not video_id:
        first_video_id = PYTHON_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id')
        if first_video_id is not None:
            return redirect(url_for('python_learning', video_id=first_video_id))
        else:
            flash("No Python learning content is available.", "warning")
            return render_template('python_learning.html', course_data=PYTHON_DATA, current_video=None, current_topic_name=None)

    current_video, current_topic_name = find_video_by_id(video_id, PYTHON_DATA)
    if not current_video:
        first_video_id = PYTHON_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id')
        flash(f"The requested video (ID: {video_id}) could not be found.", "danger")
        return redirect(url_for('python_learning', video_id=first_video_id))
    
    return render_template('python_learning.html', course_data=PYTHON_DATA, current_video=current_video, current_topic_name=current_topic_name)

@app.route('/machine-learning')
@app.route('/machine-learning/<video_id>')
def machine_learning(video_id=None):
    if not video_id:
        first_video_id = ML_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id')
        if first_video_id is not None:
            return redirect(url_for('machine_learning', video_id=first_video_id))
        else:
            flash("No Machine Learning content is available.", "warning")
            return render_template('machine_learning.html', course_data=ML_DATA, current_video=None, current_topic_name=None)
            
    current_video, current_topic_name = find_video_by_id(video_id, ML_DATA)
    if not current_video:
        first_video_id = ML_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id')
        flash(f"Video with ID '{video_id}' not found.", "danger")
        return redirect(url_for('machine_learning', video_id=first_video_id))

    return render_template('machine_learning.html', course_data=ML_DATA, current_video=current_video, current_topic_name=current_topic_name)

@app.route('/deep-learning-ai')
@app.route('/deep-learning-ai/<video_id>')
def deep_learning_ai(video_id=None):
    if not video_id:
        first_video_id = DL_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id')
        if first_video_id is not None:
            return redirect(url_for('deep_learning_ai', video_id=first_video_id))
        else:
            flash("No Deep Learning content is available.", "warning")
            return render_template('deep_learning_ai.html', course_data=DL_DATA, current_video=None, current_topic_name=None)

    current_video, current_topic_name = find_video_by_id(video_id, DL_DATA)
    if not current_video:
        first_video_id = DL_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id')
        flash(f"Video with ID '{video_id}' not found.", "danger")
        return redirect(url_for('deep_learning_ai', video_id=first_video_id))

    return render_template('deep_learning_ai.html', course_data=DL_DATA, current_video=current_video, current_topic_name=current_topic_name)

@app.route('/algorithms')
@app.route('/algorithms/<video_id>')
def algorithms(video_id=None):
    if not video_id:
        first_video_id = ALGORITHMS_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id')
        if first_video_id is not None:
            return redirect(url_for('algorithms', video_id=first_video_id))
        else:
            flash("No Algorithms content is available.", "warning")
            return render_template('algorithms_course_page.html', course_data=ALGORITHMS_DATA, current_video=None, current_topic_name=None)

    current_video, current_topic_name = find_video_by_id(video_id, ALGORITHMS_DATA)
    if not current_video:
        first_video_id = ALGORITHMS_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id')
        flash(f"Video with ID '{video_id}' not found.", "danger")
        return redirect(url_for('algorithms', video_id=first_video_id))

    return render_template('algorithms_course_page.html', course_data=ALGORITHMS_DATA, current_video=current_video, current_topic_name=current_topic_name)

@app.route('/interview-preparation')
@app.route('/interview-preparation/<video_id>')
def interview_preparation(video_id=None):
    if not video_id:
        first_video_id = INTERVIEW_PREP_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id')
        if first_video_id is not None:
            return redirect(url_for('interview_preparation', video_id=first_video_id))
        else:
            flash("No Interview Prep content is available.", "warning")
            return render_template('interview_prep_course_page.html', course_data=INTERVIEW_PREP_DATA, current_video=None, current_topic_name=None)

    current_video, current_topic_name = find_video_by_id(video_id, INTERVIEW_PREP_DATA)
    if not current_video:
        first_video_id = INTERVIEW_PREP_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id')
        flash(f"Video with ID '{video_id}' not found.", "danger")
        return redirect(url_for('interview_preparation', video_id=first_video_id))

    return render_template('interview_prep_course_page.html', course_data=INTERVIEW_PREP_DATA, current_video=current_video, current_topic_name=current_topic_name)

@app.route('/projects')
def projects():
    project_list = PROJECTS_DATA.get('projects', [])
    page_title = PROJECTS_DATA.get('page_title', 'Projects')
    hero_image = PROJECTS_DATA.get('hero_image_url', '')
    return render_template('projects.html', 
                           projects=project_list,
                           page_title=page_title,
                           hero_image=hero_image)

# --- Error Handlers ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    logging.error(f"Server Error: {e}", exc_info=True)
    return render_template('index.html'), 500

# --- App Runner ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
