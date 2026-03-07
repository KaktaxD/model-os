from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List

from app.db_depends import get_async_db
from app.schemas import Phoner, PhoneCreate
from app.models.model import Phone
from app.models.os import Os
from app.models.users import User as UserModel  # ← ДОБАВИЛИ
from app.auth import get_current_user  # ← ДОБАВИЛИ (или get_current_seller → get_current_user)

router = APIRouter(prefix="/model", tags=["model"])


# Проверяем что пользователь admin
def get_current_admin(current_user: UserModel = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администраторы могут управлять моделями"
        )
    return current_user


@router.get("/", response_model=List[Phoner])
async def get_models(db: AsyncSession = Depends(get_async_db)):
    """Список всех моделей ус-в (доступно всем авторизованным)"""
    stmt = select(Phone).order_by(Phone.id)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/", response_model=Phoner, status_code=status.HTTP_201_CREATED)
async def create_model(
        model: PhoneCreate,
        db: AsyncSession = Depends(get_async_db),
        current_admin: UserModel = Depends(get_current_admin)  # ← АВТОРИЗАЦИЯ
):
    """Создаёт новую мобилу (только admin)"""
    if model.os_id is not None:
        os_stmt = select(Os).where(Os.id == model.os_id)
        os_result = await db.execute(os_stmt)
        os_exists = os_result.scalar_one_or_none()
        if os_exists is None:
            raise HTTPException(status_code=404, detail="OS с таким ID не найден")

    db_model = Phone(**model.model_dump())
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)
    return db_model


@router.get("/{id}", response_model=Phoner, status_code=status.HTTP_200_OK)
async def get_model(id: int, db: AsyncSession = Depends(get_async_db)):
    """Получение мобилы по id (доступно всем авторизованным)"""
    stmt = select(Phone).where(Phone.id == id)
    result = await db.execute(stmt)
    phone = result.scalar_one_or_none()
    if phone is None:
        raise HTTPException(status_code=404, detail="Телефон не найден")
    return phone


@router.put("/{id}", response_model=Phoner, status_code=status.HTTP_200_OK)
async def change_model(
        id: int,
        model_update: PhoneCreate,
        db: AsyncSession = Depends(get_async_db),
        current_admin: UserModel = Depends(get_current_admin)  # ← АВТОРИЗАЦИЯ
):
    """Обновить телефон по id (только admin)"""
    stmt = select(Phone).where(Phone.id == id)
    result = await db.execute(stmt)
    phone = result.scalar_one_or_none()
    if phone is None:
        raise HTTPException(status_code=404, detail="Телефон не найден")

    if model_update.os_id is not None:
        os_stmt = select(Os).where(Os.id == model_update.os_id)
        os_result = await db.execute(os_stmt)
        os_exists = os_result.scalar_one_or_none()
        if os_exists is None:
            raise HTTPException(status_code=404, detail="OS не найден")

    await db.execute(
        update(Phone).where(Phone.id == id).values(**model_update.model_dump(exclude_unset=True))
    )
    await db.commit()
    await db.refresh(phone)
    return phone


@router.delete("/{id}", response_model=Phoner, status_code=status.HTTP_200_OK)
async def delete_model(
        id: int,
        db: AsyncSession = Depends(get_async_db),
        current_admin: UserModel = Depends(get_current_admin)  # ← АВТОРИЗАЦИЯ
):
    """Удаление телефона по id (только admin)"""
    stmt = select(Phone).where(Phone.id == id)
    result = await db.execute(stmt)
    phone = result.scalar_one_or_none()
    if phone is None:
        raise HTTPException(status_code=404, detail="Телефон не найден")

    await db.delete(phone)
    await db.commit()
    return phone
