from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from models import  Candidate
from extensions import db
from models.candidate import GenderEnum, EducationStatusEnum
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import os

candidate_bp = Blueprint("candidate", __name__, url_prefix="/candidate")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


@candidate_bp.route("/form/<int:candidate_id>/complete-profile", methods=["PUT"])
@jwt_required()
def complete_profile(candidate_id):
    current_user_id = get_jwt_identity()

    # Ensure only the logged-in candidate can update their profile
    if int(current_user_id) != int(candidate_id):
        return jsonify({"error": "Unauthorized"}), 403

    candidate = Candidate.query.get_or_404(candidate_id)

    # Use request.form for text fields and request.files for resume
    data = request.form

    # -------- Personal Information --------
    if "date_of_birth" in data:
        try:
            candidate.date_of_birth = datetime.strptime(data["date_of_birth"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    if "gender" in data:
        try:
            candidate.gender = GenderEnum[data["gender"].lower()]
        except KeyError:
            return jsonify({"error": f"Invalid gender. Allowed: {[g.name for g in GenderEnum]}"}), 400

    candidate.address = data.get("address")
    candidate.aadhar_number = data.get("aadhar_number")
    candidate.pan_number = data.get("pan_number")

    # -------- Education --------
    candidate.highest_education = data.get("highest_education")
    candidate.institute = data.get("institute")
    candidate.passing_year = data.get("passing_year")
    if "education_status" in data:
        try:
            candidate.education_status = EducationStatusEnum[data["education_status"].lower()]
        except KeyError:
            return jsonify({"error": f"Invalid education_status. Allowed: {[e.name for e in EducationStatusEnum]}"}), 400

    # -------- Professional --------
    candidate.skills = data.get("skills")
    candidate.experience_years = data.get("experience_years")

    # -------- Resume Upload --------
    if "resume" in request.files:
        file = request.files["resume"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400
        if not allowed_file(file.filename):
            return jsonify({"error": f"Invalid file type. Allowed: {current_app.config['ALLOWED_EXTENSIONS']}"}), 400

        filename = secure_filename(file.filename)
        os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)
        candidate.resume_path = save_path

    # -------- Additional Information --------
    candidate.preferred_job_role = data.get("preferred_job_role")
    candidate.expected_salary = data.get("expected_salary")
    candidate.willing_to_relocate = data.get("willing_to_relocate")
    candidate.linkedin_profile = data.get("linkedin_profile")
    candidate.github_portfolio = data.get("github_portfolio")

    db.session.commit()

    return jsonify({
        "message": "Profile completed successfully",
        "resume_path": candidate.resume_path
    })
