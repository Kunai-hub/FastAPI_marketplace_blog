from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.fastapi_marketplace_blog.db.models import User
from src.fastapi_marketplace_blog.services.hasher import hash_password


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, email: str, password: str) -> User:
        async with self.session.begin():
            query = select(User).where(User.email == email)
            existing = await self.session.execute(statement=query)

            if existing.scalar_one_or_none():
                raise ValueError("Email already exists")
            new_user = User(
                email=email,
                hashed_password=hash_password(password),
            )
            self.session.add(instance=new_user)
            await self.session.flush()

            return new_user
