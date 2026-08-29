import re

def extract_email(text):

    email = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return email[0] if email else "Not Found"


def extract_phone(text):

    phone = re.findall(
        r"(?:\+91[-\s]?)?[6-9]\d{9}",
        text
    )

    return phone[0] if phone else "Not Found"


def extract_name(text):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line.split()) >= 2 and len(line) < 40:

            return line

    return "Not Found"
