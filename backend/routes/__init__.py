from .auth_routes import auth_bp
from .hr_routes import hr_bp
from .job_routes import job_bp
from .application_routes import application_bp
from .admin_routes import admin_bp
from .candidate_routes import candidate_bp
from routes.home_routes import home_bp
from routes.email_routes import email_bp


def register_routes(app):
    """Register all blueprints with the app."""
    app.register_blueprint(auth_bp)
    app.register_blueprint(hr_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(application_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(candidate_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(email_bp)
