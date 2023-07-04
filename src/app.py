from __future__ import annotations

from fastapi import FastAPI
from fastapi_jwt_auth import AuthJWT
from src.core.security import settings

from src.api.api import router


app = FastAPI(title="TaskFlow")

app.include_router(router)


@AuthJWT.load_config
def get_config():
    return settings
