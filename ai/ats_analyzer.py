import json
import re

from ai.groq_client import ask_ai


def clean_json_response(response: str) -> str:
    """
    Removes markdown formatting from Groq responses.
    """

    response = response.replace("```json", "")
    response = response.replace("```", "")
    return response.strip()


def build_prompt(resume_text: str, target_role: str):

    return f"""
You are a Senior Technical Recruiter, ATS Expert, Hiring Manager and Career Coach.

Your job is to evaluate resumes exactly like a real recruiter.

====================================================
TARGET ROLE
====================================================

{target_role}

====================================================
SCORING RUBRIC (STRICT)
====================================================

Evaluate using these weights.

1. Contact Information .......... 5%

Must include:
- Name
- Email
- Phone

2. Resume Structure ............. 10%

Evaluate:

- Clear headings
- ATS friendly formatting
- No tables
- No excessive graphics
- Logical order

3. Education .................... 10%

Evaluate:

- Degree relevance
- CGPA if available
- Graduation year

4. Technical Skills ............. 20%

Evaluate:

- Programming Languages
- Frameworks
- Databases
- Cloud
- AI/ML
- DevOps
- Tools

Score should depend on

quality

AND

relevance to TARGET ROLE.

5. Projects ..................... 25%

This is VERY IMPORTANT.

DO NOT count the number of projects.

Instead evaluate:

- Technical complexity
- Technologies used
- Real-world usefulness
- Problem solved
- Project description
- Architecture
- Innovation
- Relevance to TARGET ROLE

Example:

Student Management System

Good for Backend Developer

Poor for AI Engineer

Likewise,

AI Chatbot

Excellent for AI Engineer

Average for Frontend Developer

6. Experience ................... 15%

Evaluate:

Internships

Freelancing

Research

Open Source

Work Experience

7. Certifications ............... 5%

Evaluate

quality

and

relevance.

8. Keyword Optimization ......... 10%

Evaluate

Resume keywords

against

TARGET ROLE.

====================================================
ATS SCORE
====================================================

ATS Score should NOT be random.

ATS Score must depend on

Contact

+

Education

+

Skills

+

Projects

+

Experience

+

Resume Structure

+

Keyword Optimization

Do not give ATS above 90 unless the resume is genuinely excellent.

Freshers should rarely exceed 80 unless their projects are exceptional.

====================================================
CAREER PREDICTION
====================================================

Predict careers ONLY from evidence.

Do NOT use the career objective.

Use:

Projects

Skills

Education

Experience

Return

Primary Career

Confidence

Alternative Careers

====================================================
PROJECT ANALYSIS
====================================================

Evaluate every project.

Judge

Technology

Architecture

Complexity

Problem Solving

Scalability

Documentation

Innovation

Role relevance

Return

Project Score

Role Relevance

Reason

Strengths

Weaknesses

====================================================
SKILLS
====================================================

Extract ONLY skills explicitly present.

Do NOT invent skills.

Separate

Technical

Soft

Missing

====================================================
INTERVIEW READINESS
====================================================

Evaluate

Problem Solving

Projects

Skills

Communication

Experience

Return score 0-100.

====================================================
RETURN ONLY JSON

DO NOT WRITE PARAGRAPHS

DO NOT WRITE MARKDOWN

DO NOT WRITE ```json

====================================================

Return EXACTLY this structure.

{{
  "ats_score": 0,
  "resume_score": 0,

  "career_prediction": {{
      "primary_role": "",
      "confidence": 0,
      "alternative_roles": []
  }},

  "project_analysis": {{
      "score": 0,
      "role_relevance": "",
      "reason": "",
      "strengths": [],
      "weaknesses": []
  }},

  "job_match": {{
      "score": 0,
      "reason": ""
  }},

  "skills": {{
      "technical": [],
      "soft": [],
      "missing": []
  }},

  "resume_sections": {{
      "contact": false,
      "education": false,
      "projects": false,
      "experience": false,
      "skills": false,
      "certifications": false
  }},

  "strengths": [],

  "weaknesses": [],

  "improvements": [],

  "interview_readiness": 0,

  "summary": ""
}}

====================================================
RESUME
====================================================

{resume_text}

"""
#-----------------------------------------------------------------------#

def analyze_resume_with_ai(
        resume_text,
        target_role,
        retries=2
):

    prompt = build_prompt(

        resume_text,

        target_role

    )

    for attempt in range(retries + 1):

        try:

            response = ask_ai(prompt)

            response = clean_json_response(response)

            data = json.loads(response)

            return validate_analysis(data)

        except Exception as e:

            print("AI ATS ERROR:", e)

            if attempt == retries:

                return default_response()

    return default_response()

def default_response():
    """
    Fallback response if AI fails.
    """

    return {

        "ats_score": 0,

        "resume_score": 0,

        "career_prediction": {

            "primary_role": "Career Not Identified",

            "confidence": 0,

            "alternative_roles": []

        },

        "project_analysis": {

            "score": 0,

            "role_relevance": "Unknown",

            "reason": "AI analysis unavailable.",

            "strengths": [],

            "weaknesses": []

        },

        "job_match": {

            "score": 0,

            "reason": "AI analysis unavailable."

        },

        "skills": {

            "technical": [],

            "soft": [],

            "missing": []

        },

        "resume_sections": {

            "contact": False,

            "education": False,

            "projects": False,

            "experience": False,

            "skills": False,

            "certifications": False

        },

        "strengths": [],

        "weaknesses": [],

        "improvements": [],

        "interview_readiness": 0,

        "summary": "Unable to analyze resume."

    }

def clamp_score(value):

    try:

        value = int(value)

    except:

        value = 0

    return max(0, min(100, value))

def validate_analysis(data):

    required = [

        "ats_score",

        "resume_score",

        "career_prediction",

        "project_analysis",

        "job_match",

        "skills",

        "resume_sections",

        "strengths",

        "weaknesses",

        "improvements",

        "interview_readiness",

        "summary"

    ]

    for key in required:

        if key not in data:

            raise ValueError(f"Missing key: {key}")

    data["ats_score"] = clamp_score(data["ats_score"])

    data["resume_score"] = clamp_score(data["resume_score"])

    data["interview_readiness"] = clamp_score(

        data["interview_readiness"]

    )

    data["career_prediction"]["confidence"] = clamp_score(

        data["career_prediction"]["confidence"]

    )

    data["project_analysis"]["score"] = clamp_score(

        data["project_analysis"]["score"]

    )

    data["job_match"]["score"] = clamp_score(

        data["job_match"]["score"]

    )

    return data

