from sqlalchemy.ext.asyncio import AsyncSession

from src.fastapi_marketplace_blog.schemas.schemas import UserCreate, UserResponse
from src.fastapi_marketplace_blog.db.models import User
from src.fastapi_marketplace_blog.services.hasher import hash_password


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserCreate) -> UserResponse:
        async with self.session.begin():
            new_user = User(
                email=user.email,
                hashed_password=hash_password(user.password),
            )
            self.session.add(new_user)
            await self.session.flush()

            return UserResponse(
                id=new_user.id,
                email=new_user.email,
                created_at=new_user.created_at,
            )
