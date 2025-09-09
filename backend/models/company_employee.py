import enum
from extensions import db

from datetime import datetime


class RoleEnum(enum.Enum):
    HR = "hr"
    ADMIN = "admin"


class CompanyEmployee(db.Model):
    __tablename__ = "company_employee"

    employee_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(50))
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.HR, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relationships
    jobs = db.relationship("Job", backref="posted_by_employee", lazy=True)
    progress_updates = db.relationship("ApplicationProgress", backref="updated_by_employee", lazy=True)

    def __repr__(self):
        return f"<CompanyEmployee {self.name} ({self.role.value})>"
