import re


def calculate_ats_score(
    name,
    email,
    phone,
    skills,
    text,
    target_role
):

    score = 0
    feedback = []
    breakdown = {}

    text_lower = text.lower()
    words = len(text.split())

    # -------------------------
    # Contact Information (10)
    # -------------------------

    contact = 0

    if name != "Not Found":
        contact += 4
    else:
        feedback.append("Add your full name.")

    if email != "Not Found":
        contact += 3
    else:
        feedback.append("Add a professional email address.")

    if phone != "Not Found":
        contact += 3
    else:
        feedback.append("Add your phone number.")

    breakdown["Contact Information"] = contact
    score += contact

    # -------------------------
    # Skills (20)
    # -------------------------

    skill_count = len(skills)

    if skill_count >= 12:
        skill_score = 20

    elif skill_count >= 9:
        skill_score = 17

    elif skill_count >= 6:
        skill_score = 14

    elif skill_count >= 4:
        skill_score = 10
        feedback.append("Add more technical skills.")

    else:
        skill_score = 5
        feedback.append("Your resume has very few technical skills.")

    breakdown["Skills"] = skill_score
    score += skill_score

    # -------------------------
    # Education (10)
    # -------------------------

    education_keywords = [
        "education",
        "college",
        "university",
        "bca",
        "mca",
        "b.tech",
        "btech",
        "degree",
        "cgpa"
    ]

    education_score = 10 if any(
        word in text_lower
        for word in education_keywords
    ) else 0

    if education_score == 0:
        feedback.append("Education section missing.")

    breakdown["Education"] = education_score
    score += education_score

    # -------------------------
    # Projects (15)
    # -------------------------

    project_matches = len(
        re.findall(
            r"\bproject[s]?\b",
            text_lower
        )
    )

    if project_matches >= 3:
        project_score = 15

    elif project_matches == 2:
        project_score = 12

    elif project_matches == 1:
        project_score = 8
        feedback.append("Add another project to strengthen your resume.")

    else:
        project_score = 0
        feedback.append("Projects section missing.")

    breakdown["Projects"] = project_score
    score += project_score

    # -------------------------
    # Experience (10)
    # -------------------------

    experience_keywords = [
        "experience",
        "internship",
        "intern",
        "training",
        "freelance"
    ]

    experience_score = 10 if any(
        word in text_lower
        for word in experience_keywords
    ) else 0

    if experience_score == 0:
        feedback.append(
            "Add internships, training or relevant experience."
        )

    breakdown["Experience"] = experience_score
    score += experience_score

    # -------------------------
    # Resume Length (10)
    # -------------------------

    if words >= 700:
        length_score = 8
        feedback.append("Resume is too long.")

    elif words >= 450:
        length_score = 10

    elif words >= 250:
        length_score = 8
        feedback.append("Resume can be expanded slightly.")

    elif words >= 150:
        length_score = 5
        feedback.append("Resume is too short.")

    else:
        length_score = 2
        feedback.append("Resume needs much more content.")

    breakdown["Resume Length"] = length_score
    score += length_score

    # -------------------------
    # Resume Structure (15)
    # -------------------------

    sections = [
        "summary",
        "objective",
        "education",
        "skills",
        "project",
        "experience"
    ]

    found = sum(
        1
        for section in sections
        if section in text_lower
    )

    structure_score = round((found / len(sections)) * 15)

    if structure_score < 10:
        feedback.append("Resume is missing important sections.")

    breakdown["Resume Structure"] = structure_score
    score += structure_score

    # -------------------------
    # Final Score
    # -------------------------

    score = min(score, 100)
        # -------------------------
    # Role Match (20)
    # -------------------------

    ROLE_KEYWORDS = {

        "Full Stack Developer": [
            "html", "css", "javascript", "react",
            "bootstrap", "flask", "django",
            "node", "express", "rest", "api",
            "sql", "postgresql", "mysql",
            "git", "docker"
        ],

        "Backend Developer": [
            "python", "java", "spring",
            "flask", "django",
            "rest", "api",
            "sql", "postgresql",
            "mysql", "git", "docker"
        ],

        "Frontend Developer": [
            "html", "css", "javascript",
            "react", "angular", "vue",
            "bootstrap", "tailwind", "git"
        ],

        "Data Scientist": [
            "python", "pandas", "numpy",
            "matplotlib", "seaborn",
            "scikit", "tensorflow",
            "keras", "statistics",
            "machine learning",
            "deep learning",
            "sql"
        ],

        "AI/ML Engineer": [
            "python",
            "tensorflow",
            "keras",
            "pytorch",
            "machine learning",
            "deep learning",
            "opencv",
            "scikit",
            "numpy",
            "pandas",
            "sql"
        ]

    }

    keywords = ROLE_KEYWORDS.get(target_role, [])

    matched = sum(
        1
        for keyword in keywords
        if keyword.lower() in text_lower
    )

    if len(keywords) > 0:
        role_score = round(
            (matched / len(keywords)) * 20
        )
    else:
        role_score = 0

    breakdown["Role Match"] = role_score
    score += role_score

    if role_score < 10:
        feedback.append(
            f"Add more {target_role} related keywords."
        )

    # -------------------------
    # Normalize Final Score
    # -------------------------

    if score > 100:
        score = 100

    return score, feedback, breakdown
