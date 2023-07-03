from typing import Optional
from pydantic import BaseSettings as PydanticBaseSettings


class BaseSettings(PydanticBaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class DatabaseSettings(BaseSettings):
    DATABASE_DRIVER: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_NAME: str

    @property
    def url(self) -> str:
        driver, user, password, host, port, name = (
            self.DATABASE_DRIVER,
            self.DATABASE_USERNAME,
            self.DATABASE_PASSWORD,
            self.DATABASE_HOSTNAME,
            self.DATABASE_PORT,
            self.DATABASE_NAME,
        )

        return f"{driver}://{user}:{password}@{host}:{port}/{name}"


database_settings = DatabaseSettings()


class JWTSettings(BaseSettings):
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRATION_TIME: int
    REFRESH_TOKEN_EXPIRATION_TIME: int
    COOKIE_SECURE: bool
    COOKIE_CSRF: bool
    COOKIE_SAMESITE: str
    COOKIE_DOMAIN: Optional[str] = None
    JWT_SECRET_KEY: str


jwt_settings = JWTSettings()
