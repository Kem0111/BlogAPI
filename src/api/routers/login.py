from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body
from fastapi.responses import Response
from starlette import status
from sqlalchemy import Select, select

from src.core.depends import (AuthJWT,
                              AuthorizationRefresh,
                              DatabaseSession,
                              authorization)
from src.core.security import check_hashed_password
from src.schemas import ApplicationResponse, RouteReturn, BodyLoginRequest
from src.utils.cookies import set_and_create_tokens_cookies
from src.orm import UserModel

router = APIRouter()


@router.post(
    path="/",
    summary="WORKS: User login (token creation).",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK,
)
async def login_user(
    response: Response,
    authorize: AuthJWT,
    session: DatabaseSession,
    request: BodyLoginRequest = Body(...),
) -> RouteReturn:

    query: Select = select(UserModel).where(
        UserModel.email == request.email
    )
    result = await session.execute(query)
    user = result.scalars().first()

    if (
        not user  # user not found
        or not check_hashed_password(
            password=request.password, hashed=user.password
        )  # password doesn't  matches
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong email or password",
        )

    set_and_create_tokens_cookies(response=response,
                                  authorize=authorize,
                                  subject=user.id)

    return {
        "ok": True,
        "result": True,
    }


@router.post(
    path="/refresh/",
    dependencies=[Depends(authorization)],
    summary="WORKS (need X-CSRF-TOKEN in headers): Refresh all tokens.",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK,
)
async def refresh_jwt_tokens(
    response: Response,
    authorize: AuthJWT,
    user: AuthorizationRefresh,
) -> RouteReturn:

    set_and_create_tokens_cookies(response=response,
                                  authorize=authorize,
                                  subject=user.id)

    return {
        "ok": True,
        "result": True,
    }
