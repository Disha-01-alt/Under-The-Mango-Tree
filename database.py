import psycopg2
import psycopg2.extras
import os
import logging
from contextlib import contextmanager

def get_db_connection():
    """Get database connection"""
    try:
        database_url = os.environ.get('DATABASE_URL')
        if database_url:
            conn = psycopg2.connect(database_url)
        else:
            conn = psycopg2.connect(
                host=os.environ.get('PGHOST'),
                database=os.environ.get('PGDATABASE'),
                user=os.environ.get('PGUSER'),
                password=os.environ.get('PGPASSWORD'),
                port=os.environ.get('PGPORT', 5432)
            )
        return conn
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        raise

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = None
    try:
        conn = get_db_connection()
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Database operation error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def init_db():
    """Initialize database tables"""
    with get_db() as conn:
        cur = conn.cursor()
        
        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL CHECK (role IN ('candidate', 'admin', 'company', 'pending_setup')),
                full_name VARCHAR(255),
                phone VARCHAR(20),
                linkedin VARCHAR(255),
                github VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_approved BOOLEAN DEFAULT TRUE
            )
        """)
        
        # Create candidate_profiles table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS candidate_profiles (
                user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                summary TEXT,
                cv_filename VARCHAR(255),
                id_card_filename VARCHAR(255),
                marksheet_filename VARCHAR(255),
                rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                admin_feedback TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ews_certificate_filename VARCHAR(255),
                college_name VARCHAR(255),
                degree VARCHAR(255),
                graduation_year INTEGER,
                core_interest_domains TEXT,
                twelfth_school_type VARCHAR(50),
                parental_annual_income VARCHAR(100),
                admin_tags TEXT,
                is_certified BOOLEAN DEFAULT FALSE,
                linkedin_data JSONB,
                cv_data JSONB,
                profile_status VARCHAR(50) 
            )
        """)
        
        # Create jobs table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                company VARCHAR(255) NOT NULL,
                location VARCHAR(255),
                description TEXT,
                requirements TEXT,
                salary_range VARCHAR(100),
                job_type VARCHAR(100),
                posted_by INTEGER REFERENCES users(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                linkedin_url TEXT,
                job_tags TEXT
            )
        """)
        
        # Create companies table for whitelisting
        cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                company_name VARCHAR(255) NOT NULL
            )
        """)
        
        # Create admin user(s)
        from werkzeug.security import generate_password_hash
        
        admin_accounts = [
            {'email': 'dishasahu786forstudy@gmail.com', 'name': 'System Administrator', 'password': 'admin123'},
            {'email': 'atmabodha@gmail.com', 'name': 'Operations Admin', 'password': 'admin123'}
        ]
        for admin in admin_accounts:
            admin_password_hash = generate_password_hash(admin['password'])
            # ON CONFLICT (email) DO NOTHING prevents errors if the admin already exists.
            cur.execute("""
                INSERT INTO users (email, password_hash, role, full_name, is_approved)
                VALUES (%s, %s, 'admin', %s, TRUE)
                ON CONFLICT (email) DO NOTHING
            """, (admin['email'].lower(), admin_password_hash, admin['name']))
        
        logging.info(f"Default admin accounts checked/populated.")

        # Pre-populate the companies table with default emails
        default_companies = [
            {'email': 'atmabodha@gmail.com', 'company_name': 'Tech Innovators'},
            {'email': 'contact.dishasahu@gmail.com', 'company_name': 'Solution Works'},
            {'email': 'careers@global-data.net', 'company_name': 'Global Data Inc.'}
        ]
        for company in default_companies:
            # ON CONFLICT (email) DO NOTHING ensures we don't get an error
            # if the email already exists. It will only insert new ones.
            cur.execute("""
                INSERT INTO companies (email, company_name)
                VALUES (%s, %s)
                ON CONFLICT (email) DO NOTHING
            """, (company['email'].lower(), company['company_name']))
        
        logging.info(f"Default company emails checked/populated.")
        
        conn.commit()
        logging.info("Database initialized successfully.")


def is_company_email(email):
    """Check if an email is in the whitelisted companies table."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM companies WHERE email = %s", (email.lower(),))
        return cur.fetchone() is not None

def create_user(email, password, role, full_name=None, phone=None, linkedin=None, github=None):
    from models import User
    password_hash = User.create_password_hash(password if password is not None else os.urandom(16).hex())
    is_approved_status = True
    
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (email, password_hash, role, full_name, phone, linkedin, github, is_approved)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (email, password_hash, role, full_name, phone, linkedin, github, is_approved_status))
        user_id = cur.fetchone()[0]
        conn.commit()
        return user_id

def get_user_by_email(email):
    """Get user by email"""
    with get_db() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = cur.fetchone()
        if row:
            from models import User
            return User(
                user_id=row['id'],
                email=row['email'],
                password_hash=row['password_hash'],
                role=row['role'],
                full_name=row['full_name'],
                phone=row['phone'],
                linkedin=row['linkedin'],
                github=row['github'],
                created_at=row['created_at'],
                is_approved=row['is_approved']
            )
        return None

def get_user_by_id(user_id):
    """Get user by ID"""
    with get_db() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        row = cur.fetchone()
        if row:
            from models import User
            return User(
                user_id=row['id'],
                email=row['email'],
                password_hash=row['password_hash'],
                role=row['role'],
                full_name=row['full_name'],
                phone=row['phone'],
                linkedin=row['linkedin'],
                github=row['github'],
                created_at=row['created_at'],
                is_approved=row['is_approved']
            )
        return None

def get_candidate_details_by_id(user_id):
    """Get comprehensive candidate details by user ID."""
    with get_db() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            SELECT u.*, cp.*
            FROM users u
            LEFT JOIN candidate_profiles cp ON u.id = cp.user_id
            WHERE u.id = %s AND u.role = 'candidate'
        """, (user_id,))
        row = cur.fetchone()
        return dict(row) if row else None

def get_candidate_profile(user_id):
    """Get candidate profile"""
    with get_db() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM candidate_profiles WHERE user_id = %s", (user_id,))
        row = cur.fetchone()
        if row:
            from models import CandidateProfile
            return CandidateProfile(**row)
        return None

def update_candidate_profile(user_id, **kwargs):
    """Update candidate profile"""
    if not kwargs:
        return
    with get_db() as conn:
        cur = conn.cursor()
        set_clauses = [f"{key} = %s" for key in kwargs]
        values = list(kwargs.values())
        set_clauses.append("updated_at = CURRENT_TIMESTAMP")
        values.append(user_id)
        query = f"UPDATE candidate_profiles SET {', '.join(set_clauses)} WHERE user_id = %s"
        cur.execute(query, values)
        conn.commit()

def get_all_jobs(**filters):
    """Get all jobs with optional filters"""
    with get_db() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "SELECT j.*, u.full_name as posted_by_name FROM jobs j LEFT JOIN users u ON j.posted_by = u.id WHERE 1=1"
        params = []
        # (Your filtering logic remains unchanged)
        query += " ORDER BY j.created_at DESC"
        cur.execute(query, tuple(params))
        jobs = []
        from models import Job
        for row in cur.fetchall():
            job_obj = Job(**row)
            job_obj.id = row['id'] # Ensure Job model gets the ID
            job_obj.posted_by_name = row['posted_by_name']
            jobs.append(job_obj)
        return jobs

def create_job(title, company, location, description, requirements, posted_by, salary_range=None, job_type=None, linkedin_url=None, job_tags=None):
    """Create a new job"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO jobs (title, company, location, description, requirements, salary_range, job_type, posted_by, linkedin_url, job_tags)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (title, company, location, description, requirements, salary_range, job_type, posted_by, linkedin_url, job_tags))
        job_id = cur.fetchone()[0]
        conn.commit()
        return job_id

def get_all_candidates():
    """Get all candidates with their profiles"""
    with get_db() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            SELECT u.*, cp.*
            FROM users u
            LEFT JOIN candidate_profiles cp ON u.id = cp.user_id
            WHERE u.role = 'candidate'
            ORDER BY u.created_at DESC
        """)
        return [dict(row) for row in cur.fetchall()]

def update_user_details(user_id, **kwargs):
    """Updates specific details for a user."""
    if not kwargs:
        return
    with get_db() as conn:
        cur = conn.cursor()
        set_clauses = [f"{key} = %s" for key in kwargs]
        values = list(kwargs.values())
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(set_clauses)} WHERE id = %s"
        cur.execute(query, tuple(values))
        conn.commit()

def update_candidate_rating_feedback(user_id, **kwargs):
    """Update candidate rating, feedback, tags, etc."""
    if not kwargs:
        return
    with get_db() as conn:
        cur = conn.cursor()
        set_clauses = [f"{key} = %s" for key in kwargs]
        values = list(kwargs.values())
        set_clauses.append("updated_at = CURRENT_TIMESTAMP")
        values.append(user_id)
        query = f"UPDATE candidate_profiles SET {', '.join(set_clauses)} WHERE user_id = %s"
        cur.execute(query, tuple(values))
        conn.commit()

def search_candidates(**filters):
    """Search candidates with filters"""
    with get_db() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = """
            SELECT u.*, cp.*
            FROM users u
            LEFT JOIN candidate_profiles cp ON u.id = cp.user_id
            WHERE u.role = 'candidate' AND u.is_approved = TRUE
        """
        params = []
        # (Your filtering logic remains unchanged)
        query += " ORDER BY cp.rating DESC NULLS LAST, u.created_at DESC"
        cur.execute(query, tuple(params))
        return [dict(row) for row in cur.fetchall()]

def get_all_companies():
    """Get all users with the 'company' role."""
    with get_db() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM users WHERE role = 'company' ORDER BY created_at DESC")
        return cur.fetchall()

def get_pending_companies():
    """Get all companies waiting for approval"""
    with get_db() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM users WHERE role = 'company' AND is_approved = false ORDER BY created_at DESC")
        return [dict(row) for row in cur.fetchall()]

def approve_company(company_id):
    """Approve a company account"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET is_approved = true WHERE id = %s AND role = 'company'", (company_id,))
        conn.commit()
        return cur.rowcount > 0

def delete_job(job_id):
    """Delete a job"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM jobs WHERE id = %s", (job_id,))
        conn.commit()

def get_job_by_id(job_id):
    """Get job by ID"""
    with get_db() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
        row = cur.fetchone()
        if row:
            from models import Job
            return Job(**row)
        return None

def update_job(job_id, **kwargs):
    """Update job"""
    if not kwargs:
        return
    with get_db() as conn:
        cur = conn.cursor()
        set_clauses = [f"{key} = %s" for key in kwargs]
        values = list(kwargs.values())
        values.append(job_id)
        query = f"UPDATE jobs SET {', '.join(set_clauses)} WHERE id = %s"
        cur.execute(query, values)
        conn.commit()
