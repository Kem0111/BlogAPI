from fastapi import APIRouter


from .routers import (
    register_router,
    login_router,
    logout_router,
    post_router,
)


def create_api_router() -> APIRouter:
    api_router = APIRouter()
    api_router.include_router(register_router, tags=["register"], prefix="/register")
    api_router.include_router(login_router, tags=["login"], prefix="/login")
    api_router.include_router(logout_router, tags=["logout"], prefix="/logout")
    api_router.include_router(post_router, tags=["posts"], prefix="/posts")

    return api_router


router = create_api_router()
