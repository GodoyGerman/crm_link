from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(String, primary_key=True, index=True)
    nombre_servicio = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("Categoria")
    precio_unitario = Column(Float, nullable=False)
    unidad_medida = Column(String, nullable=True)
    duracion_estimada = Column(String, nullable=True)
    descuento_porcentaje = Column(Float, default=0.0)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # Opcional: si tienes relación con categoría
    # categoria = relationship("Categoria", back_populates="servicios")
