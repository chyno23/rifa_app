# app/api/endpoints/boletos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db2 import SessionLocal
from app.services import boletos_service
from app.api.deps import get_db

router = APIRouter()

def get_db2():
    db2 = SessionLocal()
    try:
        yield db2
    finally:
        db2.close()

@router.get("/boletos/available")
def boletos_disponibles(db2: Session = Depends(get_db)):
    return boletos_service.get_available_boletos(db2)

@router.post("/boletos/buy")
def comprar_boleto(numero: int, comprador: str, db2: Session = Depends(get_db)):
    boleto = boletos_service.buy_boleto(db2, numero, comprador)
    if not boleto:
        raise HTTPException(status_code=404, detail="Boleto no disponible")
    return {"message": f"Boleto {numero} vendido a {comprador}"}
