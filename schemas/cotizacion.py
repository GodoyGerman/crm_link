# schemas/cotizacion.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from decimal import Decimal

class CotizacionBase(BaseModel):
    nombre_cliente: str
    tipo_identificacion: str
    identificacion: str
    correo: EmailStr
    direccion: str
    telefono: str
    ciudad: str
    contacto: str
    servicio: str
    cantidad: int
    unidad: str
    precio_unitario: Decimal
    subtotal: Decimal
    iva: Decimal
    total: Decimal
    condiciones: str
    fecha_emision: Optional[date]
    valida_hasta: Optional[date]
    estado: Optional[str] = "pendiente"
    pdf_url: Optional[str] = None

class CotizacionCreate(CotizacionBase):
    pass

class CotizacionUpdate(CotizacionBase):
    pass

class CotizacionOut(CotizacionBase):
    id: int

    class Config:
        orm_mode = True
