# schemas/usuario.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    rol: Optional[str] = "usuario"
    activo: Optional[bool] = True

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioOut(UsuarioBase):
    id: int
    creado_en: datetime

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    correo: EmailStr
    contraseña: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UsuarioCreate(BaseModel):
    nombre: str
    correo: EmailStr
    contraseña: str
    rol: str = "usuario"
    activo: bool = True

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    rol: str
    activo: bool

class UsuarioUpdate(BaseModel):
    nombre: Optional[str]
    correo: Optional[EmailStr]
    rol: Optional[str]
    activo: Optional[bool]
