from app import create_app
from extensions import db
from models.company_employee import CompanyEmployee, RoleEnum
from models.candidate import Candidate, GenderEnum, EducationStatusEnum
from werkzeug.security import generate_password_hash
from datetime import date
 
app = create_app()
 
with app.app_context():
    # Check if admin already exists
    admin = CompanyEmployee.query.filter_by(email="admin1@gmail.com").first()
    if not admin:
        admin = CompanyEmployee(
            name="Administrator",
            email="admin1@gmail.com",
            phone="9999999999",
            role=RoleEnum.ADMIN,
            password_hash=generate_password_hash("admin1")
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created")
    else:
        print("Admin already exists")
 
    # Check if HR already exists
    hr = CompanyEmployee.query.filter_by(email="hr1@gmail.com").first()
    if not hr:
        hr = CompanyEmployee(
            name="HR Manager",
            email="hr1@gmail.com",
            phone="8888888888",
            role=RoleEnum.HR,
            password_hash=generate_password_hash("hr1"),
        )
        db.session.add(hr)
        db.session.commit()
        print("HR created")
    else:
        print("HR already exists")


     # Candidate setup
    # ------- CANDIDATE CREATION -------
    candidate = Candidate.query.filter_by(email="candidate1@gmail.com").first()
    if not candidate:
        candidate = Candidate(
            name="candidate1",
            email="candidate1@gmail.com",
            phone="7777777777",
            password_hash=generate_password_hash("candidate1")
        )
        db.session.add(candidate)
        db.session.commit()
        print("Candidate created")
    else:
        print("Candidate already exists")