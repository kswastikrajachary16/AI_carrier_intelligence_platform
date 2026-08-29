import json
from ai.groq_client import ask_ai


def analyze_career(resume_text):

    prompt = f"""
You are an expert AI Career Coach.

Analyze the resume below.

Resume:
{resume_text}

Return ONLY valid JSON.

{{
    "candidate_profile":"",
    "best_roles":[],
    "strengths":[],
    "skills_to_learn":[],
    "learning_roadmap": {{
        "month_1":"",
        "month_2":"",
        "month_3":""
    }},
    "recommended_certifications":[],
    "suggested_companies":[],
    "salary_range":"",
    "career_advice":""
}}
"""

    response = ask_ai(prompt)

    response = response.replace("```json", "")
    response = response.replace("```", "").strip()

    return json.loads(response)