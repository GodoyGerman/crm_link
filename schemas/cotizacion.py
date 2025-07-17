from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# Item que llega para crear
class CotizacionItemCreate(BaseModel):
    servicio: str
    cantidad: int
    unidad: str
    precio_unitario: float
    descuento_porcentaje: float = Field(0.0, description="Descuento aplicado en porcentaje")
    subtotal: float

# Item que sale al consultar
class CotizacionItemOut(CotizacionItemCreate):
    id: int
    cotizacion_id: int

    class Config:
        from_attributes = True  # Pydantic V2

# Item para actualizar
class CotizacionItemUpdate(CotizacionItemCreate):
    id: Optional[int] = None

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

# Cotización para actualizar
class CotizacionUpdate(BaseModel):
    nombre_cliente: Optional[str]
    tipo_identificacion: Optional[str]
    identificacion: Optional[str]
    correo: Optional[str]
    direccion: Optional[str]
    telefono: Optional[str]
    ciudad: Optional[str]
    contacto: Optional[str]
    condiciones: Optional[str]
    fecha_emision: Optional[date]
    valida_hasta: Optional[date]
    estado: Optional[str]
    pdf_url: Optional[str]
    subtotal: Optional[float]
    iva: Optional[float]
    total: Optional[float]
    items: Optional[List[CotizacionItemUpdate]]

# Cotización para devolver
class CotizacionOut(CotizacionCreate):
    id: int
    items: List[CotizacionItemOut]

    class Config:
        from_attributes = True
