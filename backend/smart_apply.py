import re
import os
import PyPDF2
import docx2txt
from datetime import datetime
from extensions import db
from models import Job, Candidate, Application
from models.application import ApplicationStatus

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def extract_text_from_file(file_path):
    """Extract text from PDF, DOC, or DOCX file."""
    ext = file_path.lower().split('.')[-1]

    if ext == "pdf":
        text = ""
        with open(file_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        return text

    elif ext in {"doc", "docx"}:
        return docx2txt.process(file_path)

    else:
        raise ValueError(f"Unsupported file format: {ext}")


def get_job_text(job_id):
    """Combine description + requirements from Job table."""
    job = Job.query.get_or_404(job_id)
    job_text = (job.description or "") + "\n" + (job.requirements or "")
    return job_text.strip()


def get_ats_percentage(job_text, resume_text):
    """Use Gemini to get similarity percentage."""
    model = genai.GenerativeModel("gemini-2.5-pro")
    prompt = f"""
    Compare the job description and candidate resume.
    Return ONLY a numeric percentage (0-100) that represents the match score.

    Job Description:
    {job_text}

    Resume:
    {resume_text}
    """
    response = model.generate_content(prompt)
    match = re.search(r"\d{1,3}", response.text)
    return int(match.group(0)) if match else 0


def process_application(application_id):
    """
    Process an existing application:
    - Fetch job description + requirements
    - Fetch candidate resume
    - Compute AI similarity score
    - Update Application.ai_score and Application.status
    """
    application = Application.query.get_or_404(application_id)

    # Fetch job combined text
    job_text = get_job_text(application.job_id)

    # Fetch candidate resume
    candidate = application.candidate
    if not candidate.resume_path:
        raise ValueError("Candidate has no resume uploaded")

    resume_text = extract_text_from_file(candidate.resume_path)

    # Compute similarity percentage
    percentage = get_ats_percentage(job_text, resume_text)

    # Decide status
    status = (
        ApplicationStatus.SHORTLISTED
        if percentage >= 60
        else ApplicationStatus.REJECTED
    )

    # Update DB
    application.ai_score = percentage
    application.status = status
    db.session.commit()

    return application



