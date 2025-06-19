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
from database import get_all_jobs

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
SOFT_SKILLS_DATA = load_course_data('soft_skills.json')
PROJECTS_DATA = load_course_data('projects_data.json')
TEAM_DATA = load_course_data('team_data.json')
TESTIMONIALS_DATA = load_course_data('testimonials.json')
# Note: INTERVIEW_PREP_DATA is referenced but not loaded. Check if needed or typo.
# Assuming SOFT_SKILLS_DATA might have been intended for the soft skills route render_template

logging.info("All course and site data loaded.")

# --- Route Definitions ---

@app.route('/')
def home():
    try:
        recent_jobs = get_all_jobs()[:4]
    except Exception as e:
        logging.error(f"Could not fetch jobs for homepage: {e}")
        recent_jobs = []

    # Get the testimonials list from the loaded data
    testimonials = TESTIMONIALS_DATA.get('testimonials', [])

    return render_template(
        'index.html',
        recent_jobs=recent_jobs,
        testimonials=testimonials  # <-- Pass testimonials to the template
    )

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

# Setup English learning module
english_path = os.path.join('static', 'english')
if os.path.exists(english_path):
    print(f"English learning module found at {english_path}")
else:
    print(f"English learning module not found at {english_path}")

# --- English Learning Static File Routes (HTML) ---
# These routes serve specific HTML files directly from the static/english directory.
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

# --- English Learning Static File Routes (JSON) ---
# These routes serve specific JSON data files directly from the static/english directory.
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

# Route to render the main English Learning landing page template
@app.route('/english-learning')
def english_learning():
    return render_template('english_learning.html')


# --- Dynamic Course Routes (Updated to use the new helper) ---

@app.route('/python-learning/')
@app.route('/python-learning/<video_id>')
def python_learning(video_id=None):
    if not video_id:
        # Redirect to the first video if no ID is provided
        first_video_id = PYTHON_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id') if PYTHON_DATA.get('topics') else None
        if first_video_id is not None:
             return redirect(url_for('python_learning', video_id=first_video_id))
        else:
             # Handle case where there's no data loaded
             return render_template('python_learning.html', course_data={"topics": [], "course_title": "Python Learning - No Data Available"})

    current_video, topic_name, prev_video, next_video = find_video_details(video_id, PYTHON_DATA)
    if not current_video:
        # Redirect to the base page if video_id is not found
        flash(f"Video with ID {video_id} not found.", 'error') # Optional: add a flash message
        return redirect(url_for('python_learning'))

    return render_template('python_learning.html', course_data=PYTHON_DATA, current_video=current_video, current_topic_name=topic_name, prev_video=prev_video, next_video=next_video)

@app.route('/machine-learning/')
@app.route('/machine-learning/<video_id>')
def machine_learning(video_id=None):
    if not video_id:
        first_video_id = ML_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id') if ML_DATA.get('topics') else None
        if first_video_id is not None:
             return redirect(url_for('machine_learning', video_id=first_video_id))
        else:
             return render_template('machine_learning.html', course_data={"topics": [], "course_title": "Machine Learning - No Data Available"})

    current_video, topic_name, prev_video, next_video = find_video_details(video_id, ML_DATA)
    if not current_video:
        flash(f"Video with ID {video_id} not found.", 'error')
        return redirect(url_for('machine_learning'))

    return render_template('machine_learning.html', course_data=ML_DATA, current_video=current_video, current_topic_name=topic_name, prev_video=prev_video, next_video=next_video)

@app.route('/deep-learning-ai/')
@app.route('/deep-learning-ai/<video_id>')
def deep_learning_ai(video_id=None):
    if not video_id:
        first_video_id = DL_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id') if DL_DATA.get('topics') else None
        if first_video_id is not None:
             return redirect(url_for('deep_learning_ai', video_id=first_video_id))
        else:
             return render_template('deep_learning_ai.html', course_data={"topics": [], "course_title": "Deep Learning AI - No Data Available"})

    current_video, topic_name, prev_video, next_video = find_video_details(video_id, DL_DATA)
    if not current_video:
        flash(f"Video with ID {video_id} not found.", 'error')
        return redirect(url_for('deep_learning_ai'))

    return render_template('deep_learning_ai.html', course_data=DL_DATA, current_video=current_video, current_topic_name=topic_name, prev_video=prev_video, next_video=next_video)

@app.route('/algorithms/')
@app.route('/algorithms/<video_id>')
def algorithms(video_id=None):
    if not video_id:
        first_video_id = ALGORITHMS_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id') if ALGORITHMS_DATA.get('topics') else None
        if first_video_id is not None:
             return redirect(url_for('algorithms', video_id=first_video_id))
        else:
             return render_template('algorithms_course_page.html', course_data={"topics": [], "course_title": "Algorithms - No Data Available"})

    current_video, topic_name, prev_video, next_video = find_video_details(video_id, ALGORITHMS_DATA)
    if not current_video:
        flash(f"Video with ID {video_id} not found.", 'error')
        return redirect(url_for('algorithms'))

    return render_template('algorithms_course_page.html', course_data=ALGORITHMS_DATA, current_video=current_video, current_topic_name=topic_name, prev_video=prev_video, next_video=next_video)

@app.route('/soft-skills/')
@app.route('/soft-skills/<video_id>')
def soft_skills(video_id=None):
    if not video_id:
        # Assuming SOFT_SKILLS_DATA is correct, previously referenced INTERVIEW_PREP_DATA here
        first_video_id = SOFT_SKILLS_DATA.get('topics', [{}])[0].get('videos', [{}])[0].get('id') if SOFT_SKILLS_DATA.get('topics') else None
        if first_video_id is not None:
             return redirect(url_for('soft_skills', video_id=first_video_id))
        else:
             return render_template('soft_skills.html', course_data={"topics": [], "course_title": "Soft Skills - No Data Available"}) # Use SOFT_SKILLS_DATA here

    current_video, topic_name, prev_video, next_video = find_video_details(video_id,SOFT_SKILLS_DATA)
    if not current_video:
        flash(f"Video with ID {video_id} not found.", 'error')
        return redirect(url_for('soft_skills'))

    return render_template('soft_skills.html', course_data=SOFT_SKILLS_DATA, current_video=current_video, current_topic_name=topic_name, prev_video=prev_video, next_video=next_video)


@app.route('/projects')
def projects():
    all_projects = PROJECTS_DATA.get('projects', [])
    categories_config = PROJECTS_DATA.get('categories_config', {}) # Load the config

    # Calculate category counts dynamically based on existing projects
    category_counts = {'All': len(all_projects)}
    # Initialize counts for categories defined in the config (excluding 'All')
    for category_key in categories_config:
        if category_key != 'All':
             category_counts[category_key] = 0

    # Count projects per category
    for project in all_projects:
        category = project.get('category') # Get category key from project
        # Only increment if the category exists in our config (excluding 'All')
        if category in category_counts and category != 'All':
             category_counts[category] += 1

    # Prepare categories data for the template, including config and counts
    # We'll create a list of category objects to loop through in the template
    # Order is important, put 'All' first
    display_categories = []
    if 'All' in categories_config:
         all_config = categories_config['All']
         display_categories.append({
              'key': 'All',
              'name': all_config.get('name', 'All'),
              'icon': all_config.get('icon', 'fas fa-globe-americas'), # Default icon for All
              'count': category_counts.get('All', 0)
         })

    for category_key, config in categories_config.items():
        if category_key != 'All':
             display_categories.append({
                 'key': category_key, # Keep the key for potential JS filtering
                 'name': config.get('name', category_key),
                 'icon': config.get('icon', 'fas fa-folder'), # Default icon for others
                 'count': category_counts.get(category_key, 0)
             })


    return render_template('projects.html',
                         projects=all_projects,
                         page_title=PROJECTS_DATA.get('page_title', 'Projects'),
                         subtitle=PROJECTS_DATA.get('subtitle', 'A showcase of our practical and innovative work.'), # Pass subtitle
                         hero_image=PROJECTS_DATA.get('hero_image_url', ''),
                         display_categories=display_categories # Pass the list of categories with counts and config
                         )


# --- Error Handlers ---
# --- Error Handlers ---
@app.errorhandler(404)
def page_not_found(e):
    logging.error(f"404 Not Found: {request.url}", exc_info=True) # Log the URL that wasn't found
    # Use an existing template instead of 404.html
    return render_template('index.html'), 404 # Or 'base.html' or another common one

@app.errorhandler(500)
def server_error(e):
    logging.error(f"Server Error: {e}", exc_info=True)
    # Use an existing template instead of 500.html
    return render_template('index.html'), 500 # Or 'base.html' or another common one
# --- App Runner ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # For production deployment (like Render), gunicorn will handle running the app.
    # The code below is typically for local development.
    # If deploying with gunicorn, you'll use 'gunicorn app:app' command,
    # so this block only runs when you execute `python app.py` directly.
    app.run(host='0.0.0.0', port=port, debug=True)
