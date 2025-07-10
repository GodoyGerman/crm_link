from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.servicio import Servicio
from schemas.servicio import ServicioCreate, ServicioUpdate, ServicioResponse
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ServicioResponse])
def listar_servicios(db: Session = Depends(get_db)):
    return db.query(Servicio).all()

@router.post("/", response_model=ServicioResponse)
def crear_servicio(servicio: ServicioCreate, db: Session = Depends(get_db)):
    nuevo_servicio = Servicio(**servicio.dict())
    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)
    return nuevo_servicio

@router.get("/{id}", response_model=ServicioResponse)
def obtener_servicio(id: int, db: Session = Depends(get_db)):
    servicio = db.query(Servicio).filter(Servicio.id == id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio   


@router.put("/{id}", response_model=ServicioResponse)
def actualizar_servicio(id: int, servicio: ServicioUpdate, db: Session = Depends(get_db)):
    db_servicio = db.query(Servicio).filter(Servicio.id == id).first()
    if not db_servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    for key, value in servicio.dict(exclude_unset=True).items():
        setattr(db_servicio, key, value)

    db.commit()
    db.refresh(db_servicio)
    return db_servicio

@router.delete("/{id}")
def eliminar_servicio(id: str, db: Session = Depends(get_db)):
    servicio = db.query(Servicio).filter(Servicio.id == id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    db.delete(servicio)
    db.commit()
    return {"message": "Servicio eliminado correctamente"}
