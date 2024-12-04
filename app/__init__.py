# app/__init__.py

from flask import Flask
from app.config import Config
from flask_jwt_extended import JWTManager
# from flask_migrate import Migrate  # Import Flask-Migrate
from app.utils.database import db
from app.routes import auth_bp, history_blueprint, profile_blueprint  # Sesuaikan nama import blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'your_secure_secret_key' 

    # Inisialisasi database
    db.init_app(app)
    jwt = JWTManager(app)

    # migrate = Migrate(app, db)

    # Daftarkan blueprint dengan prefix URL masing-masing
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(history_blueprint, url_prefix="/api/scan")
    app.register_blueprint(profile_blueprint, url_prefix="/api/profile")

    return app

