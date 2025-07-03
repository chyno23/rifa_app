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

def crear_boletos(db: Session, cantidad: int):
    existing_numbers = set([b.numero for b in db.query(models.Boleto).all()])
    boletos = []
    for i in range(1, cantidad + 1):
        if i not in existing_numbers:
            boleto = models.Boleto(numero=i)
            boletos.append(boleto)
    db.add_all(boletos)
    db.commit()
    return {"created": len(boletos), "skipped": cantidad - len(boletos)}

