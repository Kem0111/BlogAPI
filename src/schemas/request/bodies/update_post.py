from pydantic import BaseModel, Field
from typing import Optional


class UpdatePost(BaseModel):
    title: Optional[str] = Field(..., max_length=250)
    description: Optional[str]
