from typing import Optional, Union, Sequence

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.fastapi_marketplace_blog.db.models import Post, PostArchive, Category
from src.fastapi_marketplace_blog.schemas.schemas import PostUpdate


class PostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_post(
        self, title: str, text: str, category_id: int, image: Optional[str] = None
    ) -> Post:
        async with self.session.begin():
            cat = await self.session.get(Category, category_id)

            if not cat:
                raise ValueError("Category does not exist")
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

    async def update_post(self, post_id: int, data: PostUpdate) -> Post:
        async with self.session.begin():
            post = await self.session.get(Post, post_id)

            if not post:
                raise ValueError("Post not found")
            post.title = data.title or post.title
            post.text = data.text or post.text
            post.category_id = data.category_id or post.category_id
            post.image = data.image or post.image
            self.session.add(post)
            await self.session.flush()
            query = (
                select(Post)
                .options(selectinload(Post.category))
                .where(Post.id == post.id)
            )
            result = await self.session.execute(statement=query)

            return result.scalar_one()

    async def delete_post(self, post_id: int) -> Post:
        async with self.session.begin():
            post = await self.session.get(Post, post_id)

            if not post:
                raise ValueError("Post not found")
            post_archive = PostArchive(
                title=post.title,
                text=post.text,
                category_id=post.category_id,
                image=post.image,
                created_at=post.created_at,
                updated_at=post.updated_at,
            )
            self.session.add(post_archive)
            await self.session.flush()
            query = (
                select(Post)
                .options(selectinload(Post.category))
                .where(Post.id == post.id)
            )
            result = await self.session.execute(statement=query)
            await self.session.delete(post)

            return result.scalar_one()
