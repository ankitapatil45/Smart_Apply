from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, migrate, jwt, revoked_tokens   # ✅ import from extensions
from routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})

    # Register token revocation callback
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return jwt_payload["jti"] in revoked_tokens

    # Register all routes
    register_routes(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
