from fastapi import APIRouter, Depends

from src.fastapi_marketplace_blog.schemas.schemas import UserResponse, UserCreate
from src.fastapi_marketplace_blog.db.database import get_db
from src.fastapi_marketplace_blog.repositories.users import UserRepository

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=UserResponse)
async def register(body: UserCreate, db=Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.create_user(body)

    return user
