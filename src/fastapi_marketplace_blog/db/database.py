from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.fastapi_marketplace_blog.core.config import config

DATABASE_URL = config.DATABASE_URL
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession]:
    session: AsyncSession = async_session()
    try:
        yield session
    finally:
        await session.close()
