from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models.job import Job, JobStatus   # 👈 Directly import from job.py
 
home_bp = Blueprint("home", __name__, url_prefix="/home")
 
#==============================
#===== List of Active Jobs for All  ==
#==============================
@home_bp.route("/jobs", methods=["GET"])
def get_active_jobs_for_candidates():
    """Return only active jobs for candidates"""
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
 
    return jsonify({"jobs": job_list}), 200
 