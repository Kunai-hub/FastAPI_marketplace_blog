from fastapi import FastAPI

from src.fastapi_marketplace_blog.routers.auth import auth_router


def get_app() -> FastAPI:
    app = FastAPI(title="MarketPlace Blog")
    app.include_router(auth_router)

    return app
