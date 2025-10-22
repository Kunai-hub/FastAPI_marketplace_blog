import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text

from src.asgi import app
from src.fastapi_marketplace_blog.db import database
from src.fastapi_marketplace_blog.db.models import Base


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture(scope="function")
async def client(monkeypatch):
    test_engine = create_async_engine(
        database.DATABASE_URL,
        echo=False,
        poolclass=NullPool,
        future=True,
    )

    TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)

    monkeypatch.setattr(database, "async_engine", test_engine)
    monkeypatch.setattr(database, "async_session", TestSessionLocal)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(
                text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE')
            )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac

    async with test_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(
                text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE')
            )

    await test_engine.dispose()
