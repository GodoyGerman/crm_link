from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON
from datetime import datetime
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    tipo_identificacion = Column(String(50))
    numero_identificacion = Column(String(100), unique=True)
    correo = Column(String(255))
    telefono = Column(String(50))
    direccion = Column(Text)
    ciudad = Column(String(100))
    nombre_empresa = Column(String(255))
    segmento = Column(String(100))
    redes_sociales = Column(JSON)  # usa JSON para integrarlo bien con PostgreSQL
    medio_adquisicion = Column(String(100))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
