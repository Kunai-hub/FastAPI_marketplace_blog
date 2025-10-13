from sqlalchemy.ext.asyncio import AsyncSession

from src.fastapi_marketplace_blog.schemas.schemas import UserCreate
from src.fastapi_marketplace_blog.db.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserCreate):
        async with self.session.begin():
            new_user = User(
                email=user.email,
                hashed_password=user.password,
                # TODO add hashing for password
            )
            self.session.add(new_user)
            await self.session.flush()

        return new_user
