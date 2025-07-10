from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
from schemas.categoria import CategoriaBase

# Solo los campos que el usuario envía al crear
class ServicioBase(BaseModel):
    nombre_servicio: str
    descripcion: Optional[str]
    categoria_id: int
    precio_unitario: Decimal
    unidad_medida: Optional[str]
    duracion_estimada: Optional[str]
    descuento_porcentaje: Optional[Decimal] = 0.00
    estado: Optional[bool] = True

# Usado para POST /servicios/
class ServicioCreate(ServicioBase):
    pass

# Usado para PUT /servicios/{id}
class ServicioUpdate(BaseModel):
    nombre_servicio: Optional[str]
    descripcion: Optional[str]
    categoria_id: Optional[int]
    precio_unitario: Optional[Decimal]
    unidad_medida: Optional[str]
    duracion_estimada: Optional[str]
    descuento_porcentaje: Optional[Decimal]
    estado: Optional[bool]

# Usado para GET (respuesta completa)
class ServicioResponse(ServicioBase):
    id: int
    categoria: Optional[CategoriaBase]  # Se incluye solo en la respuesta
    fecha_creacion: Optional[datetime]

    class Config:
        orm_mode = True