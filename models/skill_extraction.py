import re

skills_database = [

    "python",
    "java",
    "c",
    "c++",

    "sql",
    "mysql",
    "postgresql",
    "oracle",

    "html",
    "css",
    "javascript",
    "bootstrap",

    "react",
    "node.js",

    "flask",
    "django",
    "fastapi",

    "git",
    "github",

    "docker",
    "kubernetes",

    "aws",
    "azure",
    "gcp",

    "machine learning",
    "deep learning",
    "tensorflow",
    "keras",
    "pytorch",

    "numpy",
    "pandas",
    "scikit-learn",
    "opencv",

    "power bi",
    "excel"

]


def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in skills_database:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(list(set(found_skills)))