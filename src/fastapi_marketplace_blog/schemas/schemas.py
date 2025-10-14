from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from src.fastapi_marketplace_blog.schemas.base import TunedModel


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(TunedModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime


class CategoryCreate(BaseModel):
    name: str
    slug: Optional[str] = None


class CategoryResponse(TunedModel):
    id: int
    name: str
    slug: str
    created_at: datetime
