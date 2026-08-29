from ai.groq_client import ask_ai


def chat_with_resume(resume_text, user_question, chat_history):

    history = ""

    for message in chat_history:

        if message["role"] == "user":
            history += f"User: {message['content']}\n"

        else:
            history += f"Assistant: {message['content']}\n"

    prompt = f"""
You are CareerPilot AI.

You are an intelligent AI assistant.

The user has uploaded a resume.

Use the resume as context whenever useful.

If the question is unrelated to the resume,
answer like ChatGPT.

Previous Conversation:

{history}

Resume:

{resume_text}

Current User Question:

{user_question}

Answer professionally.
"""

    return ask_ai(prompt).strip()