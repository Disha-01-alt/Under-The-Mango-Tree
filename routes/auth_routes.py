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

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        # If user is already logged in, no need to show registration.
        # Redirect them to a sensible page.
        flash("You are already logged in.", "info")
        if current_user.role == 'pending_setup' or session.get('needs_registration_completion'):
            return redirect(url_for('auth_routes.complete_registration'))
        elif current_user.role == 'candidate':
            return redirect(url_for('candidate_routes.dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin_routes.dashboard'))
        elif current_user.role == 'company':
            return redirect(url_for('company_routes.dashboard'))
        return redirect(url_for('index'))

    # Get the pre-selected role from the query parameter for GET requests
    pre_selected_role = request.args.get('role', None) # e.g., 'candidate' or 'company'

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role_from_form = request.form.get('role', '') # Role selected in the form
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip() or None
        linkedin = request.form.get('linkedin', '').strip() or None
        github = request.form.get('github', '').strip() or None
        
        errors = []
        if not all([email, password, confirm_password, role_from_form, full_name]):
            errors.append('Please fill in all required fields (*).')
        if password != confirm_password:
            errors.append('Passwords do not match.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters long.')
        if role_from_form not in ['candidate', 'company']: # Validate role from form
            errors.append('Invalid role selected in the form.')
        
        if not errors:
            existing_user = get_user_by_email(email)
            if existing_user:
                errors.append('An account with this email already exists. Please login or use a different email.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            # Pass pre_selected_role again for GET part of template if POST fails
            return render_template('job_portal/auth/register.html', form_data=request.form, pre_selected_role=role_from_form or pre_selected_role) 
        
        try:
            user_id = create_user(
                email=email, password=password, role=role_from_form, full_name=full_name,
                phone=phone, linkedin=linkedin, github=github
            )
            logging.info(f"Manual registration successful for {email}, role: {role_from_form}, user_id: {user_id}")
            
            # Attempt to auto-login the user
            newly_registered_user = get_user_by_id(user_id)
            if newly_registered_user:
                login_user(newly_registered_user)
                flash('Account created and you are now logged in!', 'success')
                if newly_registered_user.role == 'company' and not newly_registered_user.is_approved:
                    flash('Your company account is pending admin approval.', 'info')
                    return redirect(url_for('index')) # Or a company pending page
                elif newly_registered_user.role == 'candidate':
                    return redirect(url_for('candidate_routes.dashboard'))
                # Add other role redirects if they could register as such manually
                return redirect(url_for('index')) # Fallback
            else:
                flash('Account created, but auto-login failed. Please try logging in.', 'warning')
                return redirect(url_for('google_auth.login')) # Or a manual login if you have one
            
        except Exception as e:
            logging.exception(f"Error during manual registration for {email}:")
            flash('An error occurred during registration. Please try again.', 'error')
            return render_template('job_portal/auth/register.html', form_data=request.form, pre_selected_role=role_from_form or pre_selected_role)

    # For GET request, pass the pre_selected_role to the template
    return render_template('job_portal/auth/register.html', pre_selected_role=pre_selected_role)


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
