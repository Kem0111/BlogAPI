from __future__ import annotations

from sqlalchemy import ForeignKey, Integer
from src.orm.config import ORMModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .post import PostModel
    from .user import UserModel


class DislikeModel(ORMModel):
    __tablename__ = "dislike"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id"))

    user: Mapped[UserModel] = relationship(
        "UserModel",
        back_populates="dislikes",
    )
    post: Mapped[PostModel] = relationship(
        "PostModel",
        back_populates="dislikes",
    )
