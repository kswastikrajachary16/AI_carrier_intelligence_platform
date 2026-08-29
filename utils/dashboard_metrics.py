import re


def calculate_skill_score(matched_skills, missing_skills):
    total = len(matched_skills) + len(missing_skills)

    if total == 0:
        return 0

    return round((len(matched_skills) / total) * 100)


def calculate_project_score(text):

    text = text.lower()

    project_count = 0

    # Count occurrences of the word "project"
    project_count += len(
        re.findall(r"\bproject[s]?\b", text)
    )

    # Ignore the section heading itself
    if project_count > 0:
        project_count -= 1

    if project_count <= 0:
        return 0

    elif project_count == 1:
        return 35

    elif project_count == 2:
        return 65

    elif project_count == 3:
        return 85

    else:
        return 100

def calculate_resume_completeness(text):

    sections = [
        "summary",
        "education",
        "skills",
        "projects",
        "experience"
    ]

    found = 0

    lower = text.lower()

    for section in sections:

        if section in lower:
            found += 1

    return round((found / len(sections)) * 100)