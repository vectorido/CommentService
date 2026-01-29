from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.database.connection import db_connection
from src.presentation.api.routes.users import router as users_router
from src.presentation.api.routes.comments import router as comments_router


# Контекст жизненного цикла приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_connection.connect()
    yield
    await db_connection.disconnect()


# Создание FastAPI приложения
def create_app() -> FastAPI:
    app = FastAPI(
        title="Clean Architecture Template",
        description="FastAPI project template with Clean Architecture principles",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключение маршрутов пользователей
    app.include_router(users_router)

    # Подключение маршрутов комментариев
    app.include_router(comments_router)

    # Health check
    @app.get("/health")
    async def health_check():
        return {"status": "ok"}

    return app


# Создание глобального экземпляра приложения
app = create_app()
