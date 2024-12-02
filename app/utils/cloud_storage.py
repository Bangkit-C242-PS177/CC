from google.cloud import storage
import tensorflow as tf
import os
from PIL import Image, UnidentifiedImageError
import numpy as np
from app.config import Config

# Daftar ekstensi file yang diperbolehkan
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Memeriksa apakah ekstensi file termasuk dalam ekstensi yang diperbolehkan."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_cloud_storage(file, filename):
    """Mengunggah file ke Cloud Storage dan mengembalikan URL publik file."""
    try:
        client = storage.Client.from_service_account_json(Config.CLOUD_STORAGE_ADMIN)
        bucket = client.get_bucket(Config.CLOUD_STORAGE_BUCKET)
        blob = bucket.blob(f"data/static/{filename}")
        blob.upload_from_file(file)
        return blob.public_url
    except Exception as e:
        print(f"Error uploading file to Cloud Storage: {e}")
        return None

def delete_file_from_cloud_storage(filename):
    """Menghapus file dari folder 'data/static/' di Cloud Storage."""
    try:
        client = storage.Client.from_service_account_json(Config.CLOUD_STORAGE_ADMIN)
        bucket = client.get_bucket(Config.CLOUD_STORAGE_BUCKET)
        blob = bucket.blob(f"data/static/{filename}")
        blob.delete()
        print(f"File {filename} deleted successfully.")
    except Exception as e:
        print(f"Error deleting file from Cloud Storage: {e}")

def load_model_from_local():
    """Memuat model lokal dari path yang ditentukan di environment variables."""
    try:
        # Path untuk model lokal yang sudah diterapkan melalui Firebase Admin dan Cloud Storage Admin
        skin_conditions_path = Config.MODEL_CONDITIONS
        skin_type_path = Config.MODEL_TYPE

        # Memastikan model tersedia di lokal
        if os.path.exists(skin_conditions_path) and os.path.exists(skin_type_path):
            print("Memuat model dari lokal...")
            model_conditions = tf.keras.models.load_model(skin_conditions_path)
            model_type = tf.keras.models.load_model(skin_type_path)
            print(f"Models loaded successfully: {skin_conditions_path}, {skin_type_path}")
            return model_conditions, model_type
        else:
            print(f"Error: Model files not found. Conditions: {skin_conditions_path}, Type: {skin_type_path}")
            return None, None

    except Exception as e:
        print(f"Error loading model from local path: {e}")
        return None, None

def preprocess_image(file):
    """Fungsi untuk memproses gambar sebelum prediksi."""
    try:
        img = Image.open(file.stream)
        img = img.resize((224, 224))  # Mengubah ukuran gambar sesuai kebutuhan model
        img_array = np.array(img) / 255.0  # Normalisasi pixel ke rentang [0, 1]
        img_array = np.expand_dims(img_array, axis=0)  # Menambahkan dimensi batch
        return img_array
    except Exception as e:
        print(f"Error in preprocessing image: {str(e)}")
        return None

#     return decoded_predictions
def decode_prediction(predictions, labels, not_detected_label="Not Detected"):
    """Decode the prediction results into readable labels with percentages."""
    if predictions is None or len(predictions) == 0:
        return {label: "0.00%" for label in labels}  # Kembalikan semua label dengan 0%

    decoded_predictions = {label: "0.00%" for label in labels}  # Inisialisasi semua label dengan 0%

    # Flatten the prediction to ensure it's a 1D array
    predictions = np.squeeze(predictions)  # Removes dimensions of size 1

    # Ensure that predictions is a numpy array
    if isinstance(predictions, np.ndarray):
        if len(predictions) != len(labels):
            raise ValueError("Length of predictions and labels must match.")

        for i in range(len(predictions)):
            # Menggunakan threshold untuk klasifikasi biner
            if predictions[i] >= 0.5:  
                decoded_predictions[labels[i]] = f"{predictions[i] * 100:.2f}%"
    else:
        raise TypeError("Predictions should be a numpy array.")

    return decoded_predictions