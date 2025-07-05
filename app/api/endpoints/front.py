from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from app.services import boletos_service
from app.api.deps import get_db

@app.get("/boletos", response_class=HTMLResponse)
def mostrar_boletos(request: Request, db: Session = Depends(get_db)):
    boletos = boletos_service.get_available_boletos(db)
    return templates.TemplateResponse("templates/boletos.html", {"request": request, "boletos": boletos})
