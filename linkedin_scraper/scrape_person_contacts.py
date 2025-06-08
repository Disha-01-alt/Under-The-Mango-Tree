


import os
import json
from dataclasses import asdict
from selenium import webdriver
from linkedin_scraper.person import Person

# --- SETUP: LinkedIn credentials ---
LINKEDIN_USER = os.environ.get("LINKEDIN_USER", "your_email_here")
LINKEDIN_PASSWORD = os.environ.get("LINKEDIN_PASSWORD", "your_password_here")

# --- Selenium driver setup ---
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  # Uncomment for headless mode

driver = webdriver.Chrome(options=options)

# --- LinkedIn login ---
def linkedin_login(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    driver.find_element("id", "username").send_keys(username)
    driver.find_element("id", "password").send_keys(password)
    driver.find_element("xpath", "//button[@type='submit']").click()

linkedin_login(driver, LINKEDIN_USER, LINKEDIN_PASSWORD)

# --- Scrape a profile ---
profile_url = "https://www.linkedin.com/in/kushal-shah-95b9a3b/"
person = Person(profile_url, driver=driver, scrape=True, close_on_complete=False)

# --- Prepare data for JSON ---
person_data_to_save = {
    "name": person.name,
    "about": person.about,
    "experiences": [asdict(e) for e in person.experiences],
    "educations": [asdict(e) for e in person.educations],
    "skills": [asdict(s) for s in person.skills],
    "interests": [asdict(i) for i in person.interests],
    "accomplishments": [asdict(a) for a in person.accomplishments],
    "contacts": person.contacts,

}

# --- Sanitize the name to use in filename ---
safe_name = person.name.replace(" ", "_").replace("/", "-")  # Avoid illegal characters
filename = f"{safe_name}.json"

# --- Save to JSON ---
with open(filename, "w", encoding="utf-8") as f:
    json.dump(person_data_to_save, f, ensure_ascii=False, indent=4)

print(f"Scraping complete. Data saved to {filename}.")


# --- Clean up ---
driver.quit()
