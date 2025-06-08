# Job-Portal-master/cv_parser.py
import fitz  # PyMuPDF
import re
import json

# Map section headers to standardized keys
SECTION_ALIASES = {
    "education": ["education", "academics", "academic background", "education and training"],
    "skills": ["technical skills", "skills", "technologies", "proficiencies"],
    "experience": ["experience", "work experience", "professional experience", "employment"],
    "projects": ["projects", "academic projects", "personal projects"],
    "certifications": ["certifications", "licenses", "achievements"],
    "interests": ["interests", "hobbies", "activities"],
    "accomplishments": ["accomplishments", "honors", "awards", "recognitions"]
}

def _extract_text_from_pdf(pdf_source):
    """
    Extracts all text from a PDF source, which can be a file path,
    a bytes object, or a file-like object.
    """
    # This now correctly uses the 'pdf_source' argument
    doc = fitz.open(stream=pdf_source, filetype="pdf")
    return "\n".join([page.get_text() for page in doc])

def _map_section_name(line):
    """Maps a line of text to a canonical section name if it's a header."""
    line_clean = line.strip().lower()
    if len(line_clean.split()) < 4:
        for canonical, aliases in SECTION_ALIASES.items():
            for alias in aliases:
                if alias in line_clean:
                    return canonical
    return None

def _split_sections(text):
    """Splits the resume text into a dictionary of sections."""
    sections = {}
    current_section = "about"
    sections[current_section] = []
    
    for line in text.splitlines():
        line_clean = line.strip()
        if not line_clean:
            continue
        
        section_name = _map_section_name(line_clean)
        
        if section_name and section_name != current_section:
            current_section = section_name
            if current_section not in sections:
                sections[current_section] = []
        else:
            sections[current_section].append(line_clean)
            
    return {k: "\n".join(v).strip() for k, v in sections.items() if v}

def _extract_contact_info(text):
    """Extracts contact information from the text."""
    email = re.search(r"\b[\w.-]+@[\w.-]+\.\w+\b", text)
    phone = re.search(r"(\+?\d[\d\s-]{8,}\d)", text)
    websites = re.findall(r'https?://[^\s,]+', text)
    linkedin = next((url for url in websites if 'linkedin.com' in url), None)
    
    return {
        "email": email.group() if email else None,
        "phone": phone.group(1).strip() if phone else None,
        "linkedin": linkedin,
        "other_websites": [url for url in websites if url != linkedin]
    }

def parse_cv_to_json(pdf_source): # <-- Argument name changed here
    """
    Main function to parse a resume PDF to a structured JSON object.
    Accepts a file path or bytes content.
    """
    text = _extract_text_from_pdf(pdf_source) # <-- Correctly passing the variable now
    lines = text.splitlines()
    name = lines[0].strip() if lines else "Unknown"
    
    sections = _split_sections(text)
    contact_info = _extract_contact_info(text)
    
    experience_text = sections.get("experience", "")
    education_text = sections.get("education", "")
    skills_text = sections.get("skills", "")
    
    resume_json = {
        "name": name,
        "contact": contact_info,
        "about": sections.get("about", "").replace(name, "", 1).strip(),
        "experience": experience_text.split('\n'),
        "education": education_text.split('\n'),
        "skills": [s.strip() for s in re.split(r',|\n|•', skills_text) if s.strip()],
        "projects": sections.get("projects", "").split('\n'),
        "certifications": sections.get("certifications", "").split('\n'),
        "accomplishments": sections.get("accomplishments", "").split('\n'),
        "interests": sections.get("interests", "").split('\n'),
    }

    return resume_json
