from flask import Flask
from app.db import initialize_db
from app.auth import auth_bp

def create_app():
    app = Flask(__name__)
    initialize_db()
    app.register_blueprint(auth_bp)
    return app
