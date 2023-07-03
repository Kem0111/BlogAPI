from typing import Optional

from fastapi.param_functions import Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt_auth.exceptions import MissingTokenError

from src.orm import UserModel
from fastapi import HTTPException
from src.orm.config import get_async_session
from starlette import status
from sqlalchemy import select, Select


async def account(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Optional[UserModel]:

    query: Select = select(UserModel).where(
        UserModel.id == user_id
    )
    result = await session.execute(query)

    return result.scalars().first()


async def authorization_refresh(
    authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> UserModel:
    authorize.jwt_refresh_token_required()

    return await account(user_id=authorize.get_jwt_subject(), session=session)


async def authorization(
    authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> UserModel:
    try:
        authorize.jwt_required()
    except MissingTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing JWT-token"
        )

    return await account(user_id=authorize.get_jwt_subject(), session=session)


async def authorization_optional(
    authorize: AuthJWT = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> Optional[UserModel]:
    authorize.jwt_optional()

    return await account(user_id=authorize.get_jwt_subject(), session=session)
