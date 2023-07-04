from __future__ import annotations

from sqlalchemy import ForeignKey, Integer
from src.orm.config import ORMModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .post import PostModel
    from .user import UserModel


class LikeModel(ORMModel):
    __tablename__ = "like"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id"))

    user: Mapped[UserModel] = relationship(
        "UserModel",
        back_populates="likes",
    )
    post: Mapped[PostModel] = relationship(
        "PostModel",
        back_populates="likes",
    )
