# app/api/endpoints/sorteos.py
import pandas as pd

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services import sorteos_service
from app.models import models
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

# @router.get("/sorteo/historial", response_class=HTMLResponse)
# def historial_sorteos(request: Request, db: Session = Depends(get_db)):
#     sorteos = sorteos_service.get_sorteos_con_boletos(db)
#     return templates.TemplateResponse("sorteo_historial.html", {"request": request, "sorteos": sorteos})

@router.get("/sorteo/historial", response_class=HTMLResponse)
def historial_sorteos(request: Request, db: Session = Depends(get_db)):
    sorteos = sorteos_service.get_sorteos_con_boletos(db)
    return templates.TemplateResponse("sorteo_historial.html", {"request": request, "sorteo": sorteo})


@router.post("/sorteo/run", response_class=HTMLResponse)
def ejecutar_sorteo_web(request: Request, db: Session = Depends(get_db)):
    ganador = sorteos_service.run_sorteo(db)
    if not ganador:
        return templates.TemplateResponse("sin_sorteo.html", {"request": request})
    return templates.TemplateResponse("ganador.html", {"request": request, "ganador": ganador})

@router.get("/sorteo", response_class=HTMLResponse)
def ver_sorteo(request: Request):
    return templates.TemplateResponse("sorteo.html", {"request": request})
