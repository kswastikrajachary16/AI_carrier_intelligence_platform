from dataset.job_roles import JOB_ROLES
from dataset.interview_bank import INTERVIEW_BANK


def generate_interview_preparation(job_role):

    skills = JOB_ROLES.get(job_role, [])

    interview_topics = []

    for skill in skills:

        skill_key = skill.lower()

        if skill_key in INTERVIEW_BANK:

            interview_topics.append({

                "skill": skill.title(),

                "category": INTERVIEW_BANK[skill_key]["category"],

                "difficulty": INTERVIEW_BANK[skill_key]["difficulty"],

                "estimated_time": INTERVIEW_BANK[skill_key]["estimated_time"],

                "question_count": len(
                    INTERVIEW_BANK[skill_key]["questions"]
                )

            })

    estimated_weeks = max(2, len(interview_topics) // 2)

    return interview_topics, estimated_weeks