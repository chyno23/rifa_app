
# app/services/sorteos_service.py
from sqlalchemy.orm import Session
from app.models import models
from random import choice

def run_sorteo(db: Session):
    vendidos = db.query(models.Boleto).filter_by(vendido=True).all()
    if not vendidos:
        return None
    ganador = choice(vendidos)
    sorteo = models.Sorteo(ganador_id=ganador.id)
    db.add(sorteo)
    db.commit()
    return ganador

def get_sorteos(db: Session):
    return db.query(models.Sorteo).all()

