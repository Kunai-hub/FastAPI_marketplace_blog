from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.fastapi_marketplace_blog.schemas.schemas import (
    CategoryCreate,
    CategoryResponse,
)
from src.fastapi_marketplace_blog.db.database import get_db
from src.fastapi_marketplace_blog.repositories.categories import CategoryRepository


category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.post("/create", response_model=CategoryResponse)
async def create_category(
    request: Request, body: CategoryCreate, db=Depends(get_db)
) -> CategoryResponse:
    if not getattr(request.state, "user", None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    try:
        slug = body.slug or body.name.lower().replace(" ", "-")
        name = body.name
        repo = CategoryRepository(session=db)
        category = await repo.create_category(name=name, slug=slug)

        return CategoryResponse(
            id=category.id,
            name=category.name,
            slug=category.slug,
            created_at=category.created_at,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database error: {str(e)}",
        )


@category_router.get("/", response_model=list[CategoryResponse])
async def get_categories(db=Depends(get_db)) -> list[CategoryResponse]:
    repo = CategoryRepository(session=db)
    category_list = await repo.get_categories()

    return category_list
