
# app/main.py
from fastapi import FastAPI
from app.api.endpoints import boletos, sorteos
from app.db2 import engine
from app.models import models
from app.services import boletos_service
from app.db2 import SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Rifas")

# app.include_router(boletos.router)
# app.include_router(sorteos.router)
app.include_router(boletos.router, prefix="/boletos", tags=["Boletos"])
app.include_router(sorteos.router, prefix="/sorteos", tags=["Sorteos"])


# Crear boletos si no existen
db = SessionLocal()
if db.query(models.Boleto).count() == 0:
    boletos_service.crear_boletos(db, 100)  # crea 100 boletos
db.close()

# Crear boletos si no existen
db = SessionLocal()
if db.query(models.Boleto).count() == 0:
    boletos_service.crear_boletos(db, 100)  # crea 100 boletos
db.close()
