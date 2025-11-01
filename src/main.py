from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.fastapi_marketplace_blog.core.config import config
from src.fastapi_marketplace_blog.db.database import get_db
from src.fastapi_marketplace_blog.routers.auth import (
    auth_router,
    ACCESS_COOKIE,
    REFRESH_COOKIE,
)
from src.fastapi_marketplace_blog.routers.category import category_router
from src.fastapi_marketplace_blog.routers.post import post_router
from src.fastapi_marketplace_blog.routers.image import image_router
from src.fastapi_marketplace_blog.services.access_token_creater import (
    decode_token,
    create_access_token,
)
from src.fastapi_marketplace_blog.repositories.auths import AuthRepository

PUBLIC_PATHS = ["/auth", "/docs", "/redoc", "/openapi.json"]


def get_app() -> FastAPI:
    app = FastAPI(title="MarketPlace Blog")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def jwt_middleware(request: Request, call_next):
        path = request.url.path

        if any(path.startswith(p) for p in PUBLIC_PATHS):
            return await call_next(request)

        access_token = request.cookies.get(ACCESS_COOKIE)
        refresh_token = request.cookies.get(REFRESH_COOKIE)
        payload = decode_token(token=access_token) if access_token else None

        if payload:
            user_email = payload.get("sub")
            user = None

            async for db in get_db():
                repo = AuthRepository(session=db)
                user = await repo.get_user_by_email_for_auth(email=user_email)
                break

            if not user:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "User not found."},
                )

            request.state.user = user

            return await call_next(request)

        if not refresh_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing refresh token."},
            )
        ref_payload = decode_token(token=refresh_token)

        if not ref_payload:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid refresh token."},
            )

        user_email = ref_payload.get("sub")
        user = None

        async for db in get_db():
            repo = AuthRepository(session=db)
            user = await repo.get_user_by_email_for_auth(email=user_email)
            break

        if not user:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "User not found."},
            )

        new_access_token = create_access_token(
            data={"sub": user_email}, method="access"
        )
        new_refresh_token = create_access_token(
            data={"sub": user_email}, method="refresh"
        )
        request.state.user = user
        response = await call_next(request)
        response.set_cookie(
            key=ACCESS_COOKIE,
            value=new_access_token,
            httponly=True,
            samesite="lax",
            path="/",
            max_age=config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        response.set_cookie(
            key=REFRESH_COOKIE,
            value=new_refresh_token,
            httponly=True,
            samesite="lax",
            path="/",
            max_age=config.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        )

        return response

    app.include_router(auth_router)
    app.include_router(category_router)
    app.include_router(post_router)
    app.include_router(image_router)

    return app
