# Job-Portal-master/background_tasks.py
import os
import logging
import json
import requests
from dataclasses import asdict
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, TimeoutException
from threading import Thread

# This import will work after you have fixed the directory structure
# as described in the previous step.
from linkedin_scraper.person import Person
from linkedin_scraper.actions import login

from cv_parser import parse_cv_to_json
from database import update_candidate_profile

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s')

def determine_profile_status(person_obj):
    """Determine a candidate's status based on scraped LinkedIn data."""
    if not person_obj:
        return "Unknown"
        
    if person_obj.open_to_work:
        return "Open to Work"
    
    if person_obj.experiences:
        latest_exp = person_obj.experiences[0]
        if 'present' in (latest_exp.to_date or '').lower():
            if 'intern' in (latest_exp.position_title or '').lower():
                return "Internship"
            return "Employed"
            
    return "Seeking Opportunities"

def scrape_linkedin_profile(user_id, linkedin_url):
    """
    The core logic for scraping a LinkedIn profile.
    This runs inside a background thread.
    """
    linkedin_user = os.environ.get("LINKEDIN_USER")
    linkedin_password = os.environ.get("LINKEDIN_PASSWORD")

    if not all([linkedin_user, linkedin_password]):
        logging.error("LINKEDIN_USER and LINKEDIN_PASSWORD environment variables are not set. Skipping scrape.")
        return

    driver = None
    try:
        # --- Selenium Driver Setup for Production (Docker on Render) ---
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        driver = webdriver.Chrome(options=options)
        
        logging.info(f"Attempting to log in to LinkedIn as {linkedin_user}...")
        login(driver, linkedin_user, linkedin_password, timeout=15)
        
        logging.info(f"Scraping LinkedIn profile for user_id: {user_id} from URL: {linkedin_url}")
        person = Person(linkedin_url, driver=driver, scrape=True, close_on_complete=False)
        
        status = determine_profile_status(person)
        
        linkedin_data = {
            "name": person.name, "location": person.location, "about": person.about,
            "open_to_work": person.open_to_work,
            "experiences": [asdict(e) for e in person.experiences],
            "educations": [asdict(e) for e in person.educations],
            "skills": [asdict(s) for s in person.skills],
            "accomplishments": [asdict(a) for a in person.accomplishments],
            "contacts": person.contacts,
        }
        
        update_candidate_profile(user_id, linkedin_data=json.dumps(linkedin_data), profile_status=status)
        logging.info(f"Successfully scraped and stored LinkedIn data for user_id: {user_id}")
        
    except TimeoutException as e:
        logging.error(f"Timeout error for user_id {user_id}: {e}. LinkedIn may be blocking or page is slow.")
    except WebDriverException as e:
        logging.error(f"WebDriver/Selenium error for user_id {user_id}: {e}.")
    except Exception as e:
        logging.error(f"Failed to scrape LinkedIn profile for user_id {user_id}: {e}", exc_info=True)
    finally:
        if driver:
            driver.quit()
            logging.info(f"Chrome driver quit for user_id {user_id} scrape task.")

# --- vvv THIS IS THE UPDATED FUNCTION vvv ---
def process_uploaded_cv(user_id, cv_url):
    """
    The core logic for parsing a CV from a URL.
    This runs inside a background thread.
    """
    try:
        logging.info(f"Downloading and parsing CV for user_id: {user_id} from URL: {cv_url}")
        
        # Download the PDF content from the Cloudinary URL
        response = requests.get(cv_url, stream=True, timeout=30)
        response.raise_for_status() # Will raise an exception for bad status codes
        
        # Get the PDF content in bytes
        pdf_content = response.content
        
        # Pass the content directly to the parser
        cv_json_data = parse_cv_to_json(pdf_content)
        
        update_candidate_profile(user_id, cv_data=json.dumps(cv_json_data))
        logging.info(f"Successfully parsed and stored CV data for user_id: {user_id}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download CV for user_id {user_id} from {cv_url}: {e}", exc_info=True)
    except Exception as e:
        logging.error(f"Failed to parse CV for user_id {user_id}: {e}", exc_info=True)
# --- MISSING FUNCTIONS - NOW ADDED ---

def run_linkedin_scrape(user_id, linkedin_url):
    """
    This is the function that candidate_routes.py imports.
    It starts the scraping logic in a new background thread.
    """
    thread = Thread(target=scrape_linkedin_profile, args=(user_id, linkedin_url), name=f"LinkedInScrape-{user_id}")
    thread.daemon = True
    thread.start()
    logging.info(f"Started background thread for LinkedIn scraping for user {user_id}.")

def run_cv_parse(user_id, cv_url_or_path):
    """
    This is the function that candidate_routes.py imports.
    It starts the CV parsing logic in a new background thread.
    Now accepts a URL.
    """
    thread = Thread(target=process_uploaded_cv, args=(user_id, cv_url_or_path), name=f"CVParse-{user_id}")
    thread.daemon = True
    thread.start()
    logging.info(f"Started background thread for CV parsing for user {user_id}.")
