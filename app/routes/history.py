from flask import Blueprint, request, jsonify, session
from app.models import History, db
from app.utils.cloud_storage import upload_file_to_cloud_storage, delete_file_from_cloud_storage
from app.utils.cloud_storage import load_model_from_local, preprocess_image, decode_prediction
from datetime import datetime
import numpy as np
history_blueprint = Blueprint("history", __name__)

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_id_from_session():
    """Ambil user_id dari sesi login pengguna."""
    user_id = session.get('user_id')  # Ambil user_id dari sesi
    if not user_id:
        raise ValueError("User not logged in")
    return user_id

from flask import Blueprint, request, jsonify
from datetime import datetime
import numpy as np  # Pastikan NumPy diimpor
# Import lainnya yang diperlukan, seperti model dan database
import json

# @history_blueprint.route("/", methods=["POST"])
# def post_scan():
#     """Endpoint untuk melakukan scan dan menyimpan hasil ke database."""
#     try:
#         user_id = get_user_id_from_session()  # Ambil user_id dari sesi

#         # Ambil file gambar dari request
#         file = request.files.get("file")
#         if not file:
#             return jsonify({"error": "Tidak ada file yang diunggah"}), 400

#         # Validasi ekstensi file
#         if not allowed_file(file.filename):
#             return jsonify({"error": "Tipe file tidak valid. Hanya png, jpg, jpeg yang diperbolehkan."}), 400

#         # Buat nama file dengan timestamp
#         timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
#         filename = f"{user_id}_{timestamp}_{file.filename}"

#         # Unggah file ke Cloud Storage
#         public_url = upload_file_to_cloud_storage(file, filename)
#         if public_url is None:
#             return jsonify({"error": "Gagal mengunggah file ke cloud storage."}), 500

#         # Preprocess gambar
#         image_array = preprocess_image(file)
#         if image_array is None:
#             return jsonify({"error": "Gagal melakukan preprocessing gambar"}), 400

#         # Memuat model untuk prediksi
#         model_conditions, model_type = load_model_from_local()

#         # Cek apakah model dimuat dengan benar
#         if model_conditions is None or model_type is None:
#             return jsonify({"error": "Model tidak dimuat dengan benar."}), 500

#         # Prediksi menggunakan model
#         predictions_skin_conditions = model_conditions.predict(image_array)
#         predictions_skin_type = model_type.predict(image_array)

#         # Konversi prediksi ke list jika dalam format numpy array
#         predictions_skin_conditions = predictions_skin_conditions.tolist() if isinstance(predictions_skin_conditions, np.ndarray) else predictions_skin_conditions
#         predictions_skin_type = predictions_skin_type.tolist() if isinstance(predictions_skin_type, np.ndarray) else predictions_skin_type

#         # Dekode hasil prediksi
#         skin_conditions_labels = ["Acne", "Eye Bags"]
#         skin_type_labels = ["Normal", "Oily", "Dry"]

#         decoded_skin_conditions = decode_prediction(predictions_skin_conditions, skin_conditions_labels)
#         decoded_skin_type = decode_prediction(predictions_skin_type, skin_type_labels)

#         # Debugging output
#         print("Decoded Skin Conditions:", decoded_skin_conditions)
#         print("Decoded Skin Type:", decoded_skin_type)

#         # Simpan hasil scan ke database
#         new_entry = History(
#             user_id=user_id,
#             filename=filename,
#             predictions_skin_type=json.dumps(decoded_skin_type),  # Convert dict to JSON string
#             predictions_skin_conditions=json.dumps(decoded_skin_conditions),  # Convert dict to JSON string
#             timestamp=datetime.utcnow(),
#         )
#         db.session.add(new_entry)
#         db.session.commit()

#         # Mengembalikan respons JSON
#         return jsonify({
#             "user_id": user_id,  # Menyertakan user_id
#             "filename": filename,  # Menyertakan nama file
#             "skin_conditions": decoded_skin_conditions,
#             "skin_type": decoded_skin_type,
#             # "image_url": public_url  # Menyertakan URL gambar yang diunggah
#         })

#     except Exception as e:
#         # Menangkap dan mengembalikan error dalam format JSON
#         return jsonify({"error": str(e)}), 500


# @history_blueprint.route("/", methods=["POST"])
# def post_scan():
#     """Endpoint untuk melakukan scan dan menyimpan hasil ke database."""
#     try:
#         user_id = get_user_id_from_session()  # Ambil user_id dari sesi

#         # Ambil file gambar dari request
#         file = request.files.get("file")
#         if not file:
#             return jsonify({"error": "Tidak ada file yang diunggah"}), 400

#         # Validasi ekstensi file
#         if not allowed_file(file.filename):
#             return jsonify({"error": "Tipe file tidak valid. Hanya png, jpg, jpeg yang diperbolehkan."}), 400

#         # Buat nama file dengan timestamp
#         timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
#         filename = f"{user_id}_{timestamp}_{file.filename}"

#         # Unggah file ke Cloud Storage
#         public_url = upload_file_to_cloud_storage(file, filename)
#         if public_url is None:
#             return jsonify({"error": "Gagal mengunggah file ke cloud storage."}), 500

#         # Preprocess gambar
#         image_array = preprocess_image(file)
#         if image_array is None:
#             return jsonify({"error": "Gagal melakukan preprocessing gambar"}), 400

#         # Memuat model untuk prediksi
#         model_conditions, model_type = load_model_from_local()

#         # Cek apakah model dimuat dengan benar
#         if model_conditions is None or model_type is None:
#             return jsonify({"error": "Model tidak dimuat dengan benar."}), 500

#         # Prediksi menggunakan model
#         predictions_skin_conditions = model_conditions.predict(image_array)
#         predictions_skin_type = model_type.predict(image_array)

#         # Dekode hasil prediksi
#         skin_conditions_labels = ["Acne", "Eye Bags", "Normal"]
#         skin_type_labels = ["Oily", "Normal", "Dry"]

#         decoded_skin_conditions = decode_prediction(predictions_skin_conditions, skin_conditions_labels, threshold=0.5)
#         decoded_skin_type = decode_prediction(predictions_skin_type, skin_type_labels, threshold=0.5)

#         # Debugging output
#         print("Decoded Skin Conditions:", decoded_skin_conditions)
#         print("Decoded Skin Type:", decoded_skin_type)

#         # Simpan hasil scan ke database
#         new_entry = History(
#             user_id=user_id,
#             filename=filename,
#             predictions_skin_type=json.dumps(decoded_skin_type),  # Convert nested array to JSON string
#             predictions_skin_conditions=json.dumps(decoded_skin_conditions),  # Convert nested array to JSON string
#             timestamp=datetime.utcnow(),
#         )
#         db.session.add(new_entry)
#         db.session.commit()

#         # Mengembalikan respons JSON
#         return jsonify({
#             "user_id": user_id,
#             "filename": filename,
#             "skin_conditions": decoded_skin_conditions,
#             "skin_type": decoded_skin_type,
#             "image_url": public_url
#         })

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.database import db
from app.models import History
from datetime import datetime
import json

history_blueprint = Blueprint("history", __name__)

<<<<<<< HEAD
# 
@history_blueprint.route("/", methods=["POST"])
@jwt_required(optional=True)  # Mengizinkan akses tanpa token
def post_scan():
    """Endpoint untuk melakukan scan dan menyimpan hasil ke database."""
    try:
        # Ambil user_id dari sesi jika tidak ada token
        user_id = get_jwt_identity()  # Ambil user_id dari token jika ada
        if user_id is None:
            user_id = session.get('user_id')  # Ambil user_id dari sesi jika token tidak ada
        if user_id is None:
            return jsonify({"error": "Pengguna tidak terautentikasi"}), 401
=======
@history_blueprint.route("/", methods=["POST"])
@jwt_required()  # Menambahkan dekorator untuk memastikan pengguna terautentikasi
def post_scan():
    """Endpoint untuk melakukan scan dan menyimpan hasil ke database."""
    try:
        user_id = str(get_jwt_identity())  # Pastikan user_id adalah string
>>>>>>> dfcdb8cb0e780c67bc1cb10cb76be05800989766

        # Ambil file gambar dari request
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "Tidak ada file yang diunggah"}), 400

        # Validasi ekstensi file
        if not allowed_file(file.filename):
            return jsonify({"error": "Tipe file tidak valid. Hanya png, jpg, jpeg yang diperbolehkan."}), 400

        # Buat nama file dengan timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filename = f"{user_id}_{timestamp}_{file.filename}"

        # Unggah file ke Cloud Storage
        public_url = upload_file_to_cloud_storage(file, filename)
        if public_url is None:
            return jsonify({"error": "Gagal mengunggah file ke cloud storage."}), 500

        # Preprocess gambar
        image_array = preprocess_image(file)
        if image_array is None:
            return jsonify({"error": "Gagal melakukan preprocessing gambar"}), 400

        # Memuat model untuk prediksi
        model_conditions, model_type = load_model_from_local()

        # Cek apakah model dimuat dengan benar
        if model_conditions is None or model_type is None:
            return jsonify({"error": "Model tidak dimuat dengan benar."}), 500

        # Prediksi menggunakan model
        predictions_skin_conditions = model_conditions.predict(image_array)
        predictions_skin_type = model_type.predict(image_array)

        # Dekode hasil prediksi
        skin_conditions_labels = ["Acne", "Eye Bags", "Normal"]
        skin_type_labels = ["Oily", "Normal", "Dry"]

        decoded_skin_conditions = decode_prediction(predictions_skin_conditions, skin_conditions_labels, threshold=0.5)
        decoded_skin_type = decode_prediction(predictions_skin_type, skin_type_labels, threshold=0.5)

        # Simpan hasil scan ke database
        new_entry = History(
            user_id=user_id,
            filename=filename,
            predictions_skin_type=json.dumps(decoded_skin_type),
            predictions_skin_conditions=json.dumps(decoded_skin_conditions),
            timestamp=datetime.utcnow(),
        )
        db.session.add(new_entry)
        db.session.commit()

        # Mengembalikan respons JSON
        return jsonify({
            "user_id": user_id,
            "filename": filename,
            "skin_conditions": decoded_skin_conditions,
            "skin_type": decoded_skin_type,
            "image_url": public_url
        }), 201  # Mengembalikan status 201 Created

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@history_blueprint.route("/history", methods=["GET"])
def get_history():
    """Endpoint untuk mendapatkan riwayat scan pengguna."""
    try:
        user_id = get_user_id_from_session()

        # Ambil semua data riwayat berdasarkan user_id
        history_entries = History.query.filter_by(user_id=user_id).order_by(History.timestamp.desc()).all()

        # Konversi data riwayat ke dalam format JSON
        history_data = [
            {
                "id": entry.id,
                "filename": entry.filename,
                "predictions_skin_type": entry.predictions_skin_type,
                "predictions_skin_conditions": entry.predictions_skin_conditions,
                "timestamp": entry.timestamp.isoformat(),
            }
            for entry in history_entries
        ]

        return jsonify({"history": history_data}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 401
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@history_blueprint.route("/delete/<int:id>", methods=["DELETE"])
def delete_history(id):
    """Endpoint untuk menghapus entri riwayat scan."""
    try:
        user_id = get_user_id_from_session()

        # Cari entri history berdasarkan ID dan user_id
        history_entry = History.query.filter_by(id=id, user_id=user_id).first()
        if not history_entry:
            return jsonify({"error": "History not found"}), 404

        # Hapus file dari Cloud Storage
        try:
            delete_file_from_cloud_storage(history_entry.filename)
        except Exception as e:
            return jsonify({"error": f"Failed to delete file from cloud storage: {str(e)}"}), 500

        # Hapus data dari tabel history
        db.session.delete(history_entry)
        db.session.commit()

        return jsonify({"message": "History entry deleted successfully"}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 401
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
