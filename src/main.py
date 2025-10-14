from fastapi import FastAPI

from src.fastapi_marketplace_blog.routers.auth import auth_router
from src.fastapi_marketplace_blog.routers.category import category_router


def get_app() -> FastAPI:
    app = FastAPI(title="MarketPlace Blog")
    app.include_router(auth_router)
    app.include_router(category_router)

    return app
