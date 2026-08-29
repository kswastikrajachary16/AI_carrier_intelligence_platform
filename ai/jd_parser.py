import json

from ai.groq_client import ask_ai


def parse_job_description(job_description):

    prompt = f"""
You are an expert ATS parser.

Extract the following information from the job description.

Return ONLY valid JSON.

Fields:

job_title
company
location
experience
education
required_skills
preferred_skills

Job Description:

{job_description}
"""

    response = ask_ai(prompt)

# Remove markdown formatting if present
    response = response.replace("```json", "")
    response = response.replace("```", "").strip()

    try:
        data = json.loads(response)
        return data

    except:

        return {
            "error": "Invalid JSON returned",
            "raw_response": response
        }