
# app/main.py
from fastapi import FastAPI
from app.api.endpoints import boletos, sorteos
from app.db2 import engine
from app.models import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Rifas")

app.include_router(boletos.router)
app.include_router(sorteos.router)
