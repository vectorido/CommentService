import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from src.infrastructure.database.connection import db_connection
from src.presentation.api.routes.users import router as users_router


@pytest_asyncio.fixture(scope="function")
async def client():
    if db_connection.pool:
        db_connection.pool = None
    
    await db_connection.connect()
    
    app = FastAPI(title="Test App")
    app.include_router(users_router)
    
    pool = db_connection.pool
    async with pool.acquire() as conn:
        await conn.execute("truncate table users cascade;")
    
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac
    
    async with pool.acquire() as conn:
        await conn.execute("truncate table users cascade;")

