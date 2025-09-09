import os
from datetime import timedelta

class Config:
    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:1122@localhost:5432/smart_apply_system"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

    # JWT config
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_TYPE = "Bearer"

    # File upload config
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads/resumes")
    ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}
