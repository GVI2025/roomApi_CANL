from app.routers import reservation, salle
import uvicorn
import logging
import logging.config
from fastapi import FastAPI, Request
from time import time
from app.logging_config import LOGGING_CONFIG

from prometheus_fastapi_instrumentator import Instrumentator


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="roomAPI",
    description="A WebAPI REST to reserve rooms built with FastAPI, SQLAlchemy, and SQLite",
    version="0.1.0",
)

instrumentator = Instrumentator().instrument(app).expose(app)

app.include_router(salle.router)
app.include_router(reservation.router)


@app.get("/")
async def root():
    return {"message": "Welcome to roomAPI!"}

# Middleware pour journaliser les requêtes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time()
    logger.info(f"Requête entrante: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Erreur lors de la requête: {str(e)}")
        raise e

    duration = time() - start_time
    logger.info(f"Durée de traitement: {duration:.4f}s")
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="debug")