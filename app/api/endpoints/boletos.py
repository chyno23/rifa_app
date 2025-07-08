# # app/api/endpoints/boletos.py
# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.db2 import SessionLocal
# from app.services import boletos_service
# from app.api.deps import get_db

# router = APIRouter()

# def get_db2():
#     db2 = SessionLocal()
#     try:
#         yield db2
#     finally:
#         db2.close()

# @router.post("/boletos/create")
# def crear_boletos_endpoint(cantidad: int, db: Session = Depends(get_db)):
#     boletos_service.crear_boletos(db, cantidad)
#     return {"message": f"Se crearon {cantidad} boletos."}

# @router.get("/boletos/available")
# def boletos_disponibles(db2: Session = Depends(get_db)):
#     return boletos_service.get_available_boletos(db2)

# @router.post("/boletos/buy")
# def comprar_boleto(numero: int, comprador: str, db2: Session = Depends(get_db)):
#     boleto = boletos_service.buy_boleto(db2, numero, comprador)
#     if not boleto:
#         raise HTTPException(status_code=404, detail="Boleto no disponible")
#     return {"message": f"Boleto {numero} vendido a {comprador}"}
import pandas as pd

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services import boletos_service
from app.models import models
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

@router.get("/available")
def boletos_disponibles(db: Session = Depends(get_db)):
    return boletos_service.get_available_boletos(db)

@router.post("/buy")
def comprar_boleto(numero: int, comprador: str,telefono:str,direccion:str ,db: Session = Depends(get_db)):
    boleto = boletos_service.buy_boleto(db, numero, comprador,telefono,direccion)
    if not boleto:
        raise HTTPException(status_code=404, detail="Boleto no disponible")
    return {"message": f"Boleto {numero} vendido a {comprador}"}

@router.post("/create")
def crear_boletos(cantidad: int, db: Session = Depends(get_db)):
    boletos_service.crear_boletos(db, cantidad)
    return {"message": f"Se crearon {cantidad} boletos."}



@router.post("/upload_excel")
def upload_boletos(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="El archivo debe ser .xlsx")

    # Leer Excel
    df = pd.read_excel(file.file)

    # Validar columnas requeridas
    required_columns = {'numero', 'comprador'}
    if not required_columns.issubset(df.columns):
        raise HTTPException(status_code=400, detail=f"El Excel debe tener las columnas: {required_columns}")

    # Crear boletos en base de datos
    for _, row in df.iterrows():
        boleto = models.Boleto(
            numero=row['numero'],
            comprador=row.get('comprador'),
            vendido=bool(row.get('comprador'))
        )
        db.add(boleto)
    db.commit()

    return {"message": "Boletos cargados correctamente"}

@router.get("/upload_excel", response_class=HTMLResponse)
def formulario_upload_excel(request: Request):
    return templates.TemplateResponse("upload_excel.html", {"request": request})