from typing import Optional, Sequence, Union

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.fastapi_marketplace_blog.db.models import Category


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, name: str, slug: Optional[str] = None) -> Category:
        async with self.session.begin():
            if slug:
                query = select(Category).where(
                    or_(Category.slug == slug, Category.name == name)
                )
                existing = await self.session.execute(statement=query)
            else:
                query = select(Category).where(Category.name == name)
                existing = await self.session.execute(statement=query)

            if existing.scalar_one_or_none():
                raise ValueError("Category already exists")
            new_category = Category(
                name=name,
                slug=slug,
            )
            self.session.add(instance=new_category)
            await self.session.flush()

            return new_category

    async def get_categories(self) -> Union[Sequence[Category], None]:
        async with self.session.begin():
            query = select(Category).order_by(Category.created_at.desc())
            result = await self.session.execute(statement=query)
            categories = result.scalars().all()

            return categories
