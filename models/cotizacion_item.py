from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class CotizacionItem(Base):
    __tablename__ = "cotizacion_items"
    id = Column(Integer, primary_key=True, index=True)
    cotizacion_id = Column(Integer, ForeignKey("cotizaciones.id"))
    servicio = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    unidad = Column(String, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    cotizacion = relationship("Cotizacion", back_populates="items")
