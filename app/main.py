from fastapi import FastAPI
from app.routers.model import router as r1
from app.database import Base, engine
from app.routers.os import router as r2
from app.routers import users

# Создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Интернет-магазин")

app.include_router(r1)
app.include_router(r2)
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}