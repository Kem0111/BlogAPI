from datetime import datetime
from pydantic import BaseModel


class Posts(BaseModel):
    id: int
    title: str
    description: str
    author: str
    created_at: datetime
