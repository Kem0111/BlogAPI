from pydantic import EmailStr, BaseModel, Field
from src.metadata import PASSWORD_REGEX


class Login(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=30, regex=PASSWORD_REGEX)
