# --------------- Асинхронное подключение к PostgreSQL -------------------------
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine  # ✅ Добавили синхронный
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql+asyncpg://ecommerce:1234@localhost:5432/bazuka"

# ✅ АСИНХРОННЫЙ engine для FastAPI
async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

# ✅ СИНХРОННЫЙ engine для main.py и Alembic
sync_engine = create_engine(DATABASE_URL.replace("+asyncpg", ""))  # psycopg2 для синхронного

# ✅ Экспорт для совместимости
SessionLocal = async_session_maker
engine = sync_engine  # ← Это решает ошибку импорта!

class Base(DeclarativeBase):
    pass
