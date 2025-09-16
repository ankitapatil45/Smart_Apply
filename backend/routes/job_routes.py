from flask import Blueprint, jsonify, request

# Blueprint define karo
job_bp = Blueprint("job", __name__, url_prefix="/jobs")


