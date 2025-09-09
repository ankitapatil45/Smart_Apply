from extensions import db

from datetime import datetime
import enum


class JobStatus(enum.Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    DRAFT = "draft"
    ARCHIVED = "archived"


class Job(db.Model):
    __tablename__ = "job"

    job_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    location = db.Column(db.String(255), index=True)

    posted_by = db.Column(
        db.Integer,
        db.ForeignKey("company_employee.employee_id", ondelete="SET NULL")
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    status = db.Column(db.Enum(JobStatus), default=JobStatus.ACTIVE, nullable=False)

    # Relationships
    applications = db.relationship("Application", backref="job", lazy=True)

    def __repr__(self):
        return f"<Job {self.title} (ID: {self.job_id}, Status: {self.status.value})>"
