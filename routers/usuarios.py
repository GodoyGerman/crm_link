from fastapi import APIRouter, Depends
from models.usuario import Usuario
from utils.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.usuario import UsuarioCreate, UsuarioOut
from models.usuario import Usuario
from database import get_db
import bcrypt
from schemas.usuario import UsuarioUpdate
from models.usuario import Usuario
from schemas.usuario import UsuarioOut
from typing import List


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)
@router.get("/", response_model=List[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db), usuario_actual: Usuario = Depends(get_current_user)):
    # Opcional: aquí puedes validar permisos, por ejemplo solo admin puede listar usuarios
    usuarios = db.query(Usuario).all()
    return usuarios

@router.get("/perfil")
def leer_perfil(usuario_actual: Usuario = Depends(get_current_user)):
    return {
        "id": usuario_actual.id,
        "nombre": usuario_actual.nombre,
        "correo": usuario_actual.correo,
        "rol": usuario_actual.rol,
    }

@router.get("/{id}", response_model=UsuarioOut)
def obtener_usuario(id: int, db: Session = Depends(get_db), usuario_actual: Usuario = Depends(get_current_user)):
    usuario = db.query(Usuario).filter(Usuario.id == id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario




@router.post("/registrar", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar si el correo ya existe
    usuario_existente = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    # Encriptar la contraseña
    contraseña_hash = bcrypt.hashpw(usuario.contraseña.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

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



@router.put("/{usuario_id}", response_model=UsuarioOut)
def actualizar_usuario(
    usuario_id: int,
    usuario_update: UsuarioUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Si el correo está siendo actualizado, verificar duplicados
    if usuario_update.correo and usuario_update.correo != usuario.correo:
        existe = db.query(Usuario).filter(Usuario.correo == usuario_update.correo).first()
        if existe:
            raise HTTPException(status_code=400, detail="El nuevo correo ya está en uso")

    # Actualizar campos
    for key, value in usuario_update.dict(exclude_unset=True).items():
        setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)

    return usuario


@router.delete("/{usuario_id}")
def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()

    return {"mensaje": "Usuario eliminado correctamente"}
