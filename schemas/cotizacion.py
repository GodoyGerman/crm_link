from pydantic import BaseModel
from typing import List, Optional
from datetime import date

# Item que llega para crear
class CotizacionItemCreate(BaseModel):
    servicio: str
    cantidad: int
    unidad: str
    precio_unitario: float
    subtotal: float

# Item que sale al consultar
class CotizacionItemOut(CotizacionItemCreate):
    id: int
    cotizacion_id: int

    class Config:
        from_attributes = True  # reemplaza orm_mode en Pydantic V2

# Cotización para crear
class CotizacionCreate(BaseModel):
    nombre_cliente: str
    tipo_identificacion: str
    identificacion: str
    correo: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    contacto: Optional[str] = None
    condiciones: Optional[str] = None
    fecha_emision: date
    valida_hasta: date
    estado: str
    pdf_url: Optional[str] = None
    subtotal: float
    iva: float
    total: float
    items: List[CotizacionItemCreate]

# Cotización para devolver (incluye items con IDs)
class CotizacionOut(CotizacionCreate):
    id: int
    items: List[CotizacionItemOut]
    

    class Config:
        from_attributes = True

