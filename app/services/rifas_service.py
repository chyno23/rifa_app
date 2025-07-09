from app.models import models
from app.db2 import SessionLocal

def crear_rifa(db, nombre, descripcion, cantidad_boletos):
    nueva_rifa = models.Rifa(
        nombre=nombre,
        descripcion=descripcion,
        cantidad_boletos=cantidad_boletos
    )
    db.add(nueva_rifa)
    db.commit()
    db.refresh(nueva_rifa)
    return nueva_rifa

def get_rifas(db):
    return db.query(models.Rifa).all()

def get_rifa_by_id(db, rifa_id):
    return db.query(models.Rifa).filter_by(id=rifa_id).first()

def delete_rifa(db, rifa_id):
    rifa = get_rifa_by_id(db, rifa_id)
    if not rifa:
        return False
    db.delete(rifa)
    db.commit()
    return True

