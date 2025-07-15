# utils/jwt.py

from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "clave_ultrasecreta"  # Cámbiala por una segura y guárdala en .env
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 60

def crear_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token
