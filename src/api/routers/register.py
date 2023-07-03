from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body
from starlette import status

from src.core.security import hash_password
from src.core.depends import DatabaseSession
from src.orm import UserModel
from src.schemas import (
    ApplicationResponse,
    BodyRegisterRequest,
    RouteReturnT
)
from src.utils.db_query import check_duplicates

router = APIRouter()


@router.post(
    path="/",
    summary="WORKS: User registration.",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    session: DatabaseSession,
    request: BodyRegisterRequest = Body(...),
) -> RouteReturnT:

    async with session.begin():

        if await check_duplicates(session,
                                  UserModel,
                                  'username',
                                  request.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username is already registered",
            )

        if await check_duplicates(session,
                                  UserModel,
                                  'email',
                                  request.email):

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email is already registered",
            )

        new_user = UserModel(
            first_name=request.first_name,
            last_name=request.last_name,
            username=request.username,
            email=request.email,
            password=hash_password(password=request.password),
        )
        session.add(new_user)
    return {
        "ok": True,
        "result": True,
    }
