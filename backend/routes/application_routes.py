from flask import Blueprint, request, jsonify
from extensions import db
from models import Application
from models.application import ApplicationStatus
from smart_apply import process_application  # your function that takes application_id

application_bp = Blueprint("application", __name__, url_prefix="/applications")

@application_bp.route("/process/<int:job_id>", methods=["POST"])
def process_job_applications(job_id):
    try:
        # Fetch all applications for this job
        applications = Application.query.filter_by(job_id=job_id).all()
        if not applications:
            return jsonify({"message": "No applications found for this job"}), 404

        results = []
        for app_obj in applications:
            # Process each application individually
            processed_app = process_application(app_obj.application_id)
            results.append({
                "application_id": processed_app.application_id,
                "candidate_id": processed_app.candidate_id,
                "ai_score": float(processed_app.ai_score),
                "status": processed_app.status.value
            })

        return jsonify({"job_id": job_id, "applications": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 400
