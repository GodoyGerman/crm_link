# routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.usuario import UsuarioCreate, UsuarioOut
from models.usuario import Usuario
from database import get_db
import bcrypt
from schemas.usuario import LoginRequest, TokenResponse
from utils.jwt import crear_token


router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/registro", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe un usuario con ese correo
    usuario_existente = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado."
        )

    # Hashear la contraseña
    contraseña_hash = bcrypt.hashpw(usuario.contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Crear nuevo usuario
    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        contraseña_hash=contraseña_hash,
        rol=usuario.rol,
        activo=usuario.activo
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario

# routers/auth.py



@router.post("/login", response_model=TokenResponse)
def login(datos: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.correo == datos.correo).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if not bcrypt.checkpw(datos.contraseña.encode('utf-8'), usuario.contraseña_hash.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Crear token con el ID del usuario y su rol
    token = crear_token({
        "sub": str(usuario.id),
        "rol": usuario.rol,
        "correo": usuario.correo
    })

    return TokenResponse(access_token=token)
