# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# app/models/models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Boleto(Base):
    __tablename__ = "boletos"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, index=True)
    vendido = Column(Boolean, default=False)
    comprador = Column(String, nullable=True)

class Sorteo(Base):
    __tablename__ = "sorteos"
    id = Column(Integer, primary_key=True, index=True)
    ganador_id = Column(Integer, ForeignKey("boletos.id"))
    fecha = Column(DateTime, default=datetime.utcnow)