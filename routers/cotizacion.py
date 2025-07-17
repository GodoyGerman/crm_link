from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.cotizacion import Cotizacion, CotizacionItem
from schemas.cotizacion import CotizacionCreate, CotizacionUpdate, CotizacionOut
from sqlalchemy.orm import joinedload
from utils.email import enviar_cotizacion_por_correo
from utils.security import get_current_user
from models.usuario import Usuario
import logging

logging.basicConfig(
    level=logging.INFO,  # Cambia a DEBUG para más detalles
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Cotizaciones"])

@router.post("/crear/", response_model=CotizacionOut)
def crear_cotizacion(cotizacion: CotizacionCreate, db: Session = Depends(get_db)):
    import logging
    logger = logging.getLogger(__name__)

    subtotal = cotizacion.subtotal
    iva = round(subtotal * 0.19, 2)
    total = round(subtotal + iva, 2)

    logger.info(f"Subtotal recibido: {subtotal}")
    logger.info(f"IVA calculado: {iva}")
    logger.info(f"Total calculado: {total}")

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
        subtotal=subtotal,
        iva=iva,
        total=total
    )

    for item in cotizacion.items:
        db_item = CotizacionItem(
        servicio=item.servicio,
        cantidad=item.cantidad,
        unidad=item.unidad,
        precio_unitario=item.precio_unitario,
        descuento_porcentaje=item.descuento_porcentaje,  # 👈 NUEVO
        subtotal=item.subtotal
    )
        db_cotizacion.items.append(db_item)

    logger.info(f"Valores antes de commit: subtotal={db_cotizacion.subtotal}, iva={db_cotizacion.iva}, total={db_cotizacion.total}")

    db.add(db_cotizacion)
    db.commit()
    db.refresh(db_cotizacion)

    logger.info(f"Guardado en BD: subtotal={db_cotizacion.subtotal}, iva={db_cotizacion.iva}, total={db_cotizacion.total}")

    return db_cotizacion


@router.get("/{cotizacion_id}", response_model=CotizacionOut)
def obtener_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user)  # protección JWT
):
    cotizacion = db.query(Cotizacion).options(joinedload(Cotizacion.items)).filter(Cotizacion.id == cotizacion_id).first()
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    return cotizacion

@router.get("/consulta/", response_model=List[CotizacionOut])
def listar_cotizaciones(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(get_current_user)  # protección con JWT
):
    cotizaciones = db.query(Cotizacion).options(joinedload(Cotizacion.items)).all()
    return cotizaciones

@router.post("/enviar-correo")
async def enviar_pdf_correo(
    correo: str = Form(...),
    pdf: UploadFile = File(...),
    usuario_actual: Usuario = Depends(get_current_user)  # protección JWT
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
                    item_existente.descuento_porcentaje = item_data.descuento_porcentaje  # 👈 NUEVO
                    item_existente.subtotal = item_data.subtotal
            else:
                # Crear nuevo item
                nuevo_item = CotizacionItem(
                    servicio=item_data.servicio,
                    cantidad=item_data.cantidad,
                    unidad=item_data.unidad,
                    precio_unitario=item_data.precio_unitario,
                    descuento_porcentaje=item_data.descuento_porcentaje,  # 👈 NUEVO
                    subtotal=item_data.subtotal,
                    cotizacion_id=cotizacion.id,
                )
                db.add(nuevo_item)

    db.commit()
    db.refresh(cotizacion)
    return cotizacion