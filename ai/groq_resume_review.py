import json
from ai.groq_client import ask_ai


def review_resume(resume_text):

    prompt = f"""
You are an expert ATS Resume Reviewer and Technical Recruiter.

Analyze this resume.

Return ONLY valid JSON.

JSON Format:

{{
"overall_score": 0,
"ats_score": 0,
"summary": "",
"strengths": [],
"weaknesses": [],
"suggestions": [],
"missing_skills": [],
"final_verdict": ""
}}

Resume:

{resume_text}

"""

    response = ask_ai(prompt)

    response = response.replace("```json", "")
    response = response.replace("```", "").strip()

    return json.loads(response)