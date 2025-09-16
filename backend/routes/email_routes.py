# backend/routes/email_routes.py
from flask import Blueprint, jsonify, current_app
from extensions import db
from models import Application, Candidate
from models.application import ApplicationStatus
from models.email_log import EmailLog, EmailType
from models.application_progress import ApplicationProgress
import smtplib
from email.message import EmailMessage

email_bp = Blueprint("email", __name__, url_prefix="/emails")


def send_email(recipient: str, subject: str, body: str):
    """Send email via SMTP."""
    SMTP_SERVER = current_app.config.get("SMTP_SERVER")
    SMTP_PORT = current_app.config.get("SMTP_PORT")
    SMTP_USER = current_app.config.get("SMTP_USER")
    SMTP_PASSWORD = current_app.config.get("SMTP_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = recipient
    msg.set_content(body)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)


@email_bp.route("/send/<int:job_id>", methods=["POST"])
def send_emails(job_id):
    results = []

    # Get all applications for the job
    applications = Application.query.filter_by(job_id=job_id).all()

    for app_obj in applications:
        candidate = app_obj.candidate
        recipient = candidate.email

        # Prepare email content
        subject = "Application Update"
        if app_obj.status == ApplicationStatus.SHORTLISTED:
            body = f"Dear {candidate.name},\n\nCongratulations! You have been shortlisted for the job."
            progress_notes = "Candidate matched AI score of requirements, shortlisted for interview."
        else:
            body = f"Dear {candidate.name},\n\nWe regret to inform you that you were not selected for the job."
            progress_notes = "Rejected due to AI score below threshold."

        try:
            # Send email
            send_email(recipient, subject, body)

            # Log email in DB
            email_log = EmailLog(
                application_id=app_obj.application_id,
                recipient=recipient,
                subject=subject,
                body=body,
                type=EmailType.CUSTOM
            )
            db.session.add(email_log)

            # Add entry to ApplicationProgress
            progress = ApplicationProgress(
                application_id=app_obj.application_id,
                status=app_obj.status,
                notes=progress_notes,
                # updated_by=None or pass admin id if available
            )
            db.session.add(progress)

            db.session.commit()
            results.append({"application_id": app_obj.application_id, "status": "sent"})

        except Exception as e:
            db.session.rollback()
            results.append({"application_id": app_obj.application_id, "status": f"failed: {str(e)}"})

    return jsonify({"applications": results})
