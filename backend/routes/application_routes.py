from flask import Blueprint, jsonify, request

# Blueprint define karo
application_bp = Blueprint("application", __name__, url_prefix="/applications")

# Example route: get all applications (dummy data)
@application_bp.route("/", methods=["GET"])
def get_applications():
    return jsonify([
        {"id": 1, "job_id": 2, "candidate_id": 5, "status": "Applied"},
        {"id": 2, "job_id": 3, "candidate_id": 6, "status": "Reviewed"}
    ])

# Example route: apply to a job
@application_bp.route("/apply", methods=["POST"])
def apply_job():
    data = request.get_json()
    return jsonify({
        "message": f"Application submitted for Job {data.get('job_id')} by Candidate {data.get('candidate_id')}"
    })
