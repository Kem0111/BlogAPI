from typing import List, Optional

from fastapi.exceptions import HTTPException
from fastapi.param_functions import Body
from fastapi import APIRouter, Depends, Path, Query
from starlette import status

from sqlalchemy import Select, select
from sqlalchemy.orm import joinedload

from src.core.depends import DatabaseSession, authorization
from src.orm.user import UserModel
from src.orm import PostModel
from src.schemas import (ApplicationResponse,
                         RouteReturn,
                         Posts,
                         BodyPostRequest,
                         BodyUpdatePostRequest)
from .like import router as post_like_router
from .dislike import router as post_dislike_router


router = APIRouter()


async def get_all_posts_core(posts: List[PostModel]):
    return [
            {
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "author": post.author.username,
                "created_at": post.created_at,
            }
            for post in posts
    ]


@router.get(
    path="/",
    summary="WORKS: Get posts from database with pagination.",
    response_model=ApplicationResponse[List[Optional[Posts]]],
    status_code=status.HTTP_200_OK
)
async def get_all_posts(
    session: DatabaseSession,
    page: int = Query(1, ge=1, title="Page number"),
    per_page: int = Query(10, ge=1, le=100, title="Items per page")
) -> RouteReturn:

    offset = (page - 1) * per_page

    query: Select = (
        select(PostModel)
        .options(joinedload(PostModel.author))
        .offset(offset)
        .limit(per_page)
    )
    result = await session.execute(query)
    posts = result.scalars().all()

    return {
        "ok": True,
        "result": await get_all_posts_core(posts)
    }


@router.post(
    path="/add_post",
    summary="WORK: add post in database",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK
)
async def add_post(
    session: DatabaseSession,
    request: BodyPostRequest = Body(...),
    user: UserModel = Depends(authorization)
) -> RouteReturn:
    
    new_post = PostModel(
        title=request.title,
        description=request.description,
        author_id=user.id
    )
    session.add(new_post)
    await session.commit()

    return {
        "ok": True,
        "result": True
    }


@router.patch(
    path="/{post_id}/update_post",
    summary="WORK: update title or description of post",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK
)
async def update_post(
    session: DatabaseSession,
    request: BodyUpdatePostRequest = Body(...),
    post_id: int = Path(..., title="The ID of the post to update"),
    user: UserModel = Depends(authorization)
) -> RouteReturn:

    query: Select = select(PostModel).where(PostModel.id == post_id)
    result = await session.execute(query)
    post = result.scalars().first()

    if not post or post.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post not found or the user isn't the author of the post"
        )
    if request.title:
        post.title = request.title
    if request.description:
        post.description = request.description

    await session.commit()

    return {
        "ok": True,
        "result": True
    }


@router.delete(
    path="/{post_id}/delete_post",
    summary="WORK: Delete post from database",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK
)
async def delete_post(
    session: DatabaseSession,
    post_id: int = Path(..., title="The ID of the post to delete"),
    user: UserModel = Depends(authorization)
) -> RouteReturn:

    post = await session.get(PostModel, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if post.author_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    await session.delete(post)
    await session.commit()

    return {
        "ok": True,
        "result": True
    }


router.include_router(post_like_router)
router.include_router(post_dislike_router)
