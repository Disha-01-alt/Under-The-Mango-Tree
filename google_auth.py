# Google Authentication for Job Portal and Entire Platform
import json
import os
import requests
from flask import Blueprint, redirect, request, url_for, session, flash
from flask_login import login_user, logout_user, current_user
from oauthlib.oauth2 import WebApplicationClient
from database import get_user_by_email, create_user
from models import User

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

client = WebApplicationClient(GOOGLE_CLIENT_ID)
google_auth = Blueprint("google_auth", __name__)

@google_auth.route("/google_login")
def login():
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Dynamically generate redirect URI
    redirect_uri = url_for("google_auth.callback", _external=True, _scheme="https")

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=redirect_uri,
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@google_auth.route("/google_login/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Authorization code not found.", 400

    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]

    redirect_uri = url_for("google_auth.callback", _external=True, _scheme="https")

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url.replace("http://", "https://"),
        redirect_url=redirect_uri,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    userinfo = userinfo_response.json()

    if not userinfo.get("email_verified"):
        return "User email not available or not verified by Google.", 400

    # Extract user info
    unique_id = userinfo["sub"]
    users_email = userinfo["email"]
    users_name = userinfo["given_name"]
    picture = userinfo["picture"]

    existing_user = get_user_by_email(users_email)

    if existing_user:
        user = User(
            user_id=existing_user['id'],
            email=existing_user['email'],
            password_hash='',
            role=existing_user['role'],
            full_name=existing_user['full_name'],
            phone=existing_user['phone'],
            linkedin=existing_user['linkedin'],
            github=existing_user['github'],
            is_approved=existing_user['is_approved']
        )
        login_user(user)

        session['google_id'] = unique_id
        session['google_name'] = users_name
        session['google_picture'] = picture

        # Role-based redirection
        print(f"🔐 Logged in as {user.role}")
        if user.role == 'admin':
            return redirect(url_for('admin_routes.dashboard'))
        elif user.role == 'company':
            if user.is_approved:
                return redirect(url_for('company_routes.dashboard'))
            else:
                flash('Your company account is pending admin approval.', 'info')
                return redirect(url_for('index'))
        else:
            return redirect(url_for('candidate_routes.dashboard'))
    else:
        # New user
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
