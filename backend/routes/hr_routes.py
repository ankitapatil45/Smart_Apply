from flask import Blueprint


from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import  Job, JobStatus, CompanyEmployee
from extensions import db

hr_bp = Blueprint("hr", __name__, url_prefix="/hr")


#==========================
#=====  jobs Posting =======
#===========================
@hr_bp.route("/job_posting", methods=["POST"])
@jwt_required()
def create_or_update_job():
    claims = get_jwt()
    if claims.get("role") != "hr":
        return jsonify({"error": "Only HRs can manage jobs"}), 403

    current_user_id = get_jwt_identity()
    data = request.get_json() or {}

    job_id = data.get("job_id")   # ✅ If present → update, else → new
    title = data.get("title")
    description = data.get("description")
    requirements = data.get("requirements")
    location = data.get("location")
    status_str = data.get("status", "draft").lower()  # default draft

    #  Validate status
    try:
        status = JobStatus(status_str)
    except ValueError:
        return jsonify({"error": f"Invalid status. Allowed: {[s.value for s in JobStatus]}"}), 400

    #  If updating existing job
    if job_id:
        job = Job.query.filter_by(job_id=job_id, posted_by=current_user_id).first()
        if not job:
            return jsonify({"error": "Job not found or not owned by you"}), 404

        if title: job.title = title
        if description: job.description = description
        if requirements: job.requirements = requirements
        if location: job.location = location
        job.status = status

        db.session.commit()
        return jsonify({"message": f"Job {job.job_id} updated", "status": job.status.value}), 200

    #  If creating new job
    if not title or not description:
        return jsonify({"error": "Title and description are required"}), 400

    new_job = Job(
        title=title,
        description=description,
        requirements=requirements,
        location=location,
        posted_by=current_user_id,
        status=status
    )
    db.session.add(new_job)
    db.session.commit()

    return jsonify({
        "message": "Job created successfully",
        "job": {
            "id": new_job.job_id,
            "title": new_job.title,
            "status": new_job.status.value,
            "posted_by": new_job.posted_by
        }
    }), 201


#==========================
#===== List of jobs =======
#===========================
@hr_bp.route("/jobs", methods=["GET"])
@jwt_required()
def get_all_jobs():
    # anyone logged in (admin/hr/candidate) can view jobs
    jobs = Job.query.all()
 
    job_list = []
    for job in jobs:
        job_list.append({
            "id": job.job_id,
            "title": job.title,
            "description": job.description,
            "requirements": job.requirements,
            "location": job.location,
            "status": job.status.value if job.status else None,  # Enum -> string
            "is_active": (job.status == JobStatus.ACTIVE),       # ✅ direct check
            "posted_by": job.posted_by,
            "created_at": job.created_at.isoformat() if job.created_at else None
        })
 
    return jsonify({"jobs": job_list}), 200
