from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.company_employee import CompanyEmployee, RoleEnum
from models import  Candidate
from extensions import db
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt
from extensions import revoked_tokens
from datetime import timedelta
 
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
 
 
# -----------------------------
# Route: Register Admin (Only once)
# -----------------------------
@auth_bp.route("/register-admin", methods=["POST"])
def register_admin():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400
 
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
 
    if not name or not email or not password:
        return jsonify({"error": "Name, email and password are required"}), 400
 
    # Prevent multiple admins
    admin_exists = CompanyEmployee.query.filter_by(role=RoleEnum.ADMIN).first()
    if admin_exists:
        return jsonify({"error": "An Admin already exists. Only one Admin can be created this way."}), 403
 
    if CompanyEmployee.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
 
    hashed_pw = generate_password_hash(password)
 
    new_admin = CompanyEmployee(
        name=name,
        email=email,
        phone=phone,
        role=RoleEnum.ADMIN,
        password_hash=hashed_pw,
    )
 
    db.session.add(new_admin)
    db.session.commit()
 
    return jsonify({
        "message": "Admin registered successfully",
        "employee": {
            "id": new_admin.employee_id,
            "name": new_admin.name,
            "email": new_admin.email,
            "role": new_admin.role.value,
        }
    }), 201
 
 
# -----------------------------
# Route: Login (Admin / HR / Candidate)
# -----------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400
 
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")  # must be selected manually: "admin", "hr", "candidate"
 
    if not email or not password or not role:
        return jsonify({"error": "Email, password, and role are required"}), 400
 
    role = role.lower()
    user = None
 
    if role in ["admin", "hr"]:
        user = CompanyEmployee.query.filter_by(email=email, role=RoleEnum(role)).first()
    elif role == "candidate":
        user = Candidate.query.filter_by(email=email).first()
    else:
        return jsonify({"error": "Invalid role. Choose 'admin', 'hr', or 'candidate'."}), 400
 
    if not user:
        return jsonify({"error": f"{role.capitalize()} not found"}), 404
 
    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401
 
    # FIXED: identity is user_id (string), role in claims
    access_token = create_access_token(
        identity=str(user.employee_id if role in ["admin", "hr"] else user.candidate_id),
        additional_claims={"role": role},
        expires_delta=timedelta(hours=12)
    )
 
    return jsonify({
        "message": f"{role.capitalize()} logged in successfully",
        "access_token": access_token,
        "user": {
            "id": user.employee_id if role in ["admin", "hr"] else user.candidate_id,
            "name": getattr(user, "name", getattr(user, "full_name", None)),
            "email": user.email,
            "role": role
        }
    }), 200


#-------------- CANDIDATE REGISTER-------------
@auth_bp.route("/register_candidate", methods=["POST"])
def register_candidate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing request body"}), 400
 
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
 
    if not name or not email or not password:
        return jsonify({"error": "Name, email and password are required"}), 400
 
    # Check if email already exists
    if Candidate.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
 
    hashed_pw = generate_password_hash(password)
 
    new_candidate = Candidate(
        name=name,
        email=email,
        phone=phone,
        password_hash=hashed_pw,
    )
 
    db.session.add(new_candidate)
    db.session.commit()
 
    return jsonify({
        "message": "Candidate registered successfully",
        "candidate": {
            "id": new_candidate.candidate_id,
            "name": new_candidate.name,
            "email": new_candidate.email,
            "phone": new_candidate.phone,
        }
    }), 201
 

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    revoked_tokens.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200




