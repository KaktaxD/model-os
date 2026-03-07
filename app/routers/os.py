from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from app.database import async_session_maker  # ← ПРЯМОЙ импорт!
from app.models.os import Os
from app.schemas import OsSchema, OsCreate
from typing import List

router = APIRouter(tags=["os"], prefix="/os")

@router.get("/", response_model=List[OsSchema])
async def get_os():
    async with async_session_maker() as db:
        result = await db.execute(select(Os).order_by(Os.id))
        return result.scalars().all()

@router.post("/", response_model=OsSchema, status_code=status.HTTP_201_CREATED)
async def create_os(os_data: OsCreate):
    async with async_session_maker() as db:
        db_os = Os(**os_data.model_dump())
        db.add(db_os)
        await db.commit()
        await db.refresh(db_os)
        return db_os

@router.delete("/{id}", response_model=OsSchema, status_code=status.HTTP_200_OK)
async def delete_os(id: int):
    async with async_session_maker() as db:
        result = await db.execute(select(Os).where(Os.id == id))
        os_obj = result.scalars().first()
        if os_obj is None:
            raise HTTPException(status_code=404, detail="OS не найдена")
        await db.delete(os_obj)
        await db.commit()
        return os_obj
