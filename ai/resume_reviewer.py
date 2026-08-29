from ai.groq_client import ask_ai


def review_resume(resume_text, target_role):

    prompt = f"""
You are an expert ATS recruiter and career coach.

Analyze the following resume.

Target Role:
{target_role}

Resume:
{resume_text}

Return ONLY valid JSON.

Format:

{{
    "strengths": [
        "...",
        "..."
    ],
    "weaknesses": [
        "...",
        "..."
    ],
    "suggestions": [
        "...",
        "..."
    ],
    "ats_improvement": [
        "...",
        "..."
    ]
}}

Rules:
1. Return ONLY valid JSON.
2. Do NOT use markdown.
3. Do NOT use ```json or ``` code blocks.
4. Do NOT write any explanation before or after the JSON.
5. Maximum 4 points per section.
6. Make every point short, professional and ATS-focused.
"""

    return ask_ai(prompt)