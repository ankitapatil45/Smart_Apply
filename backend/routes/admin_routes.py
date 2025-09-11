from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.company_employee import CompanyEmployee, RoleEnum
from extensions import db
 
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
 
 
# -----------------------------
# Route: Create HR (Only Admin)
# -----------------------------
@admin_bp.route("/create_hr", methods=["POST"])
@jwt_required()
def create_hr():
    current_user_id = get_jwt_identity()   # user_id (string)
    claims = get_jwt()                     # contains role, exp, etc.
 
    # Ensure only Admins can create HR
    if claims.get("role") != "admin":
        return jsonify({"error": "Only Admins can create HR users"}), 403
 
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400
 
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
 
    if not name or not email or not password:
        return jsonify({"error": "Name, email, and password are required"}), 400
 
    # Check duplicate email
    if CompanyEmployee.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409
 
    # Hash password
    hashed_pw = generate_password_hash(password)
 
    # Create HR user
    new_hr = CompanyEmployee(
        name=name,
        email=email,
        phone=phone,
        role=RoleEnum.HR,   # Assign HR role here
        password_hash=hashed_pw,
    )
 
    db.session.add(new_hr)
    db.session.commit()
 
    return jsonify({
        "message": "HR created successfully",
        "hr": {
            "id": new_hr.employee_id,
            "name": new_hr.name,
            "email": new_hr.email,
            "role": new_hr.role.value
        },
        "created_by": current_user_id
    }), 201


#===========================================
#====== Update and Delete Hr by Admin =====
#-==========================================
@admin_bp.route("/hr/<int:hr_id>", methods=["PUT", "DELETE"])
@jwt_required()
def manage_hr(hr_id):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Only Admins can manage HR users"}), 403
 
    hr = CompanyEmployee.query.filter_by(employee_id=hr_id, role=RoleEnum.HR).first()
    if not hr:
        return jsonify({"error": "HR not found"}), 404
 
    # Update HR
    if request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400
 
        if "name" in data:
            hr.name = data["name"]
        if "phone" in data:
            hr.phone = data["phone"]
        if "password" in data:
            hr.password_hash = generate_password_hash(data["password"])
 
        db.session.commit()
 
        return jsonify({
            "message": "HR updated successfully",
            "hr": {
                "id": hr.employee_id,
                "name": hr.name,
                "email": hr.email,
                "phone": hr.phone,
                "role": hr.role.value
            }
        }), 200
 
    # Delete HR
    elif request.method == "DELETE":
        db.session.delete(hr)
        db.session.commit()
        return jsonify({"message": "HR deleted successfully"}), 200
