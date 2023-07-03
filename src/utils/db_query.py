from typing import Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy.ext.declarative import DeclarativeMeta


async def check_duplicates(session: AsyncSession,
                           model: Type[DeclarativeMeta],
                           field: str,
                           value: str):
    query: Select = select(model).where(
            getattr(model, field) == value
        )
    result = await session.execute(query)

    return result.scalars().first()
