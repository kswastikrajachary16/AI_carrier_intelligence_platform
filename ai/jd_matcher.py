import json

from ai.groq_client import ask_ai


def analyze_resume_job_match(resume_text, job_data):

    prompt = f"""
You are an expert ATS and Recruitment AI.

Compare the candidate's resume with the Job Description.

Resume:

{resume_text}

Job Description:

{json.dumps(job_data, indent=2)}

Return ONLY raw JSON.

Do NOT use markdown.

Do NOT use ```json.

Return this format only:

{{
    "match_percentage": 0,
    "ats_score": 0,
    "matching_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "suggestions": [],
    "final_verdict": ""
}}
"""

    response = ask_ai(prompt)

    response = response.replace("```json", "")
    response = response.replace("```", "").strip()

    return json.loads(response)