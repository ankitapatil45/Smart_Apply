
from extensions import db

from datetime import datetime

import enum

class ApplicationStatus(enum.Enum):
    PENDING = "pending"
    REJECTED = "rejected"
    SHORTLISTED = "shortlisted"


class Application(db.Model):
    __tablename__ = "application"

    application_id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.job_id", ondelete="CASCADE"), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidate.candidate_id", ondelete="CASCADE"), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    ai_score = db.Column(db.Numeric(5, 2))
    status = db.Column(db.Enum(ApplicationStatus), default=ApplicationStatus.PENDING, nullable=False)

    progress = db.relationship("ApplicationProgress", backref="application", lazy=True, cascade="all, delete-orphan")
    emails = db.relationship("EmailLog", backref="application", lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
      return f"<Application {self.application_id} - Job {self.job_id}>"

