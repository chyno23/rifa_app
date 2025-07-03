# app/api/endpoints/sorteos.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db2 import SessionLocal
from app.services import sorteos_service

router = APIRouter()

def get_db():
    db2 = SessionLocal()
    try:
        yield db2
    finally:
        db2.close()

@router.post("/sorteo/run")
def ejecutar_sorteo(db2: Session = Depends(get_db)):
    ganador = sorteos_service.run_sorteo(db2)
    if not ganador:
        return {"message": "No hay boletos vendidos"}
    return {"ganador": ganador.numero, "comprador": ganador.comprador}

@router.get("/sorteo/history")
def historial_sorteos(db2: Session = Depends(get_db)):
    sorteos = sorteos_service.get_sorteos(db2)
    return sorteos
