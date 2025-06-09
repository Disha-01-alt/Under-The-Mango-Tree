import json
import os
import requests
import logging
from flask import Blueprint, redirect, request, url_for, session, flash
from flask_login import login_user, logout_user, current_user, login_required
from oauthlib.oauth2 import WebApplicationClient
from database import get_user_by_email, create_user, get_user_by_id, is_company_email, get_db
from models import User

# --- Environment Variable Handling ---
if os.environ.get("FLASK_ENV") == "development" or not os.environ.get("RENDER_EXTERNAL_URL"):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    logging.warning("OAUTHLIB_INSECURE_TRANSPORT enabled for local development.")

# --- Google OAuth Configuration ---
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# --- Blueprint and Client Initialization ---
google_auth = Blueprint("google_auth", __name__)
client = WebApplicationClient(GOOGLE_CLIENT_ID) if GOOGLE_CLIENT_ID else None

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
    """Determines the correct OAuth2 redirect URI based on the environment."""
    env_redirect_uri = os.environ.get("GOOGLE_OAUTH_REDIRECT_URI")
    if env_redirect_uri: return env_redirect_uri
    render_external_url = os.environ.get("RENDER_EXTERNAL_URL")
    if render_external_url: return f"{render_external_url}/portal/google_login/callback"
    return "http://127.0.0.1:5000/portal/google_login/callback"

@google_auth.route("/google_login")
def login():
    if not client:
        flash("Google OAuth is not configured on the server.", "error")
        return redirect(url_for('job_portal_index'))

    google_provider_cfg = get_google_provider_cfg()
    if not google_provider_cfg or "authorization_endpoint" not in google_provider_cfg:
        flash("Could not connect to Google for authentication.", "error")
        return redirect(url_for("job_portal_index"))
        
    request_uri = client.prepare_request_uri(
        google_provider_cfg["authorization_endpoint"],
        redirect_uri=get_redirect_url(),
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@google_auth.route("/google_login/callback")
def callback():
    try:
        code = request.args.get("code")
        if not code:
            flash("Authentication failed: No authorization code received from Google.", "error")
            return redirect(url_for('job_portal_index'))

        # Exchange code for a token
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=get_redirect_url(),
            code=code
        )
        token_response = requests.post(
            token_url, headers=headers, data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET), timeout=10
        )
        token_response.raise_for_status()
        client.parse_request_body_response(json.dumps(token_response.json()))

        # Get user's profile information
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body, timeout=10)
        userinfo = userinfo_response.json()

        if not userinfo.get("email_verified"):
            flash("Your Google email is not verified.", "warning")
            return redirect(url_for('job_portal_index'))

        users_email = userinfo["email"].lower()
        users_name = userinfo.get("given_name") or userinfo.get("name", "New User")

        # --- Core Login/Registration Logic ---
        user = get_user_by_email(users_email)

        if user:
            # User exists. Check if their role needs to be updated to 'company'.
            if user.role != 'company' and is_company_email(users_email):
                logging.warning(f"Correcting role for existing user {users_email} to 'company'.")
                with get_db() as conn:
                    with conn.cursor() as cur:
                        cur.execute("UPDATE users SET role = 'company' WHERE id = %s", (user.id,))
                    # THE FIX IS HERE: conn.commit() is now INSIDE the 'with' block
                    conn.commit()
                user.role = 'company' # Update the in-memory object for this request
        else:
            # User does not exist, so create a new one.
            if is_company_email(users_email):
                logging.info(f"New whitelisted company user: {users_email}. Creating 'company' account.")
                user_id = create_user(email=users_email, password=None, role='company', full_name=users_name)
            else:
                logging.info(f"New candidate user: {users_email}. Creating 'pending_setup' account.")
                user_id = create_user(email=users_email, password=None, role='pending_setup', full_name=users_name)
                session['needs_registration_completion'] = True
            
            user = get_user_by_id(user_id)
            if not user:
                flash("There was an error creating your account. Please try again.", "error")
                return redirect(url_for('job_portal_index'))

        # Log in the user and set session variables
        login_user(user)
        session['google_id'] = userinfo.get("sub")
        session['google_name'] = user.full_name
        session['google_picture'] = userinfo.get("picture")

        flash(f'Welcome, {user.full_name or user.email}!', 'success')

        # Redirect based on their final role
        if user.role == 'admin':
            return redirect(url_for('admin_routes.dashboard'))
        elif user.role == 'company':
            return redirect(url_for('company_routes.dashboard'))
        elif user.role == 'candidate':
            return redirect(url_for('candidate_routes.dashboard'))
        elif user.role == 'pending_setup':
            return redirect(url_for('auth_routes.complete_registration'))
        
        return redirect(url_for('job_portal_index'))

    except Exception as e:
        logging.error(f"An error occurred in the Google OAuth callback: {e}", exc_info=True)
        flash("An unexpected error occurred during sign-in. Please try again.", "error")
        return redirect(url_for('job_portal_index'))

@google_auth.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('job_portal_index'))
