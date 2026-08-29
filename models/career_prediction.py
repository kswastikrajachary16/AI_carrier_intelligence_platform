def predict_career(skills):

    skills = [skill.lower() for skill in skills]

    careers = {

        "AI Engineer": [
            "python",
            "tensorflow",
            "keras",
            "pytorch",
            "machine learning",
            "deep learning",
            "opencv"
        ],

        "Data Scientist": [
            "python",
            "pandas",
            "numpy",
            "machine learning",
            "sql"
        ],

        "Full Stack Developer": [
            "html",
            "css",
            "javascript",
            "react",
            "node.js",
            "java",
            "sql"
        ],

        "Java Developer": [
            "java",
            "spring",
            "hibernate",
            "sql"
        ],

        "Python Developer": [
            "python",
            "django",
            "flask",
            "sql"
        ]

    }

    results = []

    for career, required_skills in careers.items():

        matched = len(
            set(skills).intersection(required_skills)
        )

        if matched == 0:
            percentage = 0
        else:
            percentage = round(
                (matched / len(required_skills)) * 100
            )

        results.append(
            (
                career,
                percentage,
                matched
            )
        )

    results.sort(
        key=lambda x: (x[1], x[2]),
        reverse=True
    )

    # If no skills matched, don't guess a career
    if results[0][1] == 0:

        return [
            ("Career Not Identified", 0)
        ]

    return [
        (career, score)
        for career, score, _ in results[:3]
    ]