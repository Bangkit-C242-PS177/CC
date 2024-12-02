import firebase_admin
from firebase_admin import credentials, auth
from app.config import Config

# Inisialisasi Firebase
cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)

def verify_firebase_token(token):
    """
    Verifies a Firebase ID token and returns the decoded token if valid.
    If invalid, returns None.
    """
    try:
        # Verifikasi token Firebase
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except auth.InvalidIdTokenError:
        # Token tidak valid
        print("Invalid Firebase ID token.")
        return None
    except auth.ExpiredIdTokenError:
        # Token sudah kadaluarsa
        print("Firebase ID token has expired.")
        return None
    except Exception as e:
        # Untuk kesalahan lain
        print(f"Error verifying token: {e}")
        return None
