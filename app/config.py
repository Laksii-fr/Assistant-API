from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
        DATABASE_URL: str
        MONGO_INITDB_DATABASE: str
        OPENAI_API_KEY: str
        CLIENT_ORIGIN: str
        EMAIL_FROM: EmailStr

        class Config:
                env_file = './.env'


settings = Settings()
