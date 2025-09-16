from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from models import  Candidate, Job, Application
from models.application import ApplicationStatus
from models.job import JobStatus
from extensions import db
from models.candidate import GenderEnum, EducationStatusEnum
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
import os
 
 
candidate_bp = Blueprint("candidate", __name__, url_prefix="/candidate")
 
 
def allowed_file(filename):
    """Check if file extension is allowed"""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )
 
 
@candidate_bp.route("/form/<int:candidate_id>/complete-profile", methods=["PUT"])
@jwt_required()
def complete_profile(candidate_id):
    current_user_id = get_jwt_identity()
 
    # Ensure only the logged-in candidate can update their profile
    if int(current_user_id) != int(candidate_id):
        return jsonify({"error": "Unauthorized"}), 403
 
    candidate = Candidate.query.get_or_404(candidate_id)
 
    data = request.form
 
    # -------- Personal Information --------
    if "date_of_birth" in data:
        try:
            candidate.date_of_birth = datetime.strptime(
                data["date_of_birth"], "%Y-%m-%d"
            ).date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
 
    if "gender" in data:
        try:
            candidate.gender = GenderEnum[data["gender"].lower()]
        except KeyError:
            return jsonify(
                {"error": f"Invalid gender. Allowed: {[g.name for g in GenderEnum]}"}
            ), 400
 
    candidate.address = data.get("address")
    candidate.aadhar_number = data.get("aadhar_number")
    candidate.pan_number = data.get("pan_number")
 
    # -------- Education --------
    candidate.highest_education = data.get("highest_education")
    candidate.institute = data.get("institute")
    candidate.passing_year = data.get("passing_year")
    if "education_status" in data:
        try:
            candidate.education_status = EducationStatusEnum[
                data["education_status"].lower()
            ]
        except KeyError:
            return jsonify(
                {
                    "error": f"Invalid education_status. Allowed: {[e.name for e in EducationStatusEnum]}"
                }
            ), 400
 
    # -------- Professional --------
    candidate.skills = data.get("skills")
    candidate.experience_years = data.get("experience_years")
 
    # -------- Resume Upload --------
    if "resume" in request.files:
        file = request.files["resume"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        if not allowed_file(file.filename):
            return jsonify(
                {
                    "error": f"Invalid file type. Allowed: {current_app.config['ALLOWED_EXTENSIONS']}"
                }
            ), 400
 
        filename = secure_filename(file.filename)
 
        # Ensure uploads/resumes folder exists
        upload_dir = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_dir, exist_ok=True)
 
        # Save file
        save_path = os.path.join(upload_dir, filename)
        file.save(save_path)
 
        # Store relative path in DB
        candidate.resume_path = os.path.relpath(save_path, os.getcwd())
 
    # -------- Additional Information --------
    candidate.preferred_job_role = data.get("preferred_job_role")
    candidate.expected_salary = data.get("expected_salary")
    candidate.willing_to_relocate = data.get("willing_to_relocate")
    candidate.linkedin_profile = data.get("linkedin_profile")
    candidate.github_portfolio = data.get("github_portfolio")
 
    db.session.commit()
 
    return jsonify(
        {
            "message": "Profile completed successfully",
            "resume_path": candidate.resume_path,
        }
    )
 
 
#==============================
#===== List of Active Jobs (Candidate only) ==
#==============================
@candidate_bp.route("/jobs", methods=["GET"])
@jwt_required()
def get_active_jobs_for_candidates():
    """Return only active jobs for candidates"""
    current_user_id = get_jwt_identity()
    claims = get_jwt()
 
    # Ensure only candidates can access
    if claims.get("role") != "candidate":
        return jsonify({"error": "Only candidates can view this"}), 403
 
    # Fetch candidate info
    candidate = Candidate.query.get(current_user_id)
 
    # Fetch active jobs
    active_jobs = Job.query.filter_by(status=JobStatus.ACTIVE).all()
 
    job_list = []
    for job in active_jobs:
        job_list.append({
            "id": job.job_id,
            "title": job.title,
            "description": job.description,
            "requirements": job.requirements,
            "location": job.location,
            "status": job.status.value,  
            "posted_by": job.posted_by,
            "created_at": job.created_at.isoformat() if job.created_at else None
        })
 
    return jsonify({
        "candidate": {
            "id": candidate.candidate_id,
            "name": candidate.name,
            "email": candidate.email,
            "role": "candidate"
        },
        "jobs": job_list
    }), 200
 
 

#=-----------------------------------
#------ Apply Job by candidate----
#--------------------------------------
@candidate_bp.route("/apply/<int:job_id>", methods=["POST"])
@jwt_required()
def apply_for_job(job_id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()

    #  Ensure only candidates can apply
    if claims.get("role") != "candidate":
        return jsonify({"error": "Only candidates can apply for jobs"}), 403

    # Check if the job exists
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    # Ensure the job is active
    if job.status != JobStatus.ACTIVE:
        return jsonify({"error": "This job is not open for applications"}), 400

    # Prevent duplicate applications
    existing_application = Application.query.filter_by(
        job_id=job_id,
        candidate_id=current_user_id
    ).first()

    if existing_application:
        return jsonify({"error": "You have already applied to this job"}), 400

    # Create new application
    new_application = Application(
        job_id=job_id,
        candidate_id=current_user_id,
        status=ApplicationStatus.PENDING
    )

    db.session.add(new_application)
    db.session.commit()

    return jsonify({
        "message": "Application submitted successfully",
        "application": {
            "application_id": new_application.application_id,
            "job_id": job_id,
            "candidate_id": current_user_id,
            "status": new_application.status.value,
            "applied_at": new_application.applied_at.isoformat()
        }
    }), 201


# ---------------------------------------------------
# GET Candidate Basic Profile (id, name, email, phone)
# ---------------------------------------------------
@candidate_bp.route("/profile/<int:candidate_id>", methods=["GET"])
@jwt_required()
def get_profile(candidate_id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
 
    # Candidate khud ka hi profile access kare
    if claims.get("role") != "candidate" or int(current_user_id) != int(candidate_id):
        return jsonify({"error": "Unauthorized"}), 403
 
    candidate = Candidate.query.get_or_404(candidate_id)
 
    return jsonify({
        "message": "Candidate profile fetched successfully",
        "candidate": {
            "id": candidate.candidate_id,
            "name": candidate.name,
            "email": candidate.email,
            "phone": candidate.phone
        }
    }), 200