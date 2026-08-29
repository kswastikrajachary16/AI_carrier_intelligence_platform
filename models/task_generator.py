def generate_tasks(score, skills, text, career_goal):

    tasks = []

    if score < 90:
        tasks.append((
            "Improve ATS Score to 90+",
            "https://resumeworded.com/"
        ))

    if "github" not in text.lower():
        tasks.append((
            "Add GitHub Profile",
            "https://github.com/"
        ))

    if "linkedin" not in text.lower():
        tasks.append((
            "Add LinkedIn Profile",
            "https://www.linkedin.com/"
        ))

    if "project" not in text.lower():
        tasks.append((
            "Add Two Technical Projects",
            "https://github.com/topics/project"
        ))

    if career_goal == "Full Stack Developer":

        tasks.append((
            "Learn Docker",
            "https://docs.docker.com/get-started/"
        ))

        tasks.append((
            "Learn REST APIs",
            "https://developer.mozilla.org/en-US/docs/Learn"
        ))

    elif career_goal == "Data Scientist":

        tasks.append((
            "Learn Pandas",
            "https://pandas.pydata.org/docs/"
        ))

        tasks.append((
            "Practice Machine Learning",
            "https://scikit-learn.org/stable/tutorial/"
        ))

    return tasks