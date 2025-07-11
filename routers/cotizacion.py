from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.cotizacion import Cotizacion, CotizacionItem
from schemas.cotizacion import CotizacionCreate, CotizacionOut
from sqlalchemy.orm import joinedload

router = APIRouter(tags=["Cotizaciones"]) 

@router.post("/crear/", response_model=CotizacionOut)
def crear_cotizacion(cotizacion: CotizacionCreate, db: Session = Depends(get_db)):

    db_cotizacion = Cotizacion(
        nombre_cliente=cotizacion.nombre_cliente,
        tipo_identificacion=cotizacion.tipo_identificacion,
        identificacion=cotizacion.identificacion,
        correo=cotizacion.correo,
        direccion=cotizacion.direccion,
        telefono=cotizacion.telefono,
        ciudad=cotizacion.ciudad,
        contacto=cotizacion.contacto,
        condiciones=cotizacion.condiciones,
        fecha_emision=cotizacion.fecha_emision,
        valida_hasta=cotizacion.valida_hasta,
        estado=cotizacion.estado,
        pdf_url=cotizacion.pdf_url,
        subtotal=cotizacion.subtotal,
        iva=cotizacion.iva,
        total=cotizacion.total
    )

    # Agregar los items (relación 1-n)
    for item in cotizacion.items:
        db_item = CotizacionItem(
            servicio=item.servicio,
            cantidad=item.cantidad,
            unidad=item.unidad,
            precio_unitario=item.precio_unitario,
            subtotal=item.subtotal
        )
        db_cotizacion.items.append(db_item)

    db.add(db_cotizacion)
    db.commit()
    db.refresh(db_cotizacion)

    return db_cotizacion


@router.get("/consulta/", response_model=List[CotizacionOut])
def listar_cotizaciones(db: Session = Depends(get_db)):
    cotizaciones = db.query(Cotizacion).options(joinedload(Cotizacion.items)).all()
    return cotizaciones
