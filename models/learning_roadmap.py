def generate_learning_roadmap(missing_skills):

    roadmap = []

    week = 1

    for skill in missing_skills:

        roadmap.append({

            "week": week,

            "skill": skill

        })

        week += 1

    return roadmap