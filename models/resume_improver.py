def generate_resume_summary(
    name,
    job_role,
    skills
):

    top_skills = ", ".join(skills[:5])

    summary = (
        f"{name} is an aspiring {job_role} with knowledge of "
        f"{top_skills}. Passionate about software development, "
        f"problem-solving, continuous learning, and building "
        f"real-world applications."
    )

    return summary