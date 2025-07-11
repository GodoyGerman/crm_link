from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Cotizacion(Base):
    __tablename__ = "cotizaciones"

    id = Column(Integer, primary_key=True, index=True)
    nombre_cliente = Column(String, nullable=False)
    tipo_identificacion = Column(String, nullable=False)
    identificacion = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    direccion = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    ciudad = Column(String, nullable=True)
    contacto = Column(String, nullable=True)
    condiciones = Column(String, nullable=True)
    fecha_emision = Column(Date, nullable=False)
    valida_hasta = Column(Date, nullable=False)
    estado = Column(String, nullable=False)
    pdf_url = Column(String, nullable=True)
    subtotal = Column(Float, nullable=False)
    iva = Column(Float, nullable=False)
    total = Column(Float, nullable=False)

    items = relationship("CotizacionItem", back_populates="cotizacion", cascade="all, delete-orphan")


class CotizacionItem(Base):
    __tablename__ = "cotizacion_items"

    id = Column(Integer, primary_key=True, index=True)
    cotizacion_id = Column(Integer, ForeignKey("cotizaciones.id"), nullable=False)
    servicio = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    unidad = Column(String, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    cotizacion = relationship("Cotizacion", back_populates="items")
