from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    dp_type: str = Field("sqlite", env="DP_TYPE")
    sqlite_url: str = Field("sqlite:///./medical.db", env="SQLITE_URL")
    postgresql_url: str = Field("postgresql+psycopg2://user:password@localhost/dbname", env="POSTGRESQL_URL")
    mysql_url: str = Field("mysql+pymysql://user:password@localhost/dbname", env="MYSQL_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
