# app/models/models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class Rifa(Base):
    __tablename__ = 'rifas'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    cantidad_boletos = Column(Integer, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # relación con boletos, opcional si quieres obtenerlos en bloque
    boletos = relationship("Boleto", back_populates="rifa", cascade="all, delete-orphan")

class Boleto(Base):
    __tablename__ = "boletos"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, index=True)
    vendido = Column(Boolean, default=False)
    comprador = Column(String, nullable=True)
    telefono = Column(String, nullable=True)  
    direccion = Column(String, nullable=True)
    rifa_id = Column(Integer, ForeignKey('rifas.id'))
    rifa = relationship("Rifa", back_populates="boletos")


class Sorteo(Base):
    __tablename__ = "sorteos"
    id = Column(Integer, primary_key=True, index=True)
    ganador_id = Column(Integer, ForeignKey("boletos.id"))
    fecha = Column(DateTime, default=datetime.utcnow)
