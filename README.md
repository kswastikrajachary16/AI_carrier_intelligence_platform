# AI Career Intelligence Platform

An AI-powered career assistance platform that brings resume analysis, career guidance, interview preparation, job discovery, and related career tools into one application.

## Features

* **AI Resume Analysis** — analyze an uploaded PDF resume and receive AI-powered feedback.
* **ATS / Resume Scoring** — evaluate resume quality and highlight areas for improvement.
* **Career Guidance** — get AI-assisted career recommendations based on resume information and skills.
* **Career Prediction** — identify suitable career directions from the available profile information.
* **Interview Preparation** — practice personalized interview questions with AI assistance.
* **Job Finder** — search job listings using the JSearch/RapidAPI integration.
* **Job Description Matching** — compare a resume/profile against a job description.
* **Resume Chat** — interact with resume-related information through AI.
* **Forgot Password with OTP** — recover an account using email-based OTP verification.
* **Dashboard** — access career-related results and platform features from a central interface.
* **Responsive UI** — dark-themed interface with animated homepage sections and an integrated product demo.

## Tech Stack

### Backend

* Python
* Flask
* PostgreSQL
* psycopg2
* bcrypt

### AI

* Groq API
* LLM-powered resume, career, interview, and job-description features

### Frontend

* HTML
* CSS
* JavaScript
* Bootstrap / Bootstrap Icons where used by the application

### APIs \& Services

* Groq API
* JSearch / RapidAPI
* Gmail SMTP for OTP email delivery

### Document Processing

* pdfplumber for PDF resume text extraction

## Project Structure

```text
AI\_carrier\_intelligence\_platform/
│
├── ai/
│   ├── ats\_analyzer.py
│   ├── career\_coach.py
│   ├── groq\_client.py
│   ├── groq\_resume\_review.py
│   ├── interview\_coach.py
│   ├── jd\_matcher.py
│   ├── jd\_parser.py
│   ├── jobs\_api.py
│   ├── resume\_chat.py
│   └── resume\_reviewer.py
│
├── dataset/
├── ml/
├── models/
├── parser/
├── templates/
├── static/
│   ├── css/
│   ├── images/
│   ├── js/
│   └── videos/
│       └── platform-demo.mp4
│
├── utils/
├── app.py
├── config.py
├── database.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Local Setup

### 1\. Clone the repository

```bash
git clone https://github.com/kswastikrajachary16/AI\_carrier\_intelligence\_platform.git
cd AI\_carrier\_intelligence\_platform
```

### 2\. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\\Scripts\\activate
```

### 3\. Install dependencies

```bash
pip install -r requirements.txt
```

### 4\. Configure environment variables

Create a `.env` file in the project root.

Use `.env.example` as the template:

```env
DB\_HOST=localhost
DB\_PORT=5432
DB\_NAME=your\_database\_name
DB\_USER=your\_postgres\_user
DB\_PASSWORD=your\_postgres\_password

SECRET\_KEY=replace\_with\_a\_long\_random\_secret

GROQ\_API\_KEY=your\_groq\_api\_key

SMTP\_SERVER=smtp.gmail.com
SMTP\_PORT=587
SMTP\_EMAIL=your\_gmail\_address
SMTP\_PASSWORD=your\_gmail\_app\_password

RAPIDAPI\_KEY=your\_rapidapi\_key
```

**Never commit the real `.env` file or API keys to GitHub.**

### 5\. Set up PostgreSQL

Create the PostgreSQL database configured in your `.env` file and make sure the required application tables are available.

### 6\. Run the application

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Environment Variables

|Variable|Purpose|
|-|-|
|`DB\_HOST`|PostgreSQL host|
|`DB\_PORT`|PostgreSQL port|
|`DB\_NAME`|Application database name|
|`DB\_USER`|PostgreSQL username|
|`DB\_PASSWORD`|PostgreSQL password|
|`SECRET\_KEY`|Flask session/security key|
|`GROQ\_API\_KEY`|Groq AI API key|
|`SMTP\_SERVER`|SMTP server|
|`SMTP\_PORT`|SMTP port|
|`SMTP\_EMAIL`|Email account used for OTP|
|`SMTP\_PASSWORD`|Email app password|
|`RAPIDAPI\_KEY`|RapidAPI key for job search|

## Security

Secrets are loaded through environment variables rather than being stored directly in application source code.

The real `.env` file is excluded through `.gitignore`.

Before publishing a repository publicly, make sure no API keys, passwords, database credentials, or other secrets are present in tracked files.

## Demo

The homepage includes a short demonstration video of the platform.

Local video path:

```text
static/videos/platform-demo.mp4
```

## Future Improvements

* Production deployment and scalable file storage
* More advanced career recommendations
* Additional job-search filters
* Improved analytics and career insights
* Expanded interview evaluation capabilities

## Author

**Swastik Raj Achary**

AI Career Intelligence Platform — portfolio project.

