from extensions import db
from datetime import datetime
from .application import ApplicationStatus  # import Enum from Application model

class ApplicationProgress(db.Model):
    __tablename__ = "application_progress"

    progress_id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(
        db.Integer, 
        db.ForeignKey("application.application_id", ondelete="CASCADE"), 
        nullable=False
    )
    status = db.Column(db.Enum(ApplicationStatus), nullable=False)  # ✅ Enum instead of String
    updated_by = db.Column(
        db.Integer, 
        db.ForeignKey("company_employee.employee_id", ondelete="SET NULL")
    )
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f"<ApplicationProgress {self.status.value} @ {self.updated_at}>"



# Status: SHORTLISTED

# Notes: "Candidate matched 90% of requirements, shortlisted for interview."

# Status: INTERVIEW

# Notes: "First-round interview scheduled on 12th Sept at 3:00 PM."

# Status: REJECTED

# Notes: "Rejected due to lack of Python experience."

# Status: HIRED

# Notes: "Candidate accepted offer, joining on 1st Oct."