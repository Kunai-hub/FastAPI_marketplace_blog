from datetime import datetime

from pydantic import BaseModel, EmailStr

from src.fastapi_marketplace_blog.schemas.base import TunedModel


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(TunedModel):
    id: int
    email: EmailStr
    created_at: datetime
