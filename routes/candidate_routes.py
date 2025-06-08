# Job-Portal-master/routes/candidate_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from database import get_candidate_profile, update_candidate_profile, get_all_jobs, update_user_details
import os
import logging
import re
import cloudinary
import cloudinary.uploader
from threading import Thread

# Import background task runners
from background_tasks import run_linkedin_scrape, run_cv_parse

candidate_bp = Blueprint('candidate_routes', __name__)

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@candidate_bp.before_request
@login_required 
def candidate_blueprint_checks():
    # Allow anyone authenticated (even pending_setup) to browse jobs
    if request.endpoint == 'candidate_routes.jobs':
        logging.debug(f"User {current_user.email} accessing endpoint {request.endpoint}. Allowing.")
        return 

    # If user needs to complete setup, force them to the completion page
    if current_user.role == 'pending_setup' or session.get('needs_registration_completion'):
        flash('Please complete your registration to access this feature.', 'info')
        return redirect(url_for('auth_routes.complete_registration'))
    
    # If role is not candidate, deny access
    if current_user.role != 'candidate':
        logging.warning(f"Access denied for user {current_user.email} (role: {current_user.role}) to {request.endpoint}.")
        flash('Access denied. This area is for candidates only.', 'error')
        # Redirect based on actual role
        if current_user.role == 'admin': return redirect(url_for('admin_routes.dashboard'))
        if current_user.role == 'company': return redirect(url_for('company_routes.dashboard'))
        return redirect(url_for('job_portal_index'))
    
    logging.debug(f"User {current_user.email} (role: {current_user.role}) accessing {request.endpoint}. Candidate check passed.")

@candidate_bp.route('/dashboard')
def dashboard():
    try:
        profile = get_candidate_profile(current_user.id)
        return render_template('job_portal/candidate/dashboard.html', profile=profile)
    except Exception as e:
        logging.exception(f"Error loading candidate dashboard for user {current_user.id}:")
        flash('Error loading dashboard. Please try again.', 'error')
        return redirect(url_for('job_portal_index'))

@candidate_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    available_core_interests = [
        "Frontend Development", "Backend Development", "Full-Stack Development",
        "Data Engineering", "Data Analytics", "Data Science & Machine Learning",
        "Prompt Engineering", "Deep Learning & AI"
    ]
    profile_db_data = get_candidate_profile(current_user.id)

    # In routes/candidate_routes.py, inside the profile() function

    if request.method == 'POST':
        logging.debug(f"POST to /candidate/profile. Form: {request.form}, Files: {request.files}")
        
        form_errors = []
        user_update_payload = {}
        profile_update_payload = {}
        user_details_changed = False

        # --- User Details Validation (from `users` table) ---
        new_whatsapp_number = request.form.get('whatsapp_number', '').strip()
        if not new_whatsapp_number: 
            form_errors.append("WhatsApp Number is required.")
        elif not re.fullmatch(r"^(?:\+91|91|0)?[6789]\d{9}$", new_whatsapp_number):
            form_errors.append("Invalid WhatsApp Number. Use a 10-digit Indian number, optionally with +91/91/0 prefix.")
        elif new_whatsapp_number != (current_user.phone or ''):
            user_update_payload['phone'] = new_whatsapp_number
            user_details_changed = True
        
        new_linkedin = request.form.get('linkedin', '').strip()
        if new_linkedin != (current_user.linkedin or ''):
            user_update_payload['linkedin'] = new_linkedin
            user_details_changed = True
        
        new_github = request.form.get('github', '').strip()     
        if new_github != (current_user.github or ''):
            user_update_payload['github'] = new_github
            user_details_changed = True

        # --- Profile Details Validation (from `candidate_profiles` table) ---
        profile_update_payload['summary'] = request.form.get('summary', '').strip()
        profile_update_payload['college_name'] = request.form.get('college_name', '').strip()
        profile_update_payload['degree'] = request.form.get('degree', '').strip()
        grad_year_str = request.form.get('graduation_year', '').strip()
        core_interests_list = request.form.getlist('core_interest_domains')
        profile_update_payload['core_interest_domains'] = ','.join(core_interests_list) if core_interests_list else None
        profile_update_payload['twelfth_school_type'] = request.form.get('twelfth_school_type')
        profile_update_payload['parental_annual_income'] = request.form.get('parental_annual_income')
        
        if not profile_update_payload['summary']: form_errors.append("Summary of Skills and Strengths is required.")
        if not profile_update_payload['college_name']: form_errors.append("College Name is required.")
        if not profile_update_payload['degree']: form_errors.append("Degree is required.")
        if not grad_year_str: form_errors.append("Graduation Year is required.")
        elif not grad_year_str.isdigit() or not (1950 <= int(grad_year_str) <= 2050):
            form_errors.append("Invalid Graduation Year.")
        else:
             profile_update_payload['graduation_year'] = int(grad_year_str)
        if not core_interests_list: form_errors.append("Please select at least one Core Interest Domain.")
        if not profile_update_payload['twelfth_school_type']: form_errors.append("12th School Type is required.")
        if not profile_update_payload['parental_annual_income']: form_errors.append("Parental Annual Income is required.")


        # --- File Upload Logic ---
        files_to_process_cloudinary = {
            'cv': {'folder': f'job_portal/user_{current_user.id}/cvs', 'db_field': 'cv_filename', 'label': 'CV/Resume', 'is_required': True},
            'id_card': {'folder': f'job_portal/user_{current_user.id}/id_cards', 'db_field': 'id_card_filename', 'label': 'ID Card', 'is_required': True},
            'marksheet': {'folder': f'job_portal/user_{current_user.id}/marksheets', 'db_field': 'marksheet_filename', 'label': '12th Marksheet', 'is_required': True},
            'ews_certificate': {'folder': f'job_portal/user_{current_user.id}/ews_certificates', 'db_field': 'ews_certificate_filename', 'label': 'EWS Certificate', 'is_required': False}
        }

        for form_field_name, config in files_to_process_cloudinary.items():
            file = request.files.get(form_field_name)
            existing_file_url = getattr(profile_db_data, config['db_field'], None) if profile_db_data else None
            
            if file and file.filename:
                if file.filename.lower().endswith('.pdf'):
                    try:
                        public_id_base = os.path.splitext(secure_filename(file.filename))[0]
                        public_id = f"{current_user.id}_{form_field_name}_{public_id_base[:50]}" 
                        upload_result = cloudinary.uploader.upload(
                            file, folder=config['folder'], public_id=public_id, resource_type="raw", overwrite=True
                        )
                        profile_update_payload[config['db_field']] = upload_result['secure_url']
                        logging.info(f"Uploaded {config['label']} to Cloudinary: {upload_result['secure_url']}")
                    except Exception as e:
                        logging.error(f"Cloudinary upload error for {config['label']}: {e}")
                        form_errors.append(f"Error uploading {config['label']}.")
                else:
                    form_errors.append(f"{config['label']} must be a PDF file.")
            elif config['is_required'] and not existing_file_url:
                form_errors.append(f"{config['label']} is required.")


        if form_errors:
            for error_msg in form_errors: flash(error_msg, 'error')
            return render_template('job_portal/candidate/profile.html',
                                 profile=profile_db_data, form_data_attempt=request.form.to_dict(), 
                                 selected_core_interests=core_interests_list,
                                 available_core_interests=available_core_interests)

        # --- CORRECTED DATABASE UPDATE AND BACKGROUND TASK TRIGGERING ---

        # 1. Update the database with all collected changes first.
        # This handles all text fields for both `users` and `candidate_profiles` tables.
        if user_details_changed:
            update_user_details(current_user.id, **user_update_payload)
        
        # This update includes the new Cloudinary file URLs.
        update_candidate_profile(current_user.id, **profile_update_payload)
        
        
        # 2. Trigger Background Tasks based on the final state of the data.
        
       # Trigger CV parsing if a new CV was uploaded in this request.
        # Check the payload we prepared for the database update.
        new_cv_url = profile_update_payload.get('cv_filename')
        if new_cv_url:
            try:
                # Pass the Cloudinary URL directly to the background task
                run_cv_parse(current_user.id, new_cv_url)
                flash('Your new CV is being processed from the cloud.', 'info')
            except Exception as e:
                logging.error(f"Error triggering background CV processing: {e}")
                flash('Could not start CV processing. Please try uploading again.', 'error')


        # Get the final state of the LinkedIn URL after potential updates.
        final_linkedin_url = user_update_payload.get('linkedin', current_user.linkedin)
        
        # Determine if a scrape should be triggered.
        should_scrape = (
            final_linkedin_url and 
            ('linkedin' in user_update_payload or not profile_db_data or not profile_db_data.linkedin_data)
        )

        if should_scrape:
            run_linkedin_scrape(current_user.id, final_linkedin_url)
            flash('Your LinkedIn profile is being analyzed in the background. This may take a few minutes.', 'info')
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('candidate_routes.profile'))

    # --- GET Request (This part remains unchanged) ---
    selected_core_interests_on_get = []
    if profile_db_data and profile_db_data.core_interest_domains:
        selected_core_interests_on_get = [interest.strip() for interest in profile_db_data.core_interest_domains.split(',')]
    
    return render_template('job_portal/candidate/profile.html', 
                        profile=profile_db_data, 
                        selected_core_interests=selected_core_interests_on_get,
                        available_core_interests=available_core_interests,
                        form_data_attempt=None)
@candidate_bp.route('/jobs')
def jobs():
    logging.info(f"Accessing /candidate/jobs by user: {current_user.email if current_user.is_authenticated else 'Guest'}")
    try: 
        location_filter = request.args.get('location_filter', '').strip()
        work_model_filter = request.args.get('work_model_filter', '').strip()
        date_posted_filter = request.args.get('date_posted_filter', '').strip()
        company_filter = request.args.get('company_filter', '').strip()
        job_function_filter = request.args.get('job_function_filter', '').strip()

        jobs_list = get_all_jobs(
            location_filter=location_filter or None,
            work_model_filter=work_model_filter or None,
            date_posted_filter=date_posted_filter or None,
            company_filter=company_filter or None,
            job_function_filter=job_function_filter or None
        )
        
        return render_template('job_portal/candidate/jobs.html', 
                            jobs=jobs_list,
                            search_filters={
                                'location': location_filter,
                                'work_model': work_model_filter,
                                'date_posted': date_posted_filter,
                                'company': company_filter,
                                'job_function': job_function_filter
                            })
    except Exception as e:
        logging.exception("Error loading jobs page for user:") 
        flash('Error loading job listings. Please try again.', 'error')
        return redirect(url_for('job_portal_index'))
