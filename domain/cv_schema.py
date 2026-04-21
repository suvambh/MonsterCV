def empty_contact():
    return {
        "email": "",
        "phone": "",
        "linkedin": "",
        "github": "",
    }

def empty_cv():
    return {
        "name": "",
        "title": "",
        "photo": "",
        "location": "",
        "summary": "",
        "contact": empty_contact(),
        "skills": [],
        "experience": [],
        "projects": [],
        "education": [],
        "certifications": [],
    }