from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "JobSentinel API"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://postgres:1547@localhost:5433/PSgvecors"
    secret_key: str = "job-sentinel-secret-key-change-me"
    jwt_algorithm: str = "HS256"

    @property
    def database_url_for_sqlalchemy(self) -> str:
        return self.database_url

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
