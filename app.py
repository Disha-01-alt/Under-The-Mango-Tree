import os
import sys
from flask import Flask, render_template, send_from_directory, url_for, redirect, send_file, flash
from flask_sqlalchemy import SQLAlchemy
import importlib.util
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get("SESSION_SECRET", "utmt_default_secret_key")

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db = SQLAlchemy(app)

# Create required directories
os.makedirs('static/images', exist_ok=True)
os.makedirs('static/english', exist_ok=True)
os.makedirs('uploads/cv', exist_ok=True)
os.makedirs('uploads/id_card', exist_ok=True)
os.makedirs('uploads/marksheet', exist_ok=True)

# Setup English learning module
english_path = os.path.join('english')
if os.path.exists(english_path):
    print(f"English learning module found at {english_path}")
else:
    print(f"English learning module not found at {english_path}")

# Setup Job Portal module
job_portal_path = os.path.join('jobportal') 
if os.path.exists(job_portal_path):
    print(f"Job Portal module found at {job_portal_path}")
else:
    print(f"Job Portal module not found at {job_portal_path}")

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
    return render_template('python_learning.html')

@app.route('/english-learning')
def english_learning():
    # Use the custom English learning page with cards
    return render_template('english_learning.html')
@app.route('/machine-learning')
def machine_learning():
    return render_template('machine_learning.html')

@app.route('/deep-learning-ai')
def deep_learning_ai():
    instructor = "Dr. Kushal Shah"
    return render_template('deep_learning_ai.html', instructor_name=instructor)



@app.route('/job-portal', defaults={'path': ''})
@app.route('/job-portal/<path:path>')
def job_portal(path=''):
    from job_portal_bridge import app as job_portal_app
    from flask import request, Response, session
    
    with job_portal_app.test_client() as client:
        # Preserve session
        if 'user_id' in session:
            with client.session_transaction() as sess:
                sess['user_id'] = session['user_id']
        
        # Forward the request
        url = f'/{path}' if path else '/'
        resp = client.open(
            url,
            method=request.method,
            headers={k:v for k,v in request.headers if k != 'Host'},
            data=request.get_data(),
            base_url=request.url_root.rstrip('/') + '/job-portal'
        )
        
        # Handle static files
        if path.startswith(('static/', 'uploads/')):
            return send_from_directory('jobportal', path)
            
        excluded_headers = ['content-length', 'content-encoding', 'transfer-encoding']
        headers = [(k, v) for k, v in resp.headers if k.lower() not in excluded_headers]
        
        return Response(resp.get_data(), resp.status_code, headers)

@app.route('/team')
def team():
    return render_template('team.html')

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('index.html'), 500
