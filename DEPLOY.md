
# Deployment Guide

## 1. Environment Variables
Required environment variables:
- `DATABASE_URL`: PostgreSQL database connection string
- `GOOGLE_API_KEY`: Google API key for Gemini integration
- `SESSION_SECRET`: Secret key for Flask sessions
- `FLASK_SECRET_KEY`: Flask application secret key

## 2. Database Setup
The application uses PostgreSQL. Make sure your database is properly configured and the DATABASE_URL environment variable is set.

## 3. Static Files
All static files are served from:
- `/static`: CSS, JavaScript, and images
- `/uploads`: User uploaded files (CVs, ID cards, etc.)

## 4. Application Structure
- `main.py`: Main application entry point
- `app.py`: Core Flask application
- `english/`: English learning module
- `jobportal/`: Job portal module
- `templates/`: HTML templates
- `static/`: Static assets

## 5. Running the Application
Development:
```bash
python main.py
```

Production:
```bash
gunicorn --bind 0.0.0.0:5000 main:app
```

## 6. Troubleshooting
- Ensure all environment variables are set
- Check database connectivity
- Verify file permissions for uploads directory
- Monitor gunicorn logs for errors

