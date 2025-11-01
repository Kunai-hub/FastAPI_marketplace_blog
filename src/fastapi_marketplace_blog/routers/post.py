from fastapi import APIRouter, Request, Depends, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError

from src.fastapi_marketplace_blog.db.database import get_db
from src.fastapi_marketplace_blog.repositories.posts import PostRepository
from src.fastapi_marketplace_blog.schemas.schemas import (
    PostResponse,
    PostCreate,
    CategoryResponse,
    PostUpdate,
)

MAX_PAGE_SIZE = 50

post_router = APIRouter(prefix="/posts", tags=["posts"])


@post_router.post("/create", response_model=PostResponse)
async def create_post(
    request: Request, body: PostCreate, db=Depends(get_db)
) -> PostResponse:
    if not getattr(request.state, "user", None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    try:
        title = body.title
        text = body.text
        category_id = body.category_id
        image = body.image
        repo = PostRepository(db)
        post = await repo.create_post(
            title=title, text=text, category_id=category_id, image=image
        )

        return PostResponse(
            id=post.id,
            title=post.title,
            text=post.text,
            category=CategoryResponse(
                id=post.category.id,
                name=post.category.name,
                slug=post.category.slug,
                created_at=post.category.created_at,
            ),
            image=post.image,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error: {str(e)}",
        )


@post_router.get("/", response_model=list[PostResponse])
async def get_posts(
    db=Depends(get_db),
    search: str | None = Query(None),
    category_id: int | None = Query(None),
    page_number: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=MAX_PAGE_SIZE),
) -> list[PostResponse]:
    repo = PostRepository(session=db)
    post_list = await repo.get_posts(
        search=search,
        category_id=category_id,
        page_number=page_number,
        page_size=page_size,
    )

    return post_list


@post_router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    request: Request,
    body: PostUpdate,
    db=Depends(get_db),
) -> PostResponse:
    if not getattr(request.state, "user", None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    try:
        repo = PostRepository(session=db)
        post = await repo.update_post(post_id=post_id, data=body)

        return PostResponse(
            id=post.id,
            title=post.title,
            text=post.text,
            category=CategoryResponse(
                id=post.category.id,
                name=post.category.name,
                slug=post.category.slug,
                created_at=post.category.created_at,
            ),
            image=post.image,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error: {str(e)}",
        )


@post_router.delete("/{post_id}", response_model=PostResponse)
async def delete_post(
    post_id: int,
    request: Request,
    db=Depends(get_db),
) -> PostResponse:
    if not getattr(request.state, "user", None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    try:
        repo = PostRepository(session=db)
        post = await repo.delete_post(post_id=post_id)

        return PostResponse(
            id=post.id,
            title=post.title,
            text=post.text,
            category=CategoryResponse(
                id=post.category.id,
                name=post.category.name,
                slug=post.category.slug,
                created_at=post.category.created_at,
            ),
            image=post.image,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error: {str(e)}",
        )
