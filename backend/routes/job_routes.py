from flask import Blueprint, jsonify, request

# Blueprint define karo
job_bp = Blueprint("job", __name__, url_prefix="/jobs")

# Example route: get all jobs (dummy data abhi ke liye)
@job_bp.route("/", methods=["GET"])
def get_jobs():
    return jsonify([
        {"id": 1, "title": "Data Analyst"},
        {"id": 2, "title": "Backend Developer"}
    ])

# Example route: create job
@job_bp.route("/create", methods=["POST"])
def create_job():
    data = request.get_json()
    return jsonify({"message": f"Job created with title {data.get('title')}"})
