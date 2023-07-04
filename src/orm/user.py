from __future__ import annotations

from datetime import datetime as dt
from sqlalchemy import DateTime, String
from src.orm.config import ORMModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from .post import PostModel
    from .like import LikeModel
    from .dislike import DislikeModel


class UserModel(ORMModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] = mapped_column(String(250), nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(
        String(250),
        unique=True,
        nullable=False
    )

    posts: Mapped[List[PostModel]] = relationship(
        "PostModel",
        back_populates="author",
        cascade="all, delete-orphan"
    )
    likes: Mapped[List[LikeModel]] = relationship(
        "LikeModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    dislikes: Mapped[List[DislikeModel]] = relationship(
        "DislikeModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    created_at: Mapped[dt] = mapped_column(DateTime, default=dt.utcnow)
