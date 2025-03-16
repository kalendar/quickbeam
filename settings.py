from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class __Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="quickbeam_")

    sqlite_database_path: str = Field()


SETTINGS = __Settings()  # type: ignore
