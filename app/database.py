# --------------- Асинхронное подключение к PostgreSQL -------------------------
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine  # ✅ Добавили синхронный
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://ecommerce:1234@localhost:5432/bazuka"


async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


sync_engine = create_engine(DATABASE_URL.replace("+asyncpg", "")) 


SessionLocal = async_session_maker
engine = sync_engine 

class Base(DeclarativeBase):
    pass
