
from typing import Optional, Union
from fastapi import HTTPException
from starlette import status

from sqlalchemy import and_, select, Select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.orm.dislike import DislikeModel
from src.orm.like import LikeModel
from src.orm.post import PostModel


async def get_like_or_dislike(
        session: AsyncSession,
        model: Union[LikeModel, DislikeModel],
        user_id: int,
        post_id: int
) -> Optional[Union[LikeModel, DislikeModel]]:
    query: Select = (
        select(model).
        where(and_(
            model.user_id == user_id,
            model.post_id == post_id
            )
        )
    )
    result = await session.execute(query)
    reaction = result.scalar_one_or_none()
    return reaction


async def get_post_with_like_and_dislike(session: AsyncSession, post_id: int):
    post_query: Select = (
        select(PostModel).
        options(selectinload(PostModel.likes)).
        options(selectinload(PostModel.dislikes)).
        where(PostModel.id == post_id)
    )
    result = await session.execute(post_query)
    post = result.scalar_one_or_none()
    return post


async def check_post_and_posts_author(post: PostModel, user_id: int) -> None:
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if post.author_id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The post's author is user"
        )
