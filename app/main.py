from fastapi import FastAPI
from app.routers import reservation, salle
import uvicorn

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

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True, log_level="debug")