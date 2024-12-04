from datetime import datetime, timedelta
import jwt
import os

# Kunci rahasia untuk encoding dan decoding JWT
JWT_SECRET = os.getenv('JWT_SECRET', 'your_default_secret_key')
JWT_ALGORITHM = 'HS256'

# Set untuk menyimpan JTI yang diblokir
BLOCKLIST = set()

def create_jwt(user_id):
    """
    Membuat JWT untuk pengguna dengan ID tertentu.
    
    Args:
        user_id (str): ID pengguna yang akan disimpan dalam token.

    Returns:
        str: Token JWT yang telah diencode.
    """
    # Pastikan user_id adalah string
    user_id_str = str(user_id)
    
    payload = {
        'sub': user_id_str,  # Menggunakan 'sub' untuk subjek
        'exp': datetime.utcnow() + timedelta(minutes=15),  # Waktu kedaluwarsa token
        'jti': str(uuid.uuid4())  # Menambahkan JTI (JWT ID) untuk pelacakan
    }
    
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token

def decode_jwt(token):
    """
    Mendecode JWT dan mengembalikan payload jika valid.
    
    Args:
        token (str): Token JWT yang akan didecode.

    Returns:
        dict or None: Payload dari token jika valid, None jika tidak valid atau kedaluwarsa.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # Memeriksa apakah token ada dalam blocklist
        if payload['jti'] in BLOCKLIST:
            print("Token telah dicabut")  # Tambahkan logging
            return None  # Token telah dicabut
        
        return payload
    except jwt.ExpiredSignatureError:
        print("Token telah kedaluwarsa")  # Tambahkan logging
        return None  # Token telah kedaluwarsa
    except jwt.InvalidTokenError:
        print("Token tidak valid")  # Tambahkan logging
        return None  # Token tidak valid