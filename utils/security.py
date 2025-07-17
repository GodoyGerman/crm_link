from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario

SECRET_KEY = "clave_ultrasecreta"  # Usa .env en producción
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        print("Error al decodificar token:", e)
        raise credentials_exception

    user = db.query(Usuario).filter(Usuario.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user

