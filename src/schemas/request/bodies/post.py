from pydantic import BaseModel, Field


class Post(BaseModel):
    title: str = Field(..., max_length=250)
    description: str
