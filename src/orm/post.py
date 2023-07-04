from __future__ import annotations

from datetime import datetime as dt
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from src.orm.config import ORMModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from .user import UserModel
    from .like import LikeModel
    from .dislike import DislikeModel


class PostModel(ORMModel):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    description: Mapped[str] = mapped_column(Text)

    author_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user.id"),
        nullable=False
    )
    author: Mapped[UserModel] = relationship(
        "UserModel",
        back_populates="posts"
    )
    likes: Mapped[List[LikeModel]] = relationship(
        "LikeModel",
        back_populates="post"
    )
    dislikes: Mapped[List[DislikeModel]] = relationship(
        "DislikeModel",
        back_populates="post"
    )

    created_at: Mapped[dt] = mapped_column(DateTime, default=dt.utcnow)
