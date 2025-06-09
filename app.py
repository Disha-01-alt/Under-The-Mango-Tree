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
except (FileNotFoundError, json.JSONDecodeError):
    PYTHON_DATA = {"topics": [], "course_title": "Error"}

def find_video_by_id(video_id, data_source):
    """Helper function to find a specific video and its topic."""
    for topic in data_source.get('topics', []):
        for video in topic.get('videos', []):
            if str(video.get('id')) == str(video_id):
                return video, topic['name'] # Return video and its topic name
    return None, None # Not found
# --- ADD THIS NEW BLOCK FOR MACHINE LEARNING DATA ---
try:
    with open(os.path.join('data', 'machine_learning_data.json'), 'r') as f:
        ml_data = json.load(f)
        ML_VIDEO_DATA = ml_data['ML_VIDEO_DATA']
        ML_SIDEBAR_TOPICS = ml_data['ML_SIDEBAR_TOPICS']
except FileNotFoundError:
    print("ERROR: machine_learning_data.json not found. Creating empty placeholders.")
    ML_VIDEO_DATA = {}
    ML_SIDEBAR_TOPICS = []
# --- END OF NEW BLOCK ---
try:
    with open(os.path.join('data', 'deep_learning_data.json'), 'r') as f:
        dl_data = json.load(f)
        DL_VIDEO_DATA = dl_data['DL_VIDEO_DATA']
        DL_SIDEBAR_TOPICS = dl_data['DL_SIDEBAR_TOPICS']
except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
    print(f"ERROR: Could not load or parse deep_learning_data.json: {e}")
    DL_VIDEO_DATA = {}
    DL_SIDEBAR_TOPICS = []
# --- END OF NEW BLOCK ---
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

@app.route('/python-learning')
def python_learning():
    video_id = request.args.get('video_id')
    
    # If no video_id is provided, show the first video of the first topic
    if not video_id:
        if PYTHON_DATA['topics'] and PYTHON_DATA['topics'][0]['videos']:
            first_video_id = PYTHON_DATA['topics'][0]['videos'][0]['id']
            return redirect(url_for('python_learning', video_id=first_video_id))
        else:
            # Handle case where there is no data at all
            flash("No Python learning videos are available at the moment.", "warning")
            return render_template('course_page_new.html', course_data=PYTHON_DATA, current_video=None, current_topic_name=None)

    # Find the requested video
    current_video, current_topic_name = find_video_by_id(video_id, PYTHON_DATA)

    if not current_video:
        flash(f"Video with ID {video_id} not found.", "danger")
        return redirect(url_for('python_learning')) # Redirect to the first video

    return render_template(
        'course_page_new.html', 
        course_data=PYTHON_DATA,       # Pass the whole data structure for the sidebar
        current_video=current_video,   # Pass the single video object to display
        current_topic_name=current_topic_name # Pass the topic name for highlighting
    )
# It's a copy of the machine_learning route, adapted for the new DL variables.
@app.route('/deep-learning-ai')
def deep_learning_ai():
    # Use the new variables we created from the JSON transformation
    if not DL_SIDEBAR_TOPICS:
        flash("Deep Learning course data is currently unavailable.", "warning")
        selected_topic = None
    else:
        selected_topic = request.args.get('topic', DL_SIDEBAR_TOPICS[0])

    # Get all videos for the selected topic
    videos = DL_VIDEO_DATA.get(selected_topic, [])
    
    # Create sidebar topics with status indicators
    sidebar_topics_with_status = []
    for topic in DL_SIDEBAR_TOPICS:
        topic_data = {
            'name': topic,
            'video_count': len(DL_VIDEO_DATA.get(topic, [])),
            'is_active': topic == selected_topic,
            'url_param': topic.replace(' ', '%20')
        }
        sidebar_topics_with_status.append(topic_data)
    
    # IMPORTANT: We re-use the machine_learning.html template!
    return render_template('deep_learning_ai.html',
                           videos=videos,
                           sidebar_topics=sidebar_topics_with_status,
                           selected_topic=selected_topic,
                           course_title="Deep Learning & AI") # Optional: Pass a title
@app.route('/english-learning')
def english_learning():
    # Use the custom English learning page with cards
    return render_template('english_learning.html')

@app.route('/machine-learning')
def machine_learning():
    # Get selected topic from query parameter, default to first topic
    # This line will now work correctly if data loads, or fail gracefully if it doesn't
    selected_topic = request.args.get('topic', ML_SIDEBAR_TOPICS[0] if ML_SIDEBAR_TOPICS else None)
    
    # Get all videos for the selected topic (no pagination)
    videos = ML_VIDEO_DATA.get(selected_topic, [])
    
    # Create sidebar topics with status indicators
    sidebar_topics_with_status = []
    for topic in ML_SIDEBAR_TOPICS:
        topic_data = {
            'name': topic,
            'video_count': len(ML_VIDEO_DATA.get(topic, [])),
            'is_active': topic == selected_topic,
            'url_param': topic.replace(' ', '%20')  # URL encode spaces
        }
        sidebar_topics_with_status.append(topic_data)
    
    return render_template('machine_learning.html',
                           videos=videos,
                           sidebar_topics=sidebar_topics_with_status,
                           selected_topic=selected_topic)
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
