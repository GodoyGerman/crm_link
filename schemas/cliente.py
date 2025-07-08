from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict

class ClienteBase(BaseModel):
    nombre: str
    tipo_identificacion: Optional[str]
    numero_identificacion: str
    correo: Optional[EmailStr]
    telefono: Optional[str]
    direccion: Optional[str]
    ciudad: Optional[str]
    nombre_empresa: Optional[str]
    segmento: Optional[str]
    redes_sociales: Optional[Dict[str, str]]
    medio_adquisicion: Optional[str]
    activo: Optional[bool] = True

class ClienteOut(ClienteBase):
    id: int

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nombre: Optional[str]
    tipo_identificacion: Optional[str]
    numero_identificacion: Optional[str]
    correo: Optional[EmailStr]
    telefono: Optional[str]
    direccion: Optional[str]
    ciudad: Optional[str]
    nombre_empresa: Optional[str]
    segmento: Optional[str]
    redes_sociales: Optional[Dict[str, str]]
    medio_adquisicion: Optional[str]
    activo: Optional[bool]

class ClienteResponse(ClienteBase):
    id: int
    nombre: str
    correo: EmailStr
    activo: bool

    class Config:
        from_attributes = True
