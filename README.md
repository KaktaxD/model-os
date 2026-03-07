# model-os
pet-проект на backend с Python, использовал FastAPI для REST API, SQLAlchemy (async) для работы с PostgreSQL, pytest для тестов, Alembic для миграций баз данных и JWT для авторизации.

## Что делает проект

- API для создания, чтения, обновления и удаления задач.
- Авторизация пользователей через JWT.
- Поддержка поиска и фильтрации задач.
- Полностью покрыт тестами (pytest + асинхронные фикстуры).

Проект задумывался как pet‑проект для прокачки backend‑навыков: асинхронный стек, Clean Architecture, покрытие тестами и удобный деплой через Docker.

# Стек технологий

- Python 3.11
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Pytest + pytest‑asyncio
- Alembic для миграций
- JWT‑авторизация
