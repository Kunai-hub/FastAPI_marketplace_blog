from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from src.fastapi_marketplace_blog.schemas.schemas import UserResponse, UserCreate
from src.fastapi_marketplace_blog.db.database import get_db
from src.fastapi_marketplace_blog.repositories.users import UserRepository

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=UserResponse)
async def register(body: UserCreate, db=Depends(get_db)) -> UserResponse:
    try:
        repo = UserRepository(db)
        user = await repo.create_user(body)

        return user
    except IntegrityError as e:
        raise HTTPException(status_code=503, detail=f"Database error: {e}")
