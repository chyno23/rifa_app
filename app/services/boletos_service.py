# app/services/boletos_service.py
from sqlalchemy.orm import Session
from app.models import models
from app.core import rabbitmq
import asyncio

def get_available_boletos(db: Session):
    return db.query(models.Boleto).filter_by(vendido=False).all()

def buy_boleto(db: Session, numero: int, comprador: str):
    boleto = db.query(models.Boleto).filter_by(numero=numero, vendido=False).first()
    if not boleto:
        return None
    boleto.vendido = True
    boleto.comprador = comprador
    db.commit()
    asyncio.run(rabbitmq.publish_sale_message(f"Boleto {numero} vendido a {comprador}"))
    return boleto
