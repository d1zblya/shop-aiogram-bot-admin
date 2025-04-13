import logging

from dotenv import load_dotenv
from typing import List, Union

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class DBSettings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    @property
    def DATABASE_URL(self):
        return (f"postgresql+asyncpg://"
                f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
                f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMINS: Union[int, List[int]]

    @field_validator("ADMINS", mode="before")
    def parse_admins(cls, v: Union[str, int, List[int]]) -> Union[int, List[int]]:
        if isinstance(v, str):
            return [int(admin_id.strip()) for admin_id in v.split(",")]
        elif isinstance(v, int):
            return v
        elif isinstance(v, list):
            return v
        raise ValueError(f"Invalid value for ADMINS: {v}")

    db: DBSettings = DBSettings()

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
