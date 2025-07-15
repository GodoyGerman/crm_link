from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.cotizacion import Cotizacion, CotizacionItem
from schemas.cotizacion import CotizacionCreate, CotizacionUpdate, CotizacionOut
from sqlalchemy.orm import joinedload
from utils.email import enviar_cotizacion_por_correo

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

@router.get("/{cotizacion_id}", response_model=CotizacionOut)
def obtener_cotizacion(cotizacion_id: int, db: Session = Depends(get_db)):
    cotizacion = db.query(Cotizacion).options(joinedload(Cotizacion.items)).filter(Cotizacion.id == cotizacion_id).first()
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    return cotizacion

@router.get("/consulta/", response_model=List[CotizacionOut])
def listar_cotizaciones(db: Session = Depends(get_db)):
    cotizaciones = db.query(Cotizacion).options(joinedload(Cotizacion.items)).all()
    return cotizaciones

@router.post("/enviar-correo")
async def enviar_pdf_correo(
    correo: str = Form(...),
    pdf: UploadFile = File(...)
):
    contenido_pdf = await pdf.read()
    await enviar_cotizacion_por_correo(correo, contenido_pdf, pdf.filename)
    return {"mensaje": "Correo enviado correctamente"}

@router.put("/actualizar-estado/{cotizacion_id}")
def actualizar_estado(cotizacion_id: int, nuevo_estado: str, db: Session = Depends(get_db)):
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    
    cotizacion.estado = nuevo_estado
    db.commit()
    return {"mensaje": "Estado actualizado", "estado": cotizacion.estado}

@router.put("/actualizar/{cotizacion_id}", response_model=CotizacionOut)
def actualizar_cotizacion(cotizacion_id: int, datos: CotizacionUpdate, db: Session = Depends(get_db)):
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")

    # Actualizar datos básicos de cotización excepto items
    datos_dict = datos.dict(exclude_unset=True, exclude={"items"})
    for key, value in datos_dict.items():
        setattr(cotizacion, key, value)

    if datos.items is not None:
        # Obtener ids de items que vienen en la actualización
        ids_actualizados = [item.id for item in datos.items if item.id is not None]

        # Eliminar items que ya no están en la actualización
        for item_bd in cotizacion.items:
            if item_bd.id not in ids_actualizados:
                db.delete(item_bd)

        # Actualizar o crear items
        for item_data in datos.items:
            if item_data.id:
                # Actualizar item existente
                item_existente = db.query(CotizacionItem).filter(CotizacionItem.id == item_data.id).first()
                if item_existente:
                    item_existente.servicio = item_data.servicio
                    item_existente.cantidad = item_data.cantidad
                    item_existente.unidad = item_data.unidad
                    item_existente.precio_unitario = item_data.precio_unitario
                    item_existente.subtotal = item_data.subtotal
            else:
                # Crear nuevo item
                nuevo_item = CotizacionItem(
                    servicio=item_data.servicio,
                    cantidad=item_data.cantidad,
                    unidad=item_data.unidad,
                    precio_unitario=item_data.precio_unitario,
                    subtotal=item_data.subtotal,
                    cotizacion_id=cotizacion.id,
                )
                db.add(nuevo_item)

    db.commit()
    db.refresh(cotizacion)
    return cotizacion