
# app/main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Form

from app.api.endpoints import boletos, sorteos, rifas
from app.db2 import engine, SessionLocal
from app.models import models
from app.services import boletos_service
from app.services import sorteos_service

# Crear base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Rifas")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar Jinja2
templates = Jinja2Templates(directory="app/templates")

# Incluir rutas
app.include_router(sorteos.router, prefix="/sorteos", tags=["Sorteos"])
app.include_router(boletos.router, prefix="/boletos",tags=["Boletos"])
app.include_router(rifas.router, prefix="/rifas", tags=["Rifas"])


# Crear boletos si no existen
db = SessionLocal()
if db.query(models.Boleto).count() == 0:
    boletos_service.crear_boletos(db, 100)
db.close()

# # Página de inicio con plantilla
# @app.get("/boletos", response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

@app.get("/boletos/view", response_class=HTMLResponse)
def ver_boletos(request: Request):
    db = SessionLocal()
    boletos = boletos_service.get_available_boletos(db)
    db.close()
    return templates.TemplateResponse("boletos.html", {"request": request, "boletos": boletos})

# Vista para ver detalle y comprar boleto
@app.get("/comprar/{numero}", response_class=HTMLResponse)
def ver_boleto(numero: int, request: Request):
    db = SessionLocal()
    boleto = db.query(models.Boleto).filter_by(numero=numero).first()
    db.close()
    if not boleto:
        return templates.TemplateResponse("error.html", {"request": request, "message": "Boleto no encontrado"})
    return templates.TemplateResponse("comprar_boleto.html", {"request": request, "boleto": boleto})

# Vista POST para comprar boleto desde formulario HTML
@app.post("/boletos/view/{numero}", response_class=HTMLResponse)
def comprar_boleto_web(numero: int, request: Request, comprador: str = Form(...),telefono:str = Form(...), direccion:str = Form(...)):
    db = SessionLocal()
    boleto = boletos_service.buy_boleto(db, numero, comprador,telefono,direccion)
    db.close()
    if not boleto:
        return templates.TemplateResponse("comprar_boleto.html", {"request": request, "boleto": {"numero": numero, "vendido": True, "comprador": "Alguien"}})
    return templates.TemplateResponse("success.html", {"request": request, "numero": numero, "comprador": comprador})

@app.get("/boletos/vendidos", response_class=HTMLResponse)
def boletos_vendidos(request: Request):
    db = SessionLocal()
    boletos = db.query(models.Boleto).filter(models.Boleto.vendido == True).all()
    db.close()
    return templates.TemplateResponse("vendidos.html", {"request": request, "boletos": boletos})

@app.get("/sorteo/historial", response_class=HTMLResponse)
def historial_sorteos(request: Request):
    db = SessionLocal()
    sorteos = sorteos_service.get_sorteos_con_boletos(db)
    db.close()
    return templates.TemplateResponse("sorteo_historial.html", {
        "request": request,
        "sorteos": sorteos
    })

