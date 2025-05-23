
# Under The Mango Tree - Customization Guide

## Adding New Subjects

1. Create a new template file in `/templates` folder (e.g., `new_subject.html`)
2. Add a new route in `app.py`
3. Update the subjects page

Example for adding a new subject:

```python
# In app.py
@app.route('/new-subject')
def new_subject():
    return render_template('new_subject.html')
```

```html
<!-- In templates/subjects.html -->
<div class="card mb-4 shadow-sm">
    <div class="card-body">
        <h2 class="card-title">
            <i class="fas fa-book text-primary me-2"></i>New Subject
        </h2>
        <p class="card-text">Description of the new subject</p>
        <div class="d-flex justify-content-between align-items-center">
            <div class="features">
                <span class="badge bg-primary me-2">Feature 1</span>
                <span class="badge bg-primary me-2">Feature 2</span>
            </div>
            <a href="{{ url_for('new_subject') }}" class="btn btn-primary">Start Learning</a>
        </div>
    </div>
</div>
```

## Customizing Team Section

The team section can be modified in two ways:

1. Direct HTML editing in `templates/team.html`
2. Using the database model (recommended)

To add/edit team members using the database:

```python
# Example using TeamMember model
from models import db, TeamMember

# Add new team member
new_member = TeamMember(
    name="New Member",
    title="Position Title",
    bio="Professional background and experience",
    photo_url="https://example.com/photo.jpg",
    email="member@example.com",
    order=1  # For controlling display order
)
db.session.add(new_member)
db.session.commit()
```

Image Requirements:
- Recommended size: 400x400px
- Format: JPG or PNG
- Max file size: 2MB

## File Structure
- `/templates` - All HTML templates
- `/static/css` - CSS files
- `/static/js` - JavaScript files
- `/static/images` - Image assets
