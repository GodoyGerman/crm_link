from sqlalchemy import Column, Integer, String, Text, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base
from database import Base

Base = declarative_base()

class Cotizacion(Base):
    __tablename__ = "cotizaciones"

    id = Column(Integer, primary_key=True, index=True)

    nombre_cliente = Column(String(100))
    tipo_identificacion = Column(String(50))
    identificacion = Column(String(50))
    correo = Column(String(100))
    direccion = Column(Text)
    telefono = Column(String(20))
    ciudad = Column(String(100))
    contacto = Column(String(100))

    servicio = Column(String(100))
    cantidad = Column(Integer)
    unidad = Column(String(50))
    precio_unitario = Column(Numeric(12, 2))

    subtotal = Column(Numeric(12, 2))
    iva = Column(Numeric(12, 2))
    total = Column(Numeric(12, 2))

    condiciones = Column(Text)

    fecha_emision = Column(Date)
    valida_hasta = Column(Date)
    estado = Column(String(20), default="pendiente")
    pdf_url = Column(Text, nullable=True)