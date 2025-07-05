
# app/services/sorteos_service.py
from sqlalchemy.orm import Session
from app.models import models
from random import choice

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services import sorteos_service
from fastapi.templating import Jinja2Templates

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

def get_sorteos_con_boletos(db: Session):
    sorteos = db.query(models.Sorteo).order_by(models.Sorteo.fecha.desc()).all()
    resultado = []
    for s in sorteos:
        boleto = db.query(models.Boleto).filter_by(id=s.ganador_id).first()
        resultado.append({"boleto": boleto, "fecha": s.fecha})
    return resultado

