import bcrypt
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    flash
)
from database import get_connection
from parser.resume_parser import extract_text
from models.skill_extraction import extract_skills
from models.information_extraction import (
    extract_name,
    extract_email,
    extract_phone
)
from models.ats_score import calculate_ats_score
from models.role_matcher import role_match
from models.career_prediction import predict_career
from dataset.job_roles import JOB_ROLES
from models.learning_roadmap import generate_learning_roadmap
from models.ai_suggestions import generate_ai_suggestions
from config import (
    SECRET_KEY,
    UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH,
    ALLOWED_EXTENSIONS,
    SMTP_SERVER,
    SMTP_PORT,
    SMTP_EMAIL,
    SMTP_PASSWORD
)
from models.interview_preparation import generate_interview_preparation
from dataset.interview_bank import INTERVIEW_BANK
from models.resume_improver import generate_resume_summary
import os
import json
from ai.groq_resume_review import review_resume
from ai.jd_parser import parse_job_description
from ai.jd_matcher import analyze_resume_job_match
from ai.career_coach import analyze_career
from ai.interview_coach import interview_coach
from ai.resume_chat import chat_with_resume
from psycopg2.extras import RealDictCursor
import random
import smtplib
from email.mime.text import MIMEText
from models.task_generator import generate_tasks
from models.learning_mentor import generate_learning_plan
from flask import jsonify
from utils.dashboard_metrics import (
    calculate_skill_score,
    calculate_project_score,
    calculate_resume_completeness
)
from ai.ats_analyzer import analyze_resume_with_ai
from ai.jobs_api import search_jobs

app = Flask(__name__)

app.secret_key = SECRET_KEY

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
        # If user is already logged in
    if "user_id" in session:
        return redirect("/dashboard")

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:

            stored_password = user[3]

            if bcrypt.checkpw(
                password.encode("utf-8"),
                stored_password.encode("utf-8")
            ):

                session["user_id"] = user[0]
                session["user_name"] = user[1]
                session["user_email"] = user[2]

                return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():
        # If user is already logged in
    if "user_id" in session:
        return redirect("/dashboard")

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
        ).decode("utf-8")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
    """
    INSERT INTO users(full_name, email, password)
    VALUES(%s, %s, %s)
    """,
         (full_name, email, hashed_password)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # -----------------------------------
    # Get Latest Resume
    # -----------------------------------
    cursor.execute("""
        SELECT *
        FROM resumes
        WHERE user_id=%s
        ORDER BY uploaded_at DESC
        LIMIT 1
    """, (session["user_id"],))

    resume = cursor.fetchone()

    analysis = {}

    if resume and resume.get("ai_analysis"):

        if isinstance(resume["ai_analysis"], str):
            analysis = json.loads(resume["ai_analysis"])
        else:
            analysis = resume["ai_analysis"]

    # -----------------------------------
    # No Resume Uploaded
    # -----------------------------------

    if resume is None:

        resume = {
            "ats_score": 0,
            "career_goal": "Not Available",
            "skills_count": 0,
            "resume_status": "Not Uploaded"
        }

        suggestions = []
        tasks = []

        technical_skills = []
        missing_skills = []

        skill_score = 0
        project_score = 0
        resume_completeness = 0
        match_percentage = 0

    else:

        # -----------------------------------
        # AI Metrics
        # -----------------------------------

        technical_skills = analysis.get(
            "skills",
            {}
        ).get(
            "technical",
            []
        )

        missing_skills = analysis.get(
            "skills",
            {}
        ).get(
            "missing",
            []
        )

        skill_score = analysis.get(
            "job_match",
            {}
        ).get(
            "score",
            0
        )

        match_percentage = analysis.get(
            "job_match",
            {}
        ).get(
            "score",
            0
        )

        project_score = analysis.get(
            "project_analysis",
            {}
        ).get(
            "score",
            0
        )

        resume_completeness = analysis.get(
            "resume_score",
            0
        )

        # -----------------------------------
        # Fetch Learning Tasks
        # -----------------------------------

        cursor.execute("""
            SELECT
                id,
                title,
                resource_link,
                completed
            FROM tasks
            WHERE user_id=%s
            ORDER BY id
        """, (session["user_id"],))

        tasks = cursor.fetchall()

        # -----------------------------------
        # AI Suggestions
        # -----------------------------------

        suggestions = []

        if resume["ats_score"] < 60:
            suggestions.append(
                "Improve your ATS score above 80%."
            )

        elif resume["ats_score"] < 80:
            suggestions.append(
                "Increase your ATS score to become more competitive."
            )

        if resume["skills_count"] < 10:
            suggestions.append(
                "Add more technical skills."
            )

        for skill in missing_skills[:3]:
            suggestions.append(
                f"Learn {skill}."
            )

        pending_tasks = [
            task
            for task in tasks
            if not task["completed"]
        ]

        for task in pending_tasks[:2]:
            suggestions.append(
                f'Complete learning task: "{task["title"]}"'
            )

        suggestions = list(dict.fromkeys(suggestions))
        suggestions = suggestions[:5]

        resume["ats_score"] = resume.get("ats_score", 0)
        resume["career_goal"] = resume.get(
            "career_goal",
            "Not Available"
        )
        resume["skills_count"] = resume.get(
            "skills_count",
            0
        )
        resume["resume_status"] = resume.get(
            "resume_status",
            "Not Uploaded"
        )

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",

        resume=resume,

        suggestions=suggestions,

        tasks=tasks,

        job_match=match_percentage,

        skill_score=skill_score,

        project_score=project_score,

        resume_completeness=resume_completeness,

        analysis=analysis,

        technical_skills=technical_skills,

        missing_skills=missing_skills,

        strengths=analysis.get(
            "strengths",
            []
        ),

        weaknesses=analysis.get(
            "weaknesses",
            []
        ),

        interview_readiness=analysis.get(
            "interview_readiness",
            0
        ),

        summary=analysis.get(
            "summary",
            ""
        )
    )


# ---------------- RESUME UPLOAD ----------------

@app.route("/upload", methods=["GET", "POST"])
def upload():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        # -------------------------------
        # Selected Job Role
        # -------------------------------
        job_role = request.form["job_role"]

        # -------------------------------
        # Uploaded Resume
        # -------------------------------
        file = request.files["resume"]

        if file.filename == "":
            flash("Please select a resume.", "warning")
            return redirect("/upload")

        filename = file.filename

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(file_path)

        # -------------------------------
        # Extract Resume Text
        # -------------------------------
        text = extract_text(file_path)

        # Optional (can be removed later)
        name = extract_name(text)
        email = extract_email(text)
        phone = extract_phone(text)

        # -------------------------------
        # AI Resume Analysis
        # -------------------------------
        analysis = analyze_resume_with_ai(
            resume_text=text,
            target_role=job_role
        )

        # -------------------------------
        # Extract AI Results
        # -------------------------------
        score = analysis["ats_score"]

        career_goal = analysis["career_prediction"]["primary_role"]

        skills = analysis["skills"]["technical"]

        skills_count = len(skills)

        resume_status = "Uploaded"

        # -------------------------------
        # Generate Learning Tasks
        # -------------------------------
        tasks = generate_tasks(
            score,
            skills,
            text,
            career_goal
        )

        # -------------------------------
        # Database
        # -------------------------------
        conn = get_connection()
        cursor = conn.cursor()

        # Remove previous tasks
        cursor.execute("""
            DELETE FROM tasks
            WHERE user_id=%s
        """, (session["user_id"],))

        # Save Resume
        cursor.execute("""
            INSERT INTO resumes(
            user_id,
            file_name,
            job_role,
            ats_score,
            career_goal,
            skills_count,
            resume_status,
            ai_analysis
           )
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """,
       (
        session["user_id"],
        filename,
        job_role,
        score,
        career_goal,
        skills_count,
        resume_status,
        json.dumps(analysis)
       ))

        # Save Tasks
        for title, link in tasks:

            cursor.execute("""
                INSERT INTO tasks(
                    user_id,
                    title,
                    resource_link
                )
                VALUES(%s,%s,%s)
            """,
            (
                session["user_id"],
                title,
                link
            ))

        conn.commit()

        cursor.close()
        conn.close()

        flash("Resume uploaded successfully!", "success")

        return redirect("/dashboard")

    return render_template("upload.html")




# ---------------- LEARNING ROADMAP ----------------

@app.route("/roadmap")
def roadmap():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("roadmap.html")


# ---------------- PROFILE ----------------

@app.route("/profile", methods=["GET", "POST"])
def profile():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()

    cursor = connection.cursor(cursor_factory=RealDictCursor)

    # Update profile
    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]

        cursor.execute("""
            UPDATE users
            SET full_name = %s,
                email = %s
            WHERE id = %s
        """, (
            full_name,
            email,
            session["user_id"]
        ))

        connection.commit()

    # Fetch latest user data
    cursor.execute("""
        SELECT
            id,
            full_name,
            email,
            created_at
        FROM users
        WHERE id = %s
    """, (session["user_id"],))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "profile.html",
        user=user
    )

#-----------------SETTINGS----------------

@app.route("/settings")
def settings():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("settings.html")

#-----------------LOGOUT------------------

@app.route("/logout")
def logout():

    if "user_id" not in session:
        return redirect("/login")

    session.clear()

    return redirect("/login")

#-------------INTERVIEW--------------


@app.route("/interview/<skill>")
def interview_questions(skill):

    if "user_id" not in session:
        return redirect("/login")

    skill = skill.lower()

    if skill not in INTERVIEW_BANK:
        flash("Interview questions not available.", "warning")
        return redirect("/dashboard")

    data = INTERVIEW_BANK[skill]

    return render_template(
        "interview_questions.html",
        skill=skill.title(),
        questions=data["questions"]
    )

#------------------------------------

@app.after_request
def add_header(response):

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response

#----------------- AI-WORKSPACE-----------------

@app.route("/ai-workspace")
def ai_workspace():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("ai_workspace.html")

#------------AI_RESUME-------------------


@app.route("/ai-resume-review")
def ai_resume_review():

    if "user_id" not in session:
        return redirect("/login")

    upload_folder = "uploads"

    files = os.listdir(upload_folder)

    pdf_files = [f for f in files if f.endswith(".pdf")]

    if not pdf_files:

        return "No resume uploaded."

    latest_resume = max(
    [os.path.join(upload_folder, f) for f in pdf_files],
    key=os.path.getmtime
    )

    resume_text = extract_text(latest_resume)

    review = review_resume(resume_text)

    return render_template(

        "ai_resume_review.html",

        review=review

    )

#-------------JD-ANALYZER------------------

@app.route("/jd-analyzer", methods=["GET", "POST"])
def jd_analyzer():

    if "user_id" not in session:
        return redirect("/login")

    match_result = None
    if request.method == "POST":

        # Get Job Description
        job_description = request.form["job_description"]

        # -------------------------------
        # Read Latest Uploaded Resume
        # -------------------------------

        upload_folder = "uploads"

        files = os.listdir(upload_folder)

        pdf_files = [f for f in files if f.endswith(".pdf")]

        if not pdf_files:
            return "No resume uploaded."

        latest_resume = max(
            [os.path.join(upload_folder, f) for f in pdf_files],
            key=os.path.getmtime
        )

        resume_text = extract_text(latest_resume)

        print("\n========== RESUME TEXT ==========")
        print(resume_text[:500])      # Print only first 500 characters
        print("=================================\n")

        # -------------------------------
        # Parse Job Description
        # -------------------------------

        print("\n========== JOB DESCRIPTION ==========")
        result = parse_job_description(job_description)
        print(result)
        print("=====================================\n")
        print("\n========== MATCH RESULT ==========")

        match_result = analyze_resume_job_match(
        resume_text,
        result
        )

        print(match_result)

        print("==================================\n")

    return render_template(
    "jd_analyzer.html",
    match_result=match_result
    )

#----------------CAREER-COACH------------

@app.route("/career-coach")
def career_coach():

    if "user_id" not in session:
        return redirect("/login")

    upload_folder = "uploads"

    files = os.listdir(upload_folder)

    pdf_files = [f for f in files if f.endswith(".pdf")]

    if not pdf_files:
        return "No resume uploaded."

    latest_resume = max(
        [os.path.join(upload_folder, f) for f in pdf_files],
        key=os.path.getmtime
    )

    resume_text = extract_text(latest_resume)

    career_result = analyze_career(resume_text)

    return render_template(
        "career_coach.html",
        career_result=career_result
    )

#-------------INTERVIEW-COACH------------

@app.route("/interview-coach")
def ai_interview_coach():

    if "user_id" not in session:
        return redirect("/login")

    upload_folder = "uploads"

    files = os.listdir(upload_folder)

    pdf_files = [f for f in files if f.endswith(".pdf")]

    if not pdf_files:
        return "No resume uploaded."

    latest_resume = max(
        [os.path.join(upload_folder, f) for f in pdf_files],
        key=os.path.getmtime
    )

    resume_text = extract_text(latest_resume)

    interview_result = interview_coach(resume_text)
    print(interview_result)

    return render_template(
        "interview_coach.html",
        interview_result=interview_result
    )

#------------------RESUME-CHAT-------------
@app.route("/resume-chat", methods=["GET", "POST"])
def resume_chat():

    if "user_id" not in session:
        return redirect("/login")

    upload_folder = "uploads"

    files = os.listdir(upload_folder)

    pdf_files = [f for f in files if f.endswith(".pdf")]

    if not pdf_files:
        return "No resume uploaded."

    latest_resume = max(
        [os.path.join(upload_folder, f) for f in pdf_files],
        key=os.path.getmtime
    )

    resume_text = extract_text(latest_resume)

    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":

        question = request.form["question"]

        history = session["chat_history"]

        answer = chat_with_resume(
            resume_text,
            question,
            history
        )

        history.append({
            "role": "user",
            "content": question
        })

        history.append({
            "role": "assistant",
            "content": answer
        })

        session["chat_history"] = history

    return render_template(
        "resume_chat.html",
        chat_history=session["chat_history"]
    )  
#--------------CHANGE-PASSWORD-----------

@app.route("/change-password", methods=["GET", "POST"])
def change_password():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        current_password = request.form["current_password"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        if new_password != confirm_password:
            flash("New passwords do not match.", "danger")
            return redirect("/change-password")

        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        cursor.execute("""
            SELECT password
            FROM users
            WHERE id = %s
        """, (session["user_id"],))

        user = cursor.fetchone()

        if not bcrypt.checkpw(
            current_password.encode("utf-8"),
            user["password"].encode("utf-8")
        ):
            cursor.close()
            connection.close()

            flash("Current password is incorrect.", "danger")
            return redirect("/change-password")

        hashed_password = bcrypt.hashpw(
            new_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute("""
            UPDATE users
            SET password = %s
            WHERE id = %s
        """, (
            hashed_password,
            session["user_id"]
        ))

        connection.commit()

        cursor.close()
        connection.close()

        flash("Password updated successfully.", "success")

        return redirect("/settings")

    return render_template("change_password.html")


# ---------------- FORGOT PASSWORD ----------------

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"].strip().lower()

        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Check whether email exists
        cursor.execute("""
            SELECT id, email
            FROM users
            WHERE LOWER(email) = %s
        """, (email,))

        user = cursor.fetchone()

        if not user:

            cursor.close()
            connection.close()

            flash("Email not found.", "danger")

            return redirect("/forgot-password")

        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))

        # OTP valid for 10 minutes
        cursor.execute("""
            DELETE FROM password_reset_otps
            WHERE user_id = %s
        """, (user["id"],))

        cursor.execute("""
            INSERT INTO password_reset_otps
            (
                user_id,
                email,
                otp,
                expires_at
            )
            VALUES
            (
                %s,
                %s,
                %s,
                NOW() + INTERVAL '10 minutes'
            )
        """, (
            user["id"],
            user["email"],
            otp
        ))

        connection.commit()

        cursor.close()
        connection.close()

        # ---------------- SEND EMAIL ----------------

        try:

            message = MIMEText(
                f"""
Hello,

We received a request to reset your password for AI Career Intelligence Platform.

Your OTP is:

{otp}

This OTP is valid for 10 minutes.

If you did not request a password reset, you can safely ignore this email.

Regards,
AI Career Intelligence Platform
"""
            )

            message["Subject"] = "Password Reset OTP"
            message["From"] = SMTP_EMAIL
            message["To"] = user["email"]

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:

                server.starttls()

                server.login(
                    SMTP_EMAIL,
                    SMTP_PASSWORD
                )

                server.send_message(message)

            # Store email temporarily in session
            session["reset_email"] = user["email"]

            flash(
                "OTP sent successfully. Check your email.",
                "success"
            )

            return redirect("/verify-otp")

        except Exception as e:

            print("OTP EMAIL ERROR:", e)

            flash(
                "Unable to send OTP. Please try again.",
                "danger"
            )

            return redirect("/forgot-password")

    return render_template("forgot_password.html")

#-----------TASK----------------
@app.route("/task/<int:task_id>")
def task_details(task_id):

    if "user_id" not in session:
        return jsonify({"success": False})

    

    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # -----------------------------
    # Get Task
    # -----------------------------

    cursor.execute("""
        SELECT *
        FROM tasks
        WHERE
            id=%s
            AND user_id=%s
    """,
    (
        task_id,
        session["user_id"]
    ))

    task = cursor.fetchone()

    if not task:

        cursor.close()
        conn.close()

        return jsonify({
            "success": False,
            "message": "Task not found"
        })

    # -----------------------------
    # Check Cached AI Plan
    # -----------------------------

    cursor.execute("""
        SELECT *
        FROM learning_plans
        WHERE task_id=%s
    """,
    (task_id,))

    cached = cursor.fetchone()

    if cached:

        cursor.close()
        conn.close()

        return jsonify({

            "title": cached["title"],

            "description": cached["description"],

            "difficulty": cached["difficulty"],

            "duration": cached["duration"],

            "career_impact": cached["career_impact"],

            "mini_project": cached["mini_project"],

            "roadmap": cached["roadmap"],

            "resources": cached["resources"]

        })

    # -----------------------------
    # Latest Resume
    # -----------------------------

    cursor.execute("""
        SELECT *
        FROM resumes
        WHERE user_id=%s
        ORDER BY uploaded_at DESC
        LIMIT 1
    """,
    (session["user_id"],))

    resume = cursor.fetchone()

    if not resume:

        cursor.close()
        conn.close()

        return jsonify({
            "success": False,
            "message": "Resume not found"
        })

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        resume["file_name"]
    )

    resume_text = extract_text(file_path)

    plan = generate_learning_plan(
        task["title"],
        resume["career_goal"],
        resume_text
    )

    # -----------------------------
    # Save AI Plan
    # -----------------------------

    cursor.execute("""
        INSERT INTO learning_plans(

            task_id,
            title,
            description,
            difficulty,
            duration,
            career_impact,
            mini_project,
            roadmap,
            resources

        )

        VALUES(

            %s,%s,%s,%s,%s,%s,%s,%s,%s

        )
    """,
    (
        task_id,
        plan["title"],
        plan["description"],
        plan["difficulty"],
        plan["duration"],
        plan["career_impact"],
        plan["mini_project"],
        json.dumps(plan["roadmap"]),
        json.dumps(plan["resources"])
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify(plan)

#-------------JOBS------------
@app.route("/jobs", methods=["GET"])
def jobs():

    query = request.args.get("query", "").strip()

    jobs = []

    error = None

    if query:

        try:
            jobs = search_jobs(query)

        except Exception as e:
            error = str(e)

    return render_template(
        "jobs.html",
        jobs=jobs,
        query=query,
        error=error
    )
    
# ---------------- VERIFY OTP ----------------

@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    if "reset_email" not in session:
        flash("Please request a password reset first.", "warning")
        return redirect("/forgot-password")

    if request.method == "POST":

        entered_otp = request.form["otp"].strip()
        email = session["reset_email"]

        connection = get_connection()
        cursor = connection.cursor(cursor_factory=RealDictCursor)

        # Get the latest OTP
        cursor.execute("""
            SELECT *
            FROM password_reset_otps
            WHERE email = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (email,))

        otp_record = cursor.fetchone()

        if not otp_record:

            cursor.close()
            connection.close()

            flash("OTP not found. Please request a new OTP.", "danger")
            return redirect("/forgot-password")

        # Check OTP expiry
        cursor.execute("""
            SELECT
                NOW() > expires_at AS expired
            FROM password_reset_otps
            WHERE id = %s
        """, (otp_record["id"],))

        expiry_result = cursor.fetchone()

        if expiry_result["expired"]:

            cursor.close()
            connection.close()

            flash("OTP has expired. Please request a new OTP.", "danger")
            return redirect("/forgot-password")

        # Check OTP
        if entered_otp != otp_record["otp"]:

            cursor.close()
            connection.close()

            flash("Invalid OTP. Please try again.", "danger")
            return redirect("/verify-otp")

        # Mark OTP as verified
        cursor.execute("""
            UPDATE password_reset_otps
            SET verified = TRUE
            WHERE id = %s
        """, (otp_record["id"],))

        connection.commit()

        cursor.close()
        connection.close()

        # Allow password reset
        session["otp_verified"] = True

        flash(
            "OTP verified successfully. You can now reset your password.",
            "success"
        )

        return redirect("/reset-password")

    return render_template("verify_otp.html")

# ---------------- RESET PASSWORD ----------------

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    # User must complete OTP verification first
    if not session.get("otp_verified"):
        flash("Please verify the OTP first.", "warning")
        return redirect("/forgot-password")

    if "reset_email" not in session:
        flash("Password reset session expired. Please try again.", "warning")
        return redirect("/forgot-password")

    if request.method == "POST":

        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        # Check password confirmation
        if new_password != confirm_password:

            flash(
                "New passwords do not match.",
                "danger"
            )

            return redirect("/reset-password")

        # Basic password validation
        if len(new_password) < 6:

            flash(
                "Password must be at least 6 characters long.",
                "danger"
            )

            return redirect("/reset-password")

        email = session["reset_email"]

        connection = get_connection()
        cursor = connection.cursor()

        # Hash new password
        hashed_password = bcrypt.hashpw(
            new_password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Update password
        cursor.execute("""
            UPDATE users
            SET password = %s
            WHERE LOWER(email) = LOWER(%s)
        """, (
            hashed_password,
            email
        ))

        connection.commit()

        cursor.close()
        connection.close()

        # Remove password-reset session data
        session.pop("reset_email", None)
        session.pop("otp_verified", None)

        flash(
            "Password reset successfully. Please login with your new password.",
            "success"
        )

        return redirect("/login")

    return render_template("reset_password.html")

#----------------END-------------------
if __name__ == "__main__":
    app.run(debug=True)