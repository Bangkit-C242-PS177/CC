from flask_sqlalchemy import SQLAlchemy

# Inisialisasi objek SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """
    Fungsi untuk menginisialisasi database pada aplikasi Flask.
    Menyambungkan SQLAlchemy dengan Flask app.
    """
    db.init_app(app)
