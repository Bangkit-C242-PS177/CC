from flask import Blueprint, request, jsonify, session
from firebase_admin import auth
from app.utils.database import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# Register
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if not username or not email or not password or not confirm_password:
        return jsonify({"error": "Username, email, password, and confirm password are required"}), 400

    # Verifikasi password dan confirm password
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    try:
        # Membuat pengguna di Firebase Auth
        firebase_user = auth.create_user(email=email, password=password)
        firebase_id = firebase_user.uid

        # Cek apakah username atau email sudah terdaftar
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username already exists"}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already exists"}), 400

        # Menyimpan pengguna baru ke database
        hashed_password = generate_password_hash(password)  # Hash password sebelum menyimpannya
        new_user = User(firebase_id=firebase_id, username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        # Cari pengguna berdasarkan username
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        # Verifikasi password
        if not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid credentials"}), 401

        # Setelah login berhasil, simpan user_id ke sesi
        session['user_id'] = user.id  # Menyimpan user_id ke sesi

        return jsonify({
            "message": "Login successful",
            "user": {
                "email": user.email,
                "username": user.username,
                "firebase_id": user.firebase_id,
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Reset password (untuk mengirimkan link reset password)
@auth_bp.route("/reset_password", methods=["POST"])
def reset_password():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        # Cek apakah email terdaftar
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Email not found"}), 404

        # Generate password reset link using Firebase Auth
        reset_link = auth.generate_password_reset_link(email)

        return jsonify({
            "message": "Password reset link has been sent to your email.",
            "reset_link": reset_link
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
