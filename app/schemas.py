from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, EmailStr

class OsCreate(BaseModel):
    """Модель для создания и обновления моделей POST PUT"""
    name: str = Field(..., min_length=3, max_length=50, description="Название модели")
    version: str = Field(..., description="Версия")
    release_year: int = Field(..., description="Дата выхода")

class OsSchema(BaseModel):
    """Для GET запросов"""
    id: int
    name: str = Field(..., min_length=3, max_length=50, description="Название модели")
    version: str = Field(..., description="Версия ОС")
    release_year: int

    model_config = ConfigDict(from_attributes=True)

class PhoneCreate(BaseModel):
    """Модель для создания и обновления мобил POST PUT"""
    firma: str = Field(..., min_length=3, max_length=20, description="фирма")
    model: str = Field(..., min_length=3, max_length=20, description="Модель")
    release_year: int = Field(..., ge=1900, le=2026, description="Год выхода")
    os_id: Optional[int] = Field(None, description="Внешний айдишник")

class Phoner(BaseModel):
    """GET"""
    id: int = Field(..., description="Собственный уникальный айдишник")
    firma: str = Field(..., min_length=3, max_length=20, description="фирма")
    model: str = Field(..., min_length=3, max_length=20, description="Модель")
    release_year: int = Field(...,ge=1900, le=2026, description="Год выхода")
    os_id: Optional[int] = Field(..., description="Внешний айдишник на os")

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr = Field(description="Email пользователя")
    password: str = Field(min_length=8, max_length=72,description="Пароль (минимум 8 символов)")
    role: str = Field(default="user", pattern="^(user|admin)$", description="Роль: 'user' или 'admin'")

class User(BaseModel):
    id: int
    email: EmailStr
    role: str
    model_config = ConfigDict(from_attributes=True)