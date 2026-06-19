from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./monitoring.db"

    # Green API (WhatsApp)
    GREEN_API_INSTANCE_ID: str = "7107657987"
    GREEN_API_TOKEN: str = "8a6f909399e94d5fa6dbe7ae1430cb497200ff5b72e44c6c97"
    GREEN_API_URL: str = "https://api.green-api.com"

    # Monitoring
    CHECK_INTERVAL_SECONDS: int = 60

    # App
    SECRET_KEY: str = "438cb8493618a37c46dc96a9c2db7e18227f9bb8e96609a35d206abe911ff992"
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()