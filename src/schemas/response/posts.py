from datetime import datetime
from pydantic import BaseModel


class Posts(BaseModel):
    id: int
    title: str
    description: str
    author: str
    likes_count: int
    dislikes_count: int
    created_at: datetime
