# app/api/deps.py
from app.db2 import SessionLocal

def get_db():
    db2 = SessionLocal()
    try:
        yield db2
    finally:
        db2.close()
