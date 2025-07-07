# routers/cotizacion.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.cotizacion import Cotizacion
from schemas.cotizacion import CotizacionCreate, CotizacionUpdate, CotizacionOut
from typing import List
from fastapi.responses import FileResponse
from utils.pdf_generator import generar_pdf
from datetime import datetime
import os
from fastapi.responses import FileResponse
from jinja2 import Template
from pathlib import Path


router = APIRouter(prefix="/cotizaciones", tags=["Cotizaciones"])



# Dependencia para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear cotización
@router.post("/", response_model=CotizacionOut)
def crear_cotizacion(cotizacion: CotizacionCreate, db: Session = Depends(get_db)):
    nueva = Cotizacion(**cotizacion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

# Listar todas
@router.get("/", response_model=List[CotizacionOut])
def listar_cotizaciones(db: Session = Depends(get_db)):
    return db.query(Cotizacion).all()

# Obtener una por ID
@router.get("/{cotizacion_id}", response_model=CotizacionOut)
def obtener_cotizacion(cotizacion_id: int, db: Session = Depends(get_db)):
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    return cotizacion

# Actualizar
@router.put("/{cotizacion_id}", response_model=CotizacionOut)
def actualizar_cotizacion(cotizacion_id: int, datos: CotizacionUpdate, db: Session = Depends(get_db)):
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    for campo, valor in datos.dict().items():
        setattr(cotizacion, campo, valor)
    db.commit()
    db.refresh(cotizacion)
    return cotizacion

# Eliminar
@router.delete("/{cotizacion_id}")
def eliminar_cotizacion(cotizacion_id: int, db: Session = Depends(get_db)):
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    db.delete(cotizacion)
    db.commit()
    return {"mensaje": "Cotización eliminada exitosamente"}



