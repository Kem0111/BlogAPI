from __future__ import annotations

from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from src.core.security import settings
from fastapi_jwt_auth.exceptions import MissingTokenError
from src.api.api import router
from starlette.responses import JSONResponse
from starlette import status

app = FastAPI(title="TaskFlow")

app.include_router(router)


@AuthJWT.load_config
def get_config():
    return settings


# @app.exception_handler(MissingTokenError)
# async def missing_token_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         content={"message": "Missing refresh token. Please re-authenticate."},
#     )
