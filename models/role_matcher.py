from dataset.job_roles import JOB_ROLES


def role_match(job_role, resume_skills):

    required_skills = JOB_ROLES.get(job_role, [])

    matched_skills = []

    missing_skills = []

    for skill in required_skills:

        if skill.lower() in [s.lower() for s in resume_skills]:

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)

    if len(required_skills) > 0:

        match_percentage = round(
            (len(matched_skills) / len(required_skills)) * 100
        )

    else:

        match_percentage = 0

    return matched_skills, missing_skills, match_percentage