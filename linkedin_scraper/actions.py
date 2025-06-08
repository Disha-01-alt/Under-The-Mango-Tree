import time # Ensure this is at the top
import getpass
from . import constants as c
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def __prompt_email_password():
    u = input("Email: ")
    p = getpass.getpass(prompt="Password: ")
    return (u, p)

def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'

def login(driver, email=None, password=None, cookie=None, timeout=10):
    if cookie is not None:
        return _login_with_cookie(driver, cookie)

    if not email or not password:
        email, password = __prompt_email_password()

    driver.get("https://www.linkedin.com/login")
    # Wait for the username field to be present on the login page
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

    email_elem = driver.find_element(By.ID, "username")
    email_elem.send_keys(email)

    password_elem = driver.find_element(By.ID, "password")
    password_elem.send_keys(password)

    # --- Handle "Keep me logged in" checkbox BEFORE submitting password ---
    try:
        # Try to find the "Keep me logged in" checkbox using the ID from constants.py
        keep_logged_in_checkbox = driver.find_element(By.ID, c.REMEMBER_PROMPT)
        if keep_logged_in_checkbox.is_displayed() and not keep_logged_in_checkbox.is_selected():
            keep_logged_in_checkbox.click()
            print("DEBUG: Clicked 'Keep me logged in' checkbox.")
        elif keep_logged_in_checkbox.is_selected():
            print("DEBUG: 'Keep me logged in' checkbox is already checked.")
    except Exception as e:
        # This exception might occur if the checkbox is not present on this specific login form,
        # which is fine, as it's not always there or critical.
        print(f"DEBUG: 'Keep me logged in' checkbox not found or not clickable: {e}")

    # Submit the login form
    password_elem.submit()

    # Add a delay to allow LinkedIn to process the login and redirect
    time.sleep(4) # Give LinkedIn time to process login and potentially redirect

    # --- Check for successful login or specific error messages ---
    try:
        # Try to wait for a common element that appears ONLY on the successful main feed page.
        # Replace c.VERIFY_LOGIN_ID with a robust selector for an element on the main LinkedIn feed.
        # Examples: By.ID("global-nav-typeahead"), By.CSS_SELECTOR(".feed-outlet")
        # If you are unsure, you can open a real LinkedIn page and inspect an element unique to the logged-in state.
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, c.VERIFY_LOGIN_ID)))
        print("INFO: Successfully logged in to LinkedIn!")
        return # Exit the login function if successful

    except Exception as e:
        # If the successful login element is not found, login was likely unsuccessful or a challenge appeared.
        print(f"ERROR: Could not verify successful login (VERIFY_LOGIN_ID not found). Details: {e}")
        print(f"Current URL after login attempt: {driver.current_url}")

        # Check for the "Wrong email or password" error message based on the HTML you provided
        try:
            # Wait for the error message element to be present
            error_message_element = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "error-for-password"))
            )
            error_text = error_message_element.text
            if "Wrong email or password" in error_text:
                print(f"LOGIN FAILED: LinkedIn reports: '{error_text}'")
                print("ACTION REQUIRED: Please double-check your LINKEDIN_USER and LINKEDIN_PASSWORD environment variables.")
                print("NOTE: LinkedIn strongly deters automation. Even with correct credentials, automated login might be blocked.")
            else:
                print(f"LOGIN FAILED: A different error message found: '{error_text}'")
        except Exception as e_error_check:
            print(f"DEBUG: No 'error-for-password' element found on the final page, or it timed out. Details: {e_error_check}")
            print("LinkedIn might have presented a different security challenge (e.g., CAPTCHA, phone verification) or redirected to a different page.")

        # Save the final page source for deep inspection, regardless of the error type
        with open("linkedin_final_failure_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("INFO: Saved the final page source to 'linkedin_final_failure_page.html' for inspection.")

        # Keep the browser open until you manually press Enter, for continued debugging.
        input("Press Enter in this terminal to close the browser (after inspecting 'linkedin_final_failure_page.html')...")
        driver.quit() # Close the browser after user input
        raise # Re-raise the original exception to ensure the script properly indicates failure

def _login_with_cookie(driver, cookie):
    driver.get("https://www.linkedin.com/login")
    driver.add_cookie({
        "name": "li_at",
        "value": cookie
    })