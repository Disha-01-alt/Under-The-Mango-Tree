import json
import os
import requests
from flask import Blueprint, redirect, request, url_for, session, flash
from flask_login import login_user, logout_user, current_user, login_required
from oauthlib.oauth2 import WebApplicationClient
from database import get_user_by_email, create_user, get_user_by_id
from models import User
from database import get_user_by_email, create_user, get_user_by_id, is_company_email
import logging

# --- Environment Variable Handling for OAuthLib ---
if os.environ.get("FLASK_ENV") == "development" or not os.environ.get("RENDER_EXTERNAL_URL"):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    logging.warning("OAUTHLIB_INSECURE_TRANSPORT enabled. Ensure HTTPS and this is disabled in production.")

# --- Google OAuth Configuration ---
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# --- Blueprint Definition ---
google_auth = Blueprint("google_auth", __name__)

# --- OAuth Client Initialization ---
if not GOOGLE_CLIENT_ID:
    logging.critical("CRITICAL: GOOGLE_OAUTH_CLIENT_ID is NOT SET. Google OAuth will fail.")
    client = None
else:
    client = WebApplicationClient(GOOGLE_CLIENT_ID)

# --- Helper Functions ---
def get_google_provider_cfg():
    """Fetches Google's OpenID configuration."""
    try:
        response = requests.get(GOOGLE_DISCOVERY_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch Google's OpenID configuration: {e}")
        return None

def get_redirect_url():
    """
    Determines the correct OAuth2 redirect URI based on the environment.
    """
    env_redirect_uri = os.environ.get("GOOGLE_OAUTH_REDIRECT_URI")
    if env_redirect_uri:
        logging.info(f"Using GOOGLE_OAUTH_REDIRECT_URI from environment: {env_redirect_uri}")
        return env_redirect_uri

    render_external_url = os.environ.get("RENDER_EXTERNAL_URL")
    if render_external_url:
        redirect_uri = f"{render_external_url}/portal/google_login/callback"
        logging.info(f"Using Render auto-detected redirect URI: {redirect_uri}")
        return redirect_uri
    
    local_redirect_uri = "http://127.0.0.1:5000/portal/google_login/callback"
    logging.info(f"Using local development redirect URI: {local_redirect_uri}")
    return local_redirect_uri

# --- Routes ---
@google_auth.route("/google_login")
def login():
    if not client:
        flash("Google OAuth is not configured on the server. Please contact support.", "error")
        return redirect(url_for('job_portal_index'))

    google_provider_cfg = get_google_provider_cfg()
    if not google_provider_cfg or "authorization_endpoint" not in google_provider_cfg:
        flash("Could not connect to Google for authentication (config error). Please try again later.", "error")
        return redirect(url_for("job_portal_index"))
        
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    redirect_uri = get_redirect_url()
    
    logging.debug(f"Google OAuth: Initiating login. Redirect URI will be: {redirect_uri}")

    try:
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=redirect_uri,
            scope=["openid", "email", "profile"],
        )
    except Exception as e:
        logging.error(f"Error preparing Google request URI: {e}. Check client_id/redirect_uri.")
        flash("Error initiating Google Sign-In. Check server configuration.", "error")
        return redirect(url_for('job_portal_index'))
        
    return redirect(request_uri)

@google_auth.route("/google_login/callback")
def callback():
    if not client:
        flash("Google OAuth is not configured on the server (callback).", "error")
        return redirect(url_for('job_portal_index'))

    code = request.args.get("code")
    if not code:
        error_reason = request.args.get("error_description") or request.args.get("error")
        logging.error(f"Google OAuth callback error: Missing 'code'. Reason: {error_reason}")
        flash(f"Authentication failed with Google. Reason: {error_reason or 'Code not provided.'}", "error")
        # CORRECTED REDIRECT
        return redirect(url_for("job_portal_index")) 

    google_provider_cfg = get_google_provider_cfg()
    if not google_provider_cfg or "token_endpoint" not in google_provider_cfg:
        flash("Could not verify auth with Google (server config error).", "error")
        return redirect(url_for("job_portal_index"))

    token_endpoint = google_provider_cfg["token_endpoint"]
    redirect_uri_for_token = get_redirect_url()

    try:
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url, 
            redirect_url=redirect_uri_for_token, 
            code=code
        )
        logging.debug(f"Requesting token. URL: {token_url}, Redirect: {redirect_uri_for_token}")

        token_response = requests.post(
            token_url, headers=headers, data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET), timeout=10
        )
        token_response.raise_for_status()
        client.parse_request_body_response(json.dumps(token_response.json()))

        userinfo_endpoint = google_provider_cfg.get("userinfo_endpoint")
        if not userinfo_endpoint: 
            raise ValueError("Userinfo endpoint not found in Google config.")
        
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body, timeout=10)
        userinfo_response.raise_for_status()
        userinfo = userinfo_response.json()

    except requests.exceptions.RequestException as e:
        logging.error(f"Google OAuth network/HTTP error: {e}", exc_info=True)
        flash(f"Authentication with Google failed. Please check Redirect URI in Google Console. Error: {e}", "error")
        # CORRECTED REDIRECT
        return redirect(url_for("job_portal_index"))
    except Exception as e: 
        logging.exception(f"Unexpected error processing Google callback: {e}")
        flash("An unexpected error occurred during Google sign-in.", "error")
        # CORRECTED REDIRECT
        return redirect(url_for("job_portal_index"))

    if not userinfo.get("email_verified"):
        flash("Your Google email is not verified.", "warning")
        # CORRECTED REDIRECT
        return redirect(url_for("job_portal_index"))

    unique_id = userinfo.get("sub")
    users_email = userinfo.get("email","").lower() 
    users_name_from_google = userinfo.get("given_name") or (userinfo.get("name", "New User").split(" ")[0])
    picture = userinfo.get("picture")

    if not unique_id or not users_email:
        logging.error(f"Google OAuth response missing sub/email. Info: {userinfo}")
        flash("Could not get profile information from Google.", "error")
        # CORRECTED REDIRECT
        return redirect(url_for("job_portal_index"))

    existing_user_model = get_user_by_email(users_email)
    logging.info(f"Google login for {users_email}. User in DB: {existing_user_model is not None}")

    if existing_user_model:
        # In google_auth.py, inside the callback() function
if existing_user_model:
    # If the user's email is on the company list but their role is not 'company', fix it.
    if is_company_email(users_email) and existing_user_model.role != 'company':
        from database import get_db
        logging.warning(f"Correcting role for {users_email} to 'company' based on whitelist.")
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE users SET role = 'company' WHERE id = %s", (existing_user_model.id,))
        conn.commit()
        existing_user_model.role = 'company'

    login_user(existing_user_model)
    # ... (rest of the existing user logic is fine)
        login_user(existing_user_model)
        session['google_id'] = unique_id 
        session['google_name'] = existing_user_model.full_name or users_name_from_google
        session['google_picture'] = picture
        session.pop('needs_registration_completion', None) 

        flash(f'Welcome back, {existing_user_model.full_name or existing_user_model.email}!', 'success')
        
        if existing_user_model.role == 'admin': return redirect(url_for('admin_routes.dashboard'))
        if existing_user_model.role == 'company':
            return redirect(url_for('company_routes.dashboard')) if existing_user_model.is_approved else redirect(url_for('job_portal_index'))
        if existing_user_model.role == 'candidate': return redirect(url_for('candidate_routes.dashboard'))
        if existing_user_model.role == 'pending_setup':
            session['needs_registration_completion'] = True
            flash('Welcome back! Please complete your registration.', 'info')
            return redirect(url_for('candidate_routes.jobs'))
        
        logging.warning(f"User {users_email} has unexpected role: {existing_user_model.role}. Redirecting home.")
        return redirect(url_for('job_portal_index')) 
    else: # This block handles NEW users who are not in the database yet.
        try:
            # Check if the new user's email is on the company whitelist
            if is_company_email(users_email):
                logging.info(f"New whitelisted company user: {users_email}. Creating 'company' account.")
                # If they are a company, create their account with the 'company' role directly.
                user_id = create_user(
                    email=users_email,
                    password='', # No password for Google users
                    role='company',
                    full_name=users_name_from_google
                )
                newly_created_user_model = get_user_by_id(user_id)
                login_user(newly_created_user_model)
                flash(f'Welcome, {users_name_from_google}! Your company account is now active.', 'success')
                return redirect(url_for('company_routes.dashboard'))
        else:
            # If they are NOT a company, they must be a candidate.
            # Create a 'pending_setup' account and send them to the "Complete Registration" form.
            logging.info(f"New candidate user: {users_email}. Creating 'pending_setup' account.")
            user_id = create_user(
                email=users_email,
                password='',
                role='pending_setup',
                full_name=users_name_from_google
            )
            newly_created_user_model = get_user_by_id(user_id)
            login_user(newly_created_user_model)
            session['needs_registration_completion'] = True
            flash(f'Welcome, {users_name_from_google}! Please complete your registration.', 'info')
            return redirect(url_for('auth_routes.complete_registration'))

    except Exception as e:
        logging.exception(f"Error during new user creation for {users_email}:")
        flash("An error occurred while setting up your account. Please try again.", "error")
        return redirect(url_for('job_portal_index'))
            login_user(newly_created_user_model) 
            
            session['google_id'] = unique_id
            session['google_name'] = users_name_from_google 
            session['google_picture'] = picture
            session['needs_registration_completion'] = True

            flash(f'Welcome, {users_name_from_google}! Please complete your registration.', 'info')
            return redirect(url_for('candidate_routes.jobs'))
        
        except Exception as e:
            logging.exception(f"Error creating user for {users_email}:")
            flash("An error occurred while setting up your account.", "error")
            # CORRECTED REDIRECT
            return redirect(url_for("job_portal_index"))

@google_auth.route("/logout")
@login_required 
def logout():
    user_email_for_log = current_user.email if current_user.is_authenticated else "Unknown"
    logout_user() 
    
    keys_to_pop = ['google_id', 'google_email', 'google_name', 'google_picture', 
                   'needs_registration_completion', '_flashes'] 
    for key in keys_to_pop:
        session.pop(key, None)
    
    flash('You have been logged out successfully.', 'info')
    logging.info(f"User {user_email_for_log} logged out.")
    return redirect(url_for('job_portal_index'))
