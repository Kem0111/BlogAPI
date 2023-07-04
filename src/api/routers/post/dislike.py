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
    path="/{post_id}/dislike",
    summary="WORK: Like a post, unlike and undislike if post if already liked",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK
)
async def like_post(
    session: DatabaseSession,
    post_id: int = Path(..., title="The ID of the post to dislike"),
    user: UserModel = Depends(authorization)
) -> RouteReturn:

    post = await get_post_with_like_and_dislike(
        session=session,
        post_id=post_id
    )

    await check_post_and_posts_author(post, user.id)

    # For check if the user has liked this post
    like = await get_like_or_dislike(
        session=session,
        model=LikeModel,
        user_id=user.id,
        post_id=post.id
    )
    # For  check if the user has disliked this post
    dislike = await get_like_or_dislike(
        session=session,
        model=DislikeModel,
        user_id=user.id,
        post_id=post.id
    )
    if dislike:
        # User has already disliked this post, so undislike it
        await session.delete(dislike)
        await session.commit()
        return {
            "ok": True,
            "result": False
        }

    if like:
        # Remove the like if the user liked the post,
        # because user desided to disliked it
        await session.delete(like)

    # dislike the post
    new_dislike = DislikeModel(user_id=user.id, post_id=post_id)
    session.add(new_dislike)
    await session.commit()

    return {
        "ok": True,
        "result": True
    }
