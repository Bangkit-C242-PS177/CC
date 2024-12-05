from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'users'  # Menambahkan nama tabel
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relasi dengan Profile
    profile = db.relationship('Profile', backref='owner', uselist=False, cascade="all, delete-orphan")

    # Relasi dengan History
    history = db.relationship('History', back_populates='user', lazy=True, cascade="all, delete-orphan")


class Profile(db.Model):
    __tablename__ = 'profiles'  # Menambahkan nama tabel
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phone_number = db.Column(db.String(20))
    address = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relasi kembali ke User
    # Tidak perlu mendefinisikan relasi kembali ke User jika sudah ada backref di User
    # user = db.relationship('User  ', back_populates='profile')


class History(db.Model):
    __tablename__ = 'history'  # Menambahkan nama tabel
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Relasi dengan tabel users
    filename = db.Column(db.String(100), nullable=False)  # Nama file
    predictions_skin_conditions = db.Column(db.String(200), nullable=False)  # Prediksi kondisi kulit
    predictions_skin_type = db.Column(db.String(200), nullable=False)  # Prediksi jenis kulit
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Waktu dibuat

    # Menambahkan relasi kembali ke User
    user = db.relationship('User', back_populates='history')