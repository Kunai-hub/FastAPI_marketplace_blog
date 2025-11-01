from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    WEB_PORT: int

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    JWT_SECRET: str
    JWT_ALGORITHM: str

    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_PORT: int

    SMTP_HOST: str
    SMTP_PORT: int
    EMAIL_FROM: str
    EMAIL_PASSWORD: str

    S3_ENDPOINT: str
    S3_REGION: str
    S3_ACCESS: str
    S3_SECRET: str
    S3_BUCKET: str
    S3_PORT: int

    model_config = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )


config = Settings()
