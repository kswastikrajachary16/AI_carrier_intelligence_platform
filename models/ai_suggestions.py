def generate_ai_suggestions(
    score,
    missing_skills,
    text
):

    suggestions = []

    # Resume Length
    if len(text.split()) < 250:
        suggestions.append(
            "Increase your resume length to at least one page."
        )

    # Missing Skills
    for skill in missing_skills:
        suggestions.append(
            f"Learn {skill.title()} to improve your job match."
        )

    # GitHub
    if "github" not in text.lower():
        suggestions.append(
            "Add your GitHub profile link."
        )

    # LinkedIn
    if "linkedin" not in text.lower():
        suggestions.append(
            "Add your LinkedIn profile."
        )

    # ATS
    if score < 80:
        suggestions.append(
            "Improve ATS score by adding more relevant projects and skills."
        )

    # Projects
    if "project" not in text.lower():
        suggestions.append(
            "Include at least two technical projects."
        )

    return suggestions