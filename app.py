import os
import sys
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import Flask, render_template, send_from_directory, url_for, redirect, send_file, flash,request
import importlib.util
import logging
import json
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
load_dotenv()  # Automatically loads the .env file
from ateam import team_members, support_pillars
# Make sure these paths are correct relative to your app.py
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
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    secure = True # Ensures HTTPS URLs
)
logging.info("Cloudinary configured.") # Add logging to confirm

app.secret_key = os.environ.get("SESSION_SECRET", "utmt_default_secret_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'google_auth.login'
login_manager.login_message = 'Please log in to access this page.'
# IMPORTANT: Register with a URL Prefix
PORTAL_PREFIX = '/portal'
app.register_blueprint(auth_bp, url_prefix=f'{PORTAL_PREFIX}/auth')
app.register_blueprint(candidate_bp, url_prefix=f'{PORTAL_PREFIX}/candidate')
app.register_blueprint(admin_bp, url_prefix=f'{PORTAL_PREFIX}/admin')
app.register_blueprint(company_bp, url_prefix=f'{PORTAL_PREFIX}/company')
# The google_auth blueprint handles its own root-level URLs like /google_login
app.register_blueprint(google_auth, url_prefix=PORTAL_PREFIX)
# Import database initialization
from database import init_db

# Initialize database
with app.app_context():
    init_db()

# Import auth setup
from auth import setup_auth
setup_auth(login_manager)
# Load Python learning data from JSON file
try:
    with open(os.path.join('data', 'python_learning_data.json'), 'r') as f:
        PYTHON_DATA = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"ERROR loading python_learning_data.json: {e}")
    # Create a default empty structure so the app doesn't crash
    PYTHON_DATA = {"topics": [], "course_title": "Error: Data Not Found"}

def find_video_by_id(video_id, data_source):
    """Helper function to find a specific video and its topic from the structured data."""
    if not video_id:
        return None, None
    for topic in data_source.get('topics', []):
        for video in topic.get('videos', []):
            if str(video.get('id')) == str(video_id):
                return video, topic.get('name')  # Return the video object and its topic name
    return None, None  # Return None if not found

# --- ADD THIS NEW BLOCK FOR MACHINE LEARNING DATA ---
try:
    with open(os.path.join('data', 'machine_learning_data.json'), 'r') as f:
        ML_DATA = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"ERROR loading machine_learning_data.json: {e}")
    # Create a default empty structure so the app doesn't crash
    ML_DATA = {"topics": [], "course_title": "Error: Data Not Found"}

# The find_video_by_id helper function is reusable for all courses.
# Ensure it is defined once in your app.py, like this:
def find_video_by_id(video_id, data_source):
    """Helper function to find a specific video and its topic from the structured data."""
    if not video_id:
        return None, None
    for topic in data_source.get('topics', []):
        for video in topic.get('videos', []):
            if str(video.get('id')) == str(video_id):
                return video, topic.get('name')  # Return the video object and its topic name
    return None, None  # Return None if not found
DL_SIDEBAR_TOPICS
try:
    with open(os.path.join('data', 'deep_learning_data.json'), 'r') as f:
        DL_DATA = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"ERROR loading deep_learning_data.json: {e}")
    # Create a default empty structure so the app doesn't crash
    DL_DATA = {"topics": [], "course_title": "Error: Data Not Found"}

# The find_video_by_id helper function is reusable for all courses.
# Make sure it is defined once in your app.py.
def find_video_by_id(video_id, data_source):
    """Helper function to find a specific video and its topic from the structured data."""
    if not video_id:
        return None, None
    for topic in data_source.get('topics', []):
        for video in topic.get('videos', []):
            if str(video.get('id')) == str(video_id):
                return video, topic.get('name')  # Return the video object and its topic name
    return None, None  # Return None if not found

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
# Create required directories
os.makedirs('static/english/images', exist_ok=True)
os.makedirs('static/english', exist_ok=True)
upload_dirs = ['uploads/cvs', 'uploads/id_cards', 'uploads/marksheets', 'uploads/temp_cvs']
for directory in upload_dirs:
    os.makedirs(directory, exist_ok=True)
# --- 6. Create a Route for the Job Portal Homepage ---
@app.route(PORTAL_PREFIX) # e.g., yoursite.com/portal
def job_portal_index():
    # This renders the Job Portal's main landing page
    return redirect(url_for('job_portal_main_page'))

# This is the original index route from the job portal's app.py, now repurposed
@app.route(f'{PORTAL_PREFIX}/index')
def job_portal_main_page():
    from flask_login import current_user
    if current_user.is_authenticated:
        # These url_for calls will correctly point to the prefixed routes
        if current_user.role == 'candidate':
            return redirect(url_for('candidate_routes.dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin_routes.dashboard'))
        elif current_user.role == 'company':
            return redirect(url_for('company_routes.dashboard'))
    return render_template('job_portal/index.html')


# Setup English learning module
english_path = os.path.join('static', 'english')
if os.path.exists(english_path):
    print(f"English learning module found at {english_path}")
else:
    print(f"English learning module not found at {english_path}")

# Serve English learning files directly
@app.route('/HinToEng.html')
def hin_to_eng():
    return send_from_directory('static/english', 'HinToEng.html')

@app.route('/PicToEng.html')
def pic_to_eng():
    return send_from_directory('static/english', 'PicToEng.html')

@app.route('/SentCorrect.html')
def sent_correct():
    return send_from_directory('static/english', 'SentCorrect.html')

@app.route('/QnA.html')
def qna():
    return send_from_directory('static/english', 'QnA.html')

@app.route('/guessWord.html')
def guess_word():
    return send_from_directory('static/english', 'guessWord.html')

@app.route('/PrepositionGame.html')
def preposition_game():
    return send_from_directory('static/english', 'PrepositionGame.html')

@app.route('/Synonyms.html')
def synonyms():
    return send_from_directory('static/english', 'Synonyms.html')

@app.route('/odd_one_out.html')
def odd_one_out():
    return send_from_directory('static/english', 'odd_one_out.html')

# Serve JSON files for English learning
@app.route('/HinToEng.json')
def hin_to_eng_json():
    return send_from_directory('static/english', 'HinToEng.json')

@app.route('/PicToEng.json')
def pic_to_eng_json():
    return send_from_directory('static/english', 'PicToEng.json')

@app.route('/SentCorrect.json')
def sent_correct_json():
    return send_from_directory('static/english', 'SentCorrect.json')

@app.route('/QnA.json')
def qna_json():
    return send_from_directory('static/english', 'QnA.json')

@app.route('/guessWord.json')
def guess_word_json():
    return send_from_directory('static/english', 'guessWord.json')

@app.route('/Prepositions.json')
def prepositions_json():
    return send_from_directory('static/english', 'Prepositions.json')

@app.route('/Synonym.json')
def synonym_json():
    return send_from_directory('static/english', 'Synonym.json')

@app.route('/odd_one_out.json')
def odd_one_out_json():
    return send_from_directory('static/english', 'odd_one_out.json')

# Define routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/learning-hub')
def learning_hub():
    return render_template('learning_hub.html')

# In app.py

@app.route('/python-learning')
def python_learning():
    # Get the requested video ID from the URL's query parameters
    video_id_to_find = request.args.get('video_id')
    
    # CASE 1: The user just arrived at /python-learning without a specific video ID.
    # We should redirect them to the very first video in the course.
    if not video_id_to_find:
        # Try to find the first video ID to redirect to
        if PYTHON_DATA.get('topics') and PYTHON_DATA['topics'][0].get('videos'):
            first_video_id = PYTHON_DATA['topics'][0]['videos'][0]['id']
            return redirect(url_for('python_learning', video_id=first_video_id))
        else:
            # This is an edge case: the JSON file is empty or malformed.
            flash("No Python learning content is available at the moment.", "warning")
            return render_template(
                'python_learning.html',
                course_data=PYTHON_DATA,
                current_video=None,
                current_topic_name=None
            )

    # CASE 2: A video ID was provided. Find the video.
    current_video, current_topic_name = find_video_by_id(video_id_to_find, PYTHON_DATA)
    
    # If the video ID from the URL is invalid, redirect to the homepage or a safe default.
    if not current_video:
        flash(f"The requested video (ID: {video_id_to_find}) could not be found.", "danger")
        return redirect(url_for('home')) # Redirect to the main homepage

    # SUCCESS: We found the video. Render the page with all the necessary data.
    return render_template(
        'python_learning.html',
        course_data=PYTHON_DATA,        # The entire course data for the sidebar
        current_video=current_video,    # The specific video object to display
        current_topic_name=current_topic_name # The name of the topic for highlighting
    )
# --- THE NEW AND FINAL DEEP LEARNING ROUTE ---
@app.route('/deep-learning-ai')
def deep_learning_ai():
    # Attempt to load the first available video if no specific ID is given
    first_video_id = None
    if DL_DATA.get('topics') and DL_DATA['topics'][0].get('videos'):
        first_video_id = DL_DATA['topics'][0]['videos'][0]['id']

    # Get video_id from URL, or default to the first video if available
    video_id_to_find = request.args.get('video_id', first_video_id)

    # CASE 1: No videos exist in the data file at all
    if not video_id_to_find:
        flash("No Deep Learning content is available at the moment.", "warning")
        return render_template(
            'deep_learning_ai.html', 
            course_data=DL_DATA, 
            current_video=None, 
            current_topic_name=None
        )

    # CASE 2: A video ID exists, so we try to find the video
    current_video, current_topic_name = find_video_by_id(video_id_to_find, DL_DATA)

    # If the specific video wasn't found (e.g., bad ID in URL), redirect
    if not current_video:
        flash(f"The requested video (ID: {video_id_to_find}) could not be found. Showing the first video instead.", "info")
        return redirect(url_for('deep_learning_ai', video_id=first_video_id))
        
    # SUCCESS CASE: Video was found, render the page
    return render_template(
        'deep_learning_ai.html', 
        course_data=DL_DATA,
        current_video=current_video,
        current_topic_name=current_topic_name
    )
@app.route('/english-learning')
def english_learning():
    # Use the custom English learning page with cards
    return render_template('english_learning.html')

@app.route('/machine-learning')
def machine_learning():
    # Attempt to load the first available video if no specific ID is given
    first_video_id = None
    if ML_DATA.get('topics') and ML_DATA['topics'][0].get('videos'):
        first_video_id = ML_DATA['topics'][0]['videos'][0]['id']

    # Get video_id from URL, or default to the first video if available
    video_id_to_find = request.args.get('video_id', first_video_id)

    # CASE 1: No videos exist in the data file at all
    if not video_id_to_find:
        flash("No Machine Learning content is available at the moment.", "warning")
        return render_template(
            'machine_learning.html', 
            course_data=ML_DATA, 
            current_video=None, 
            current_topic_name=None
        )

    # CASE 2: A video ID exists, so we try to find the video
    current_video, current_topic_name = find_video_by_id(video_id_to_find, ML_DATA)

    # If the specific video wasn't found (e.g., bad ID in URL), redirect
    if not current_video:
        flash(f"The requested video (ID: {video_id_to_find}) could not be found. Showing the first video instead.", "info")
        return redirect(url_for('machine_learning', video_id=first_video_id))
        
    # SUCCESS CASE: Video was found, render the page
    return render_template(
        'machine_learning.html', 
        course_data=ML_DATA,
        current_video=current_video,
        current_topic_name=current_topic_name
    )
@app.route('/team')
def team():
    return render_template('team.html', 
                         team_members=team_members, 
                         support_pillars=support_pillars)
# for rule in app.url_map.iter_rules():
#     print(rule.endpoint, rule.rule)

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('index.html'), 500
# ERROR HANDLERS
# ===================================================================

@app.errorhandler(404)
def page_not_found(e):
    # This renders your main site's 404 page (or index as a fallback)
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    logging.error(f"Server Error: {e}", exc_info=True)
    # This renders your main site's 500 page (or index as a fallback)
    return render_template('index.html'), 500


# ===================================================================
# APP RUNNER
# ===================================================================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # Set debug=False for production
    app.run(host='0.0.0.0', port=port, debug=True)
