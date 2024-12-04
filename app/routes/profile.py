# from flask import Blueprint, request, jsonify
# from app.models import Profile, User
# from app.utils.database import db
# from app.utils.firebase import verify_firebase_token

# profile_blueprint = Blueprint("profile", __name__)

# # Ambil profil pengguna berdasarkan token
# @profile_blueprint.route("/", methods=["GET"])
# def get_profile():
#     token = request.headers.get("Authorization", "").replace("Bearer ", "")
#     decoded_token = verify_firebase_token(token)
    
#     if not decoded_token:
#         return jsonify({"error": "Invalid token"}), 401

#     user_id = decoded_token["uid"]
#     profile = Profile.query.filter_by(user_id=user_id).first()
    
#     if not profile:
#         return jsonify({"error": "Profile not found"}), 404

#     return jsonify({
#         "full_name": profile.full_name,
#         "phone_number": profile.phone_number,
#         "address": profile.address,
#         "updated_at": profile.updated_at
#     })

# # Perbarui profil pengguna
# @profile_blueprint.route("/edit", methods=["PUT"])
# def edit_profile():
#     token = request.headers.get("Authorization", "").replace("Bearer ", "")
#     decoded_token = verify_firebase_token(token)
    
#     if not decoded_token:
#         return jsonify({"error": "Invalid token"}), 401

#     user_id = decoded_token["uid"]
#     data = request.json
#     profile = Profile.query.filter_by(user_id=user_id).first()

#     if not profile:
#         return jsonify({"error": "Profile not found"}), 404

#     profile.full_name = data.get("full_name", profile.full_name)
#     profile.phone_number = data.get("phone_number", profile.phone_number)
#     profile.address = data.get("address", profile.address)

#     db.session.commit()

#     return jsonify({"message": "Profile updated successfully"})
from flask import Blueprint, request, jsonify
from app.models import Profile, User
from app.utils.database import db
from app.utils.firebase import verify_firebase_token

profile_blueprint = Blueprint("profile", __name__)

# Ambil profil pengguna berdasarkan token
@profile_blueprint.route("/", methods=["GET"])
def get_profile():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    decoded_token = verify_firebase_token(token)
    
    if not decoded_token:
        return jsonify({"error": "Invalid token"}), 401

    user_id = decoded_token["uid"]
    profile = Profile.query.filter_by(user_id=user_id).first()
    
    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    return jsonify({
        "full_name": profile.full_name,  # Pastikan kolom ini ada di model Profile
        "phone_number": profile.phone_number,
        "address": profile.address,
        "updated_at": profile.updated_at.isoformat()  # Format waktu menjadi ISO 8601
    })

# Perbarui profil pengguna
@profile_blueprint.route("/edit", methods=["PUT"])
def edit_profile():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    decoded_token = verify_firebase_token(token)
    
    if not decoded_token:
        return jsonify({"error": "Invalid token"}), 401

    user_id = decoded_token["uid"]
    data = request.json
    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile:
        return jsonify({"error": "Profile not found"}), 404

    # Memperbarui atribut profil
    profile.full_name = data.get("full_name", profile.full_name)
    profile.phone_number = data.get("phone_number", profile.phone_number)
    profile.address = data.get("address", profile.address)

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 200  # Menambahkan status 200 OK