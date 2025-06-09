# jobportal/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin):
    def __init__(self, id, email, password_hash, role, full_name=None, 
                 phone=None, linkedin=None, github=None, created_at=None, 
                 is_approved=True):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.full_name = full_name
        self.phone = phone
        self.linkedin = linkedin
        self.github = github
        self.created_at = created_at or datetime.now()
        self.is_approved = is_approved

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def create_password_hash(password):
        return generate_password_hash(password)

class CandidateProfile:
    def __init__(self, user_id, summary=None, cv_filename=None, id_card_filename=None, 
                 marksheet_filename=None, rating=None, admin_feedback=None,
                 updated_at=None,
                 ews_certificate_filename=None,
                 college_name=None,
                 degree=None,
                 graduation_year=None,
                 core_interest_domains=None,
                 twelfth_school_type=None,
                 parental_annual_income=None,
                 admin_tags=None,
                 is_certified=False,
                 profile_status=None,
                 linkedin_data=None,
                 cv_data=None,
                 # Adding created_at with a default of None to handle older data that might not have it
                 created_at=None
                 ):
        self.user_id = user_id
        self.summary = summary
        self.cv_filename = cv_filename
        self.id_card_filename = id_card_filename
        self.marksheet_filename = marksheet_filename
        self.rating = rating
        self.admin_feedback = admin_feedback
        self.updated_at = updated_at or datetime.now()
        self.ews_certificate_filename = ews_certificate_filename
        self.college_name = college_name
        self.degree = degree
        self.graduation_year = graduation_year
        self.core_interest_domains = core_interest_domains
        self.twelfth_school_type = twelfth_school_type
        self.parental_annual_income = parental_annual_income
        self.admin_tags = admin_tags
        self.is_certified = is_certified
        self.profile_status = profile_status
        self.linkedin_data = linkedin_data
        self.cv_data = cv_data

class Job:
    # THE FIX IS HERE: The first argument is 'id', not 'job_id'.
    def __init__(self, id, title, company, location, description, 
                 requirements, salary_range=None, job_type=None, 
                 posted_by=None, created_at=None, linkedin_url=None,
                 job_tags=None):
        # AND THE FIX IS HERE: self.id is assigned from the 'id' parameter.
        self.id = id
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.requirements = requirements
        self.salary_range = salary_range
        self.job_type = job_type
        self.posted_by = posted_by
        self.created_at = created_at or datetime.now()
        self.linkedin_url = linkedin_url
        self.job_tags = job_tags
