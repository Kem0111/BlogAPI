from __future__ import annotations

from datetime import datetime as dt
from sqlalchemy import DateTime, String
from src.orm.config import ORMModel
from sqlalchemy.orm import Mapped, mapped_column
# from typing import TYPE_CHECKING, List

# if TYPE_CHECKING:
#     from .wallet import WalletModel


class UserModel(ORMModel):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    last_name: Mapped[str] = mapped_column(String(150), nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(150))
    created_at: Mapped[dt] = mapped_column(DateTime, default=dt.utcnow)
