from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.fastapi_marketplace_blog.db.models import User
from src.fastapi_marketplace_blog.services.hasher import verify_password


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email_for_auth(self, email: str) -> Union[User, None]:
        async with self.session.begin():
            query = select(User).where(User.email == email)
            result = await self.session.execute(statement=query)
            user_row = result.scalars().first()

            return user_row

    async def authenticate_user(self, email: str, password: str) -> Union[User, None]:
        user = await self.get_user_by_email_for_auth(email=email)

        if not user:
            return

        if not verify_password(
            plain_password=password, hashed_password=user.hashed_password
        ):
            return

        return user
