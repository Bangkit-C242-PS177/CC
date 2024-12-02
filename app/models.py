from app.utils.database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firebase_id = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)  # Kolom username
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Kolom password
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relasi dengan Profile
    profile = db.relationship('Profile', backref='user', uselist=False)

    # Relasi dengan History
    history = db.relationship('History', backref='user', lazy=True)


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class History(db.Model):
    __tablename__ = 'history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Relasi dengan tabel users
    filename = db.Column(db.String(100), nullable=False)  # Nama file
    predictions_skin_conditions = db.Column(db.String(200), nullable=False)  # Prediksi kondisi kulit
    predictions_skin_type = db.Column(db.String(200), nullable=False)  # Prediksi jenis kulit
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())  # Waktu dibuat
