import json
from ai.groq_client import ask_ai


def generate_learning_plan(
    task_title,
    career_goal,
    resume_text
):

    prompt = f"""
You are an expert AI Career Mentor and Senior Software Engineer.

The student is building a flagship project called:

AI Career Intelligence Platform

Technology Stack:
- Python
- Flask
- PostgreSQL
- Bootstrap 5
- HTML
- CSS
- JavaScript
- AI (Groq LLM)

Career Goal:
{career_goal}

Current Resume:

{resume_text[:4000]}

The student wants to learn:

{task_title}

Your job is to generate a personalized learning roadmap.

Rules:

1. Explain WHY this skill is important.
2. Estimate the learning duration realistically.
3. Mention the difficulty level.
4. Explain the career impact.
5. Give a mini project RELATED TO THE AI Career Intelligence Platform.
6. Generate exactly 5 learning steps.
7. Recommend only FREE and trusted resources.
8. Avoid generic advice.
9. Tailor the answer to the student's current resume and career goal.

Return ONLY valid JSON.

{{
"title":"",
"description":"",
"difficulty":"",
"duration":"",
"career_impact":"",
"mini_project":"",
"roadmap":[
"",
"",
"",
"",
""
],
"resources":[
{{
"name":"",
"url":""
}},
{{
"name":"",
"url":""
}},
{{
"name":"",
"url":""
}}
]
}}
"""

    answer = ask_ai(prompt).strip()

    # Remove markdown if Groq wraps the JSON
    if answer.startswith("```json"):
        answer = answer.replace("```json", "").replace("```", "").strip()

    elif answer.startswith("```"):
        answer = answer.replace("```", "").strip()

    try:
        return json.loads(answer)

    except Exception:

        return {
            "title": task_title,
            "description": "Unable to generate learning plan.",
            "difficulty": "Unknown",
            "duration": "Unknown",
            "career_impact": "",
            "mini_project": "",
            "roadmap": [],
            "resources": []
        }