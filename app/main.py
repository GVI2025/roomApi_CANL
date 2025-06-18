from fastapi import FastAPI

from app.routers import reservation, salle

app = FastAPI(
    title="roomAPI",
    description="A WebAPI REST to reserve rooms built with FastAPI, SQLAlchemy, and SQLite",
    version="0.1.0",
)

app.include_router(salle.router)
app.include_router(reservation.router)

@app.get("/")
async def root():
    return {"message": "Welcome to roomAPI!"}