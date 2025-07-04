from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime

class ServicioBase(BaseModel):
    
    nombre_servicio: str
    descripcion: Optional[str]
    categoria_id: int
    precio_unitario: Decimal
    unidad_medida: Optional[str]
    duracion_estimada: Optional[str]
    descuento_porcentaje: Optional[Decimal] = 0.00
    estado: Optional[bool] = True

class ServicioCreate(ServicioBase):
    pass

class ServicioUpdate(BaseModel):
    nombre_servicio: Optional[str]
    descripcion: Optional[str]
    categoria_id: Optional[int]
    precio_unitario: Optional[Decimal]
    unidad_medida: Optional[str]
    duracion_estimada: Optional[str]
    descuento_porcentaje: Optional[Decimal]
    estado: Optional[bool]

class ServicioResponse(ServicioBase):
    fecha_creacion: Optional[datetime]

    class Config:
        orm_mode = True