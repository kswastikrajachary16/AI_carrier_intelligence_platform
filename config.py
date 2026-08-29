import os
from dotenv import load_dotenv

# Load variables from .env when running locally
load_dotenv()

# ==========================
# Database Configuration
# ==========================
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# ==========================
# Flask Configuration
# ==========================
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")

UPLOAD_FOLDER = os.path.join(
    os.getcwd(),
    "uploads"
)

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf"}

# ==========================
# Groq Configuration
# ==========================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ==========================
# Email / SMTP Configuration
# ==========================
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# ==========================
# RapidAPI / Job Finder
# ==========================
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
