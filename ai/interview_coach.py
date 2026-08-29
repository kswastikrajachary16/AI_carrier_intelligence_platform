import json
from ai.groq_client import ask_ai


def interview_coach(resume_text):

    prompt = f"""
You are an expert Technical Interviewer.

Analyze the candidate's resume carefully.

Generate interview questions in FIVE categories.

1. HR Questions

Examples:
- Tell me about yourself.
- Why should we hire you?
- What are your strengths?
- What are your weaknesses?
- Why MCA?
- Describe yourself.

Generate 8 questions.

--------------------------------

2. Resume Questions

Generate questions from:

- Skills
- Education
- Internship
- Experience
- Certifications
- Achievements

Generate 10 questions.

--------------------------------

3. Project Questions

For EVERY project found in the resume, create a separate section using the project name as the key.

For each project generate 10–15 interview questions covering:

- Explain the project.
- What problem does it solve?
- Why did you build it?
- What was your role?
- Which technologies did you use?
- Why did you choose those technologies?
- Why not alternative technologies?
- Database design decisions.
- API design.
- Authentication and security.
- Challenges faced.
- How did you solve them?
- Performance optimization.
- Future improvements.
- If this project had 1 million users, what changes would you make?

Return the result like this:

"project_questions": {{
    "AI Career Intelligence Platform": [
        "...",
        "...",
        "..."
    ],
    "Hospital Management System": [
        "...",
        "...",
        "..."
    ]
}}

--------------------------------

"technology_questions":{{
    "Python":[...],
    "Flask":[...],
    "SQL":[...]
}}

--------------------------------

5. Core Subject Questions

Generate interview questions from:

DBMS
OOP
Operating System
Computer Networks
Software Engineering

Generate 5 questions for each subject.

--------------------------------

Return ONLY JSON.

Use this structure:

{{
"hr_questions": [],

"resume_questions": [],

"project_questions": {{}},

"technology_questions": {{}},

"core_subject_questions": {{
"DBMS": [],
"OOP": [],
"Operating System": [],
"Computer Networks": [],
"Software Engineering": []
}}

}}

Resume:

{resume_text}

"""

    response = ask_ai(prompt)

    response = response.replace("```json","")
    response = response.replace("```","").strip()

    return json.loads(response)