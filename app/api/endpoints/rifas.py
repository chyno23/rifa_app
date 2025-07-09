from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services import rifas_service

router = APIRouter()

@router.post("/rifas/create")
def crear_rifa(nombre: str, descripcion: str = "", cantidad_boletos: int = 0, db: Session = Depends(get_db)):
    if cantidad_boletos <= 0:
        raise HTTPException(status_code=400, detail="La cantidad de boletos debe ser mayor a 0")
    rifa = rifas_service.crear_rifa(db, nombre, descripcion, cantidad_boletos)
    return {"message": f"Rifa '{rifa.nombre}' creada con ID {rifa.id}"}

@router.get("/rifas")
def obtener_rifas(db: Session = Depends(get_db)):
    return rifas_service.get_rifas(db)

@router.get("/rifas/{rifa_id}")
def obtener_rifa(rifa_id: int, db: Session = Depends(get_db)):
    rifa = rifas_service.get_rifa_by_id(db, rifa_id)
    if not rifa:
        raise HTTPException(status_code=404, detail="Rifa no encontrada")
    return rifa

@router.delete("/rifas/{rifa_id}")
def eliminar_rifa(rifa_id: int, db: Session = Depends(get_db)):
    if not rifas_service.delete_rifa(db, rifa_id):
        raise HTTPException(status_code=404, detail="Rifa no encontrada")
    return {"message": f"Rifa {rifa_id} eliminada correctamente."}

