import os
from google.cloud import storage
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")
    
    # Cloud SQL Connection Information
    CLOUD_SQL_CONNECTION_NAME = os.environ.get(
        "CLOUD_SQL_CONNECTION_NAME",
        "fourth-walker-434012:asia-southeast2:appdatabase"
    )
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "k3r3n")
    DB_NAME = os.environ.get("DB_NAME", "appdatabase")
    DB_HOST = os.environ.get("DB_HOST", "34.101.161.175")  # Public IP address

    # Database URI for Public IP connection
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", 
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cloud Storage bucket name
    CLOUD_STORAGE_BUCKET = os.environ.get("CLOUD_STORAGE_BUCKET", "urskin-app")

    # Base directory local file
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Path to Firebase service account file
    FIREBASE_CREDENTIALS_PATH = os.environ.get(
        "FIREBASE_CREDENTIALS", 
        os.path.join(BASE_DIR, '..', 'migrations', 'firebase-account-storage.json')
    )

    # Path to Cloud Storage Admin
    CLOUD_STORAGE_ADMIN = os.environ.get(
        "CLOUD_STORAGE_ADMIN",
        os.path.join(BASE_DIR, '..', 'migrations', 'storage-account.json')
    )
    
    # Path to Model local Conditions Machine Learning
    MODEL_CONDITIONS = os.environ.get(
        "CONDITIONS",
        os.path.join(BASE_DIR, '..', 'migrations', 'model', 'skin_conditions_model.h5')
    )

    MODEL_TYPE = os.environ.get(
        "TYPE",
        os.path.join(BASE_DIR, '..', 'migrations', 'model', 'skin_type_model.h5')
    )
