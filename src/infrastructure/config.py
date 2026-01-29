from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
    
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "cleanarch_db"
    database_user: str = "postgres"
    database_password: str = "postgres"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = False


settings = Settings()

