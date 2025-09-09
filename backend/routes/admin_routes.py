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


@admin_bp.route("/hr/<int:hr_id>", methods=["PUT", "DELETE"])
@jwt_required()
def manage_hr(hr_id):
    # ✅ Ensure only Admins can do this
    if not is_admin():
        return jsonify({"error": "Only Admins can manage HR users"}), 403

    # ✅ Fetch HR by ID and ensure role is HR
    hr = CompanyEmployee.query.filter_by(employee_id=hr_id, role=RoleEnum.HR).first()
    if not hr:
        return jsonify({"error": "HR not found"}), 404

    # -------- DELETE --------
    if request.method == "DELETE":
        db.session.delete(hr)
        db.session.commit()
        return jsonify({"message": "HR deleted successfully"}), 200

    # -------- UPDATE --------
    if request.method == "PUT":
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        updated_fields = {}

        # ✅ Update allowed fields
        if "name" in data:
            hr.name = data["name"]
            updated_fields["name"] = data["name"]

        if "phone" in data:
            hr.phone = data["phone"]
            updated_fields["phone"] = data["phone"]

        if "email" in data:
            new_email = data["email"]
            # Check for duplicate email
            if CompanyEmployee.query.filter(
                CompanyEmployee.email == new_email,
                CompanyEmployee.employee_id != hr.employee_id
            ).first():
                return jsonify({"error": "Email already exists"}), 409
            hr.email = new_email
            updated_fields["email"] = new_email

        if "password" in data:
            hr.password_hash = generate_password_hash(data["password"])
            updated_fields["password"] = "updated"

        if updated_fields:
            db.session.commit()

        return jsonify({
            "message": "HR updated successfully",
            "hr": {
                "id": hr.employee_id,
                "name": hr.name,
                "email": hr.email,
                "phone": hr.phone,
                "role": hr.role.value
            },
            "updated_fields": updated_fields
        }), 200
