from pydantic import EmailStr, Field, BaseModel


class Register(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str = Field(..., max_length=30)
