from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)
jwt = JWTManager()

# Set untuk menyimpan JTI yang diblokir
BLOCKLIST = set()

# Inisialisasi JWTManager dengan aplikasi Flask
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

# Register
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    # Validasi input
    if not username or not email or not password or not confirm_password:
        return jsonify({"error": "Username, email, password, dan konfirmasi password diperlukan"}), 400

    if password != confirm_password:
        return jsonify({"error": "Password tidak cocok"}), 400

    try:
        # Cek apakah username atau email sudah terdaftar
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "Username sudah terdaftar"}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email sudah terdaftar"}), 400

        # Hash password dan simpan pengguna baru
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Pengguna berhasil terdaftar"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    # Validasi input
    if not email or not password:
        return jsonify({"error": "Email dan password diperlukan"}), 400

    try:
        # Cek kredensial pengguna
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Kredensial tidak valid"}), 401

        # Membuat token JWT
        access_token = create_access_token(identity=str(user.id))  # Pastikan user.id adalah string

        # Simpan user_id dalam sesi
        session['user_id'] = user.id  # Simpan user_id dalam sesi

        return jsonify({
            "message": "Login berhasil",
            "access_token": access_token,
            "user": {
                "email": user.email,
                "username": user.username,
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Logout
@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Ambil JTI (JWT ID) dari token yang sedang digunakan
    BLOCKLIST.add(jti)  # Tambahkan JTI ke dalam blocklist
    session.pop('user_id', None)  # Hapus user_id dari sesi saat logout
    return jsonify(msg="Logout berhasil"), 200  # Kembalikan respons sukses

# Contoh rute yang dilindungi
@auth_bp.route("/protected", methods=["GET"])
def protected():
    # Cek apakah pengguna sudah login melalui sesi
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Pengguna tidak ditemukan, silakan login"}), 401

    user = User.query.get(user_id)
    
    if user is None:
        return jsonify({"error": "Pengguna tidak ditemukan"}), 404

    return jsonify({
        "message": "Ini adalah rute yang dilindungi",
        "user": {
            "username": user.username,
            "email": user.email
        }
    }), 200