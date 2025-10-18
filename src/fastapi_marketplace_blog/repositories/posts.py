from typing import Optional, Union, Sequence

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.fastapi_marketplace_blog.db.models import Post


class PostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_post(
        self, title: str, text: str, category_id: int, image: Optional[str] = None
    ) -> Post:
        async with self.session.begin():
            new_post = Post(
                title=title,
                text=text,
                category_id=category_id,
                image=image,
            )
            self.session.add(instance=new_post)
            await self.session.flush()
            query = (
                select(Post)
                .options(selectinload(Post.category))
                .where(Post.id == new_post.id)
            )
            result = await self.session.execute(statement=query)

            return result.scalar_one()

    async def get_posts(
        self, search: str, category_id: int, page_number: int, page_size: int
    ) -> Union[Sequence[Post], None]:
        async with self.session.begin():
            query = select(Post).options(selectinload(Post.category))

            if category_id:
                query = query.where(Post.category_id == category_id)

            if search:
                query = query.where(
                    text("tsv @@ plainto_tsquery('russian', :q)")
                ).params(q=search)
                query = query.order_by(
                    text("ts_rank(tsv, plainto_tsquery('russian', :q)) DESC")
                ).params(q=search)
            else:
                query = query.order_by(Post.created_at.desc())
            query = query.offset((page_number - 1) * page_size).limit(page_size)
            result = await self.session.execute(statement=query)
            posts = result.scalars().all()

            return posts
