from pathlib import Path
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # Base
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # PostgreSQL
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    class Config:
        env_file = BASE_DIR / "dev.env"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

settings = Settings()
