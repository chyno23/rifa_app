from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services import rifas_service
from pydantic import BaseModel

router = APIRouter()

class RifaCreate(BaseModel):
    nombre: str
    descripcion: str = ""
    cantidad_boletos: int

@router.post("/create")
def crear_rifa(rifa: RifaCreate, db: Session = Depends(get_db)):
    if rifa.cantidad_boletos <= 0:
        raise HTTPException(status_code=400, detail="La cantidad de boletos debe ser mayor a 0")
    nueva_rifa = rifas_service.crear_rifa(db, rifa.nombre, rifa.descripcion, rifa.cantidad_boletos)
    return {"message": f"Rifa '{nueva_rifa.nombre}' creada con ID {nueva_rifa.id}"}

@router.get("/rifas")
def obtener_rifas(db: Session = Depends(get_db)):
    return rifas_service.get_rifas(db)

@router.get("/id/{rifa_id}")
def obtener_rifa(rifa_id: int, db: Session = Depends(get_db)):
    rifa = rifas_service.get_rifa_by_id(db, rifa_id)
    if not rifa:
        raise HTTPException(status_code=404, detail="Rifa no encontrada")
    return rifa

@router.delete("/{rifa_id}")
def eliminar_rifa(rifa_id: int, db: Session = Depends(get_db)):
    if not rifas_service.delete_rifa(db, rifa_id):
        raise HTTPException(status_code=404, detail="Rifa no encontrada")
    return {"message": f"Rifa {rifa_id} eliminada correctamente."}

