# jobportal/routes/auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user,login_required # current_user might be used for conditional rendering
from database import get_user_by_email, create_user, get_user_by_id, get_db # Ensure get_user_by_id is available
from models import User 
import logging

auth_bp = Blueprint('auth_routes', __name__)

# This /login route is for a potential manual email/password login form.
# If you are ONLY using Google Sign-In, this route might not be directly used by users,
# but Flask-Login needs a login_view. It can simply redirect to Google login.
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # Redirect based on role if already logged in
        if current_user.role == 'candidate': return redirect(url_for('candidate_routes.dashboard'))
        if current_user.role == 'admin': return redirect(url_for('admin_routes.dashboard'))
        if current_user.role == 'company': return redirect(url_for('company_routes.dashboard'))
        return redirect(url_for('index'))
    
    # For now, if someone hits /auth/login, guide them to Google Sign-In
    flash("Please use Google Sign-In to access your account.", "info")
    return redirect(url_for('google_auth.login'))

    # If you were to implement manual login:
    # if request.method == 'POST':
    #     email = request.form.get('email', '').strip().lower()
    #     password = request.form.get('password', '')
    #     # ... (manual password checking logic) ...
    # return render_template('job_portal/auth/login.html') # A page with manual login form
# jobportal/routes/auth_routes.py
# ...
@auth_bp.route('/complete_registration', methods=['GET', 'POST'])
@login_required # User should already be logged in (as 'pending_setup') to reach here
def complete_registration():
    # Check if user truly needs to complete registration
    if not session.get('needs_registration_completion') and current_user.role != 'pending_setup':
        flash('Your registration is already complete.', 'info')
        # Redirect to their actual dashboard based on their now-final role
        if current_user.role == 'candidate': return redirect(url_for('candidate_routes.dashboard'))
        if current_user.role == 'admin': return redirect(url_for('admin_routes.dashboard')) # Unlikely admin needs this
        if current_user.role == 'company': return redirect(url_for('company_routes.dashboard'))
        return redirect(url_for('index'))

    user_to_update = current_user # They are already logged in

    if request.method == 'POST':
        new_role = request.form.get('role')
        full_name_form = request.form.get('full_name', '').strip()
        # Use submitted name if provided, otherwise keep existing (which might be from Google)
        full_name_to_save = full_name_form if full_name_form else user_to_update.full_name
        
        phone_to_save = request.form.get('phone', '').strip() or None
        linkedin_to_save = request.form.get('linkedin', '').strip() or None
        github_to_save = request.form.get('github', '').strip() or None
        
        if not new_role or new_role not in ['candidate', 'company']:
            flash('Please select a valid role (Candidate or Company).', 'error')
            return render_template('job_portal/auth/complete_registration.html', 
                                 current_user_name=user_to_update.full_name, # Pass current name
                                 current_user_email=user_to_update.email,  # Pass current email
                                 form_data=request.form)
        
        try:
            # Update the user's role and other details in the database
            with get_db() as conn: # Assumes get_db is available from database.py
                cur = conn.cursor()
                is_company_approved = False if new_role == 'company' else True # Companies start unapproved
                cur.execute("""
                    UPDATE users 
                    SET role = %s, full_name = %s, phone = %s, linkedin = %s, github = %s, is_approved = %s
                    WHERE id = %s
                """, (new_role, full_name_to_save, phone_to_save, linkedin_to_save, github_to_save, is_company_approved, user_to_update.id))
                
                # If they chose 'candidate', ensure their candidate_profile record exists
                if new_role == 'candidate':
                    cur.execute("""
                        INSERT INTO candidate_profiles (user_id) VALUES (%s)
                        ON CONFLICT (user_id) DO NOTHING;
                    """, (user_to_update.id,))
                conn.commit()

            # Update the current_user object in session
            user_to_update.role = new_role
            user_to_update.full_name = full_name_to_save
            user_to_update.phone = phone_to_save
            user_to_update.linkedin = linkedin_to_save
            user_to_update.github = github_to_save
            user_to_update.is_approved = is_company_approved
            
            session.pop('needs_registration_completion', None) # Clear the flag
            
            if new_role == 'company' and not is_company_approved:
                flash('Registration complete! Your company account is pending admin approval.', 'info')
                return redirect(url_for('index')) 
            else: # Candidate or approved company
                flash('Registration complete! Your account is fully active.', 'success')
                if new_role == 'candidate': return redirect(url_for('candidate_routes.dashboard'))
                if new_role == 'company': return redirect(url_for('company_routes.dashboard'))
                
        except Exception as e:
            logging.exception(f"Error updating user during complete_registration for {user_to_update.email}:")
            flash(f'Error finalizing your account: {str(e)}. Please try again.', 'error')
            # Fall through to render GET template
                                 
    # GET request
    return render_template('job_portal/auth/complete_registration.html', 
                         current_user_name=user_to_update.full_name, # Pre-fill name
                         current_user_email=user_to_update.email)   # For display
# ...
