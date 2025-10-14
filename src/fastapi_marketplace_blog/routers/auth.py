from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.exc import IntegrityError

from src.fastapi_marketplace_blog.schemas.schemas import UserResponse, UserCreate
from src.fastapi_marketplace_blog.db.database import get_db
from src.fastapi_marketplace_blog.repositories.users import UserRepository
from src.fastapi_marketplace_blog.repositories.auth import AuthRepository
from src.fastapi_marketplace_blog.services.access_token_creater import (
    create_access_token,
)
from src.fastapi_marketplace_blog.core.config import config

ACCESS_COOKIE = "access_token"
REFRESH_COOKIE = "refresh_token"

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=UserResponse)
async def register(body: UserCreate, db=Depends(get_db)) -> UserResponse:
    try:
        repo = UserRepository(session=db)
        user = await repo.create_user(email=body.email, password=body.password)

        return UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at,
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error: {e}",
        )


@auth_router.post("/login")
async def login(response: Response, form_data: UserCreate, db=Depends(get_db)):
    repo = AuthRepository(session=db)
    user = await repo.authenticate_user(
        email=form_data.email, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(data={"sub": user.email}, method="access")
    refresh_token = create_access_token(data={"sub": user.email}, method="refresh")

    response.set_cookie(
        key=ACCESS_COOKIE,
        value=access_token,
        httponly=True,
        samesite="lax",
        path="/",
        max_age=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key=REFRESH_COOKIE,
        value=refresh_token,
        httponly=True,
        samesite="lax",
        path="/",
        max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
    )

    return {"message": "authenticated"}


@auth_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key=ACCESS_COOKIE, path="/")
    response.delete_cookie(key=REFRESH_COOKIE, path="/")

    return {"message": "successfully logged out"}
