from fastapi import APIRouter, Depends, Path
from starlette import status


from src.core.depends import DatabaseSession, authorization
from src.orm.dislike import DislikeModel
from src.orm.like import LikeModel

from src.orm.user import UserModel
from src.schemas import ApplicationResponse, RouteReturn
from .utils.common import (get_like_or_dislike,
                           get_post_with_like_and_dislike,
                           check_post_and_posts_author)

router = APIRouter()


@router.post(
    path="/{post_id}/like",
    summary="WORK: Like a post, unlike and undislike if post if already liked",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK
)
async def like_post(
    session: DatabaseSession,
    post_id: int = Path(..., title="The ID of the post to like"),
    user: UserModel = Depends(authorization)
) -> RouteReturn:

    post = await get_post_with_like_and_dislike(
        session=session,
        post_id=post_id
    )

    await check_post_and_posts_author(post, user.id)

    like = await get_like_or_dislike(
        session=session,
        model=LikeModel,
        user_id=user.id,
        post_id=post.id
    )

    dislike = await get_like_or_dislike(
        session=session,
        model=DislikeModel,
        user_id=user.id,
        post_id=post.id
    )
    if like:
        # User has already liked this post, so unlike it
        await session.delete(like)
        await session.commit()
        return {
            "ok": True,
            "result": False
        }

    if dislike:
        # Remove the dislike if the user disliked the post,
        # because user desided to liked it
        await session.delete(dislike)

    # Like the post
    new_like = LikeModel(user_id=user.id, post_id=post_id)
    session.add(new_like)
    await session.commit()

    return {
        "ok": True,
        "result": True
    }
