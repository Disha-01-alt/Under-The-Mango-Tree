# google_auth.py
import json
import os
import requests
from flask import Blueprint, redirect, request, url_for, session, flash
from flask_login import login_user, logout_user # current_user (not used here)
from oauthlib.oauth2 import WebApplicationClient
from database import get_user_by_email, create_user # Assuming these are correct
from models import User # Assuming this is correct

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

client = WebApplicationClient(GOOGLE_CLIENT_ID)
google_auth = Blueprint("google_auth", __name__)

# (Your instructional print statement can stay or go, it doesn't affect this)

@google_auth.route("/google_login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Construct the redirect_uri
    # This is the line we are interested in!
    actual_redirect_uri_sent_to_google = request.base_url.replace("http://", "https://") + "/callback"

    # ======================================================================
    # SIMPLE DEBUG: PRINT THE URI TO THE LOGS
    # ======================================================================
    print("--------------------------------------------------------------------")
    print(f"DEBUG: The redirect_uri my Flask app is about to send to Google is:")
    print(f"'{actual_redirect_uri_sent_to_google}'")
    print(f"(Compare this EXACT string with your Google Cloud Console URIs)")
    print("--------------------------------------------------------------------")
    # ======================================================================

    # Use library to construct the request for Google login
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=actual_redirect_uri_sent_to_google, # Use the URI we just printed
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@google_auth.route("/google_login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # --- Start: Simple print for callback redirect_url (for token exchange) ---
    # This must match the URI sent in the login step (the one printed above)
    # AND one of the URIs in Google Cloud Console.
    redirect_url_for_token_exchange = request.base_url.replace("http://", "https://")
    print("--------------------------------------------------------------------")
    print(f"DEBUG: In CALLBACK, the redirect_url being used for TOKEN EXCHANGE is:")
    print(f"'{redirect_url_for_token_exchange}'")
    print("--------------------------------------------------------------------")
    # --- End: Simple print ---


    # Find out what URL to hit to get tokens
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url.replace("http://", "https://"),
        redirect_url=redirect_url_for_token_exchange, # Use the one we just printed
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Check for token exchange error (simplified for now)
    if not token_response.ok:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"ERROR: Token exchange failed! Status: {token_response.status_code}")
        print(f"Response: {token_response.text}")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        flash("Error during Google sign-in (token exchange). Please try again.", "error")
        return redirect(url_for('index')) # Or your main/login page

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # ... (rest of your callback function for fetching userinfo, etc.)
    # (Keep your existing userinfo fetching and user handling logic here)

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if not userinfo_response.ok:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(f"ERROR: Fetching userinfo failed! Status: {userinfo_response.status_code}")
        print(f"Response: {userinfo_response.text}")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        flash("Error during Google sign-in (userinfo). Please try again.", "error")
        return redirect(url_for('index'))

    userinfo = userinfo_response.json()
    if userinfo.get("email_verified"):
        unique_id = userinfo["sub"]
        users_email = userinfo["email"]
        users_name = userinfo["given_name"]
        picture = userinfo["picture"]
    else:
        flash("User email not available or not verified by Google.", "error")
        return redirect(url_for('index')) # Or your login page

    existing_user = get_user_by_email(users_email)
    
    if existing_user:
        user = User(
            user_id=existing_user['id'],
            email=existing_user['email'],
            password_hash='',
            role=existing_user['role'],
            full_name=existing_user.get('full_name', users_name), # Use Google name as fallback
            phone=existing_user.get('phone'),
            linkedin=existing_user.get('linkedin'),
            github=existing_user.get('github'),
            is_approved=existing_user.get('is_approved', False)
        )
        login_user(user)
        
        session['google_id'] = unique_id
        session['google_name'] = users_name
        session['google_picture'] = picture
        
        if user.role == 'admin':
            return redirect(url_for('admin_routes.dashboard'))
        elif user.role == 'company':
            if user.is_approved:
                return redirect(url_for('company_routes.dashboard'))
            else:
                flash('Your company account is pending admin approval.', 'info')
                return redirect(url_for('index'))
        else: # candidate
            return redirect(url_for('candidate_routes.dashboard'))
    else:
        session['google_id'] = unique_id
        session['google_email'] = users_email
        session['google_name'] = users_name
        session['google_picture'] = picture
        session['pending_registration'] = True
        
        return redirect(url_for('auth_routes.complete_registration'))


@google_auth.route("/logout")
def logout():
    logout_user()
    session.pop('google_id', None)
    session.pop('google_email', None)
    session.pop('google_name', None)
    session.pop('google_picture', None)
    session.pop('pending_registration', None)
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))
