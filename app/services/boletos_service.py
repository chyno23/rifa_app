# app/services/boletos_service.py
from sqlalchemy.orm import Session
from app.models import models
from app.core import rabbitmq
import asyncio

def get_available_boletos(db: Session):
    return db.query(models.Boleto).filter_by(vendido=False).all()

def buy_boleto(db: Session, numero: int, comprador: str, telefono:str, direccion:str):
    boleto = db.query(models.Boleto).filter_by(numero=numero, vendido=False).first()
    if not boleto:
        return None
    boleto.vendido = True
    boleto.comprador = comprador
    boleto.telefono = telefono
    boleto.direccion = direccion

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

def borrar_boleto(db, rifa_id, numero):
    boleto = db.query(models.Boleto).filter_by(rifa_id=rifa_id, numero=numero).first()
    if not boleto:
        return False

    db.delete(boleto)
    db.commit()
    return True

def agregar_boletos_a_rifa(db, rifa_id, cantidad_extra):
    rifa = db.query(models.Rifa).filter_by(id=rifa_id).first()
    if not rifa:
        return None
    
    ultimo_numero = db.query(models.Boleto).filter_by(rifa_id=rifa_id).order_by(models.Boleto.numero.desc()).first()
    start = ultimo_numero.numero + 1 if ultimo_numero else 1

    for i in range(start, start + cantidad_extra):
        boleto = models.Boleto(numero=i, rifa_id=rifa_id)
        db.add(boleto)

    db.commit()
    return True