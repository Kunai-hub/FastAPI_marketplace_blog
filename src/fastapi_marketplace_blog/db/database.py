from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.fastapi_marketplace_blog.core.config import config

DATABASE_URL = config.DATABASE_URL
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        yield session
