from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.cliente import Cliente
from schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from typing import List
from schemas.cliente import ClienteOut
from utils.security import get_current_user
from models.usuario import Usuario

router = APIRouter()

# Obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ClienteResponse)
def crear_cliente(
    cliente: ClienteCreate, 
    db: Session = Depends(get_db), 
    usuario_actual: Usuario = Depends(get_current_user)  # Protege el endpoint
):
    # Aquí podrías validar roles si quieres, por ejemplo:
    # if usuario_actual.rol != "admin":
    #     raise HTTPException(status_code=403, detail="No autorizado")

    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    # Aquí current_user es el usuario autenticado
    return db.query(Cliente).filter(Cliente.activo == True).all()

@router.put("/{id}", response_model=ClienteResponse)
def actualizar_cliente(
    id: int,
    cliente_update: ClienteUpdate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),  # Protección JWT
):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    for key, value in cliente_update.dict(exclude_unset=True).items():
        setattr(cliente, key, value)

    db.commit()
    db.refresh(cliente)
    return cliente

@router.delete("/{id}")
def eliminar_cliente(
    id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),  # Protección JWT
):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    db.delete(cliente)
    db.commit()
    return {"message": "Cliente eliminado correctamente"}



@router.get("/{cliente_id}", response_model=ClienteOut)
def obtener_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),  # Protección JWT
):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.get("/clientes/buscar/")
def buscar_cliente_por_documento(
    numero_identificacion: str,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user),  # Protección JWT
):
    cliente = db.query(Cliente).filter(Cliente.numero_identificacion == numero_identificacion).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente