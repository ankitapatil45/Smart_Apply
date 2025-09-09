from extensions import db

from utils import ist_now
import enum
import pytz


# -------- ENUM DEFINITIONS --------
class GenderEnum(enum.Enum):
    male = "Male"
    female = "Female"
    other = "Other"


class EducationStatusEnum(enum.Enum):
    pursuing = "Pursuing"
    passed_out = "Passed Out"


# -------- MODEL --------
class Candidate(db.Model):
    __tablename__ = "candidate"

    candidate_id = db.Column(db.Integer, primary_key=True)
    
    # Personal Information
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # hashed password
    phone = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Enum(GenderEnum), nullable=True)  # Enum
    address = db.Column(db.Text)
    
    # Identification Details
    aadhar_number = db.Column(db.String(20), unique=True)
    pan_number = db.Column(db.String(20), unique=True)

    # Educational Information
    highest_education = db.Column(db.String(255))
    institute = db.Column(db.String(255))
    passing_year = db.Column(db.Integer)
    education_status = db.Column(db.Enum(EducationStatusEnum), nullable=True)  # Enum

    # Professional Information
    skills = db.Column(db.Text)  # could be comma-separated or JSON
    experience_years = db.Column(db.Float)
    resume_path = db.Column(db.String(255))  # file storage path

    # Additional Information
    preferred_job_role = db.Column(db.String(255))
    expected_salary = db.Column(db.Float)
    willing_to_relocate = db.Column(db.Boolean, default=False)
    linkedin_profile = db.Column(db.String(255))
    github_portfolio = db.Column(db.String(255))

    created_at = db.Column(db.DateTime(timezone=True), default=ist_now)

    # Relationships
    applications = db.relationship("Application", backref="candidate", lazy=True)

    def __repr__(self):
        return f"<Candidate {self.name}>"
