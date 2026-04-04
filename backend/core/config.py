from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # This attribute will automatically load from the DATABASE_URL environment variable
    DATABASE_URL: str

    class Config:
        # Specifies the .env file to load
        env_file = ".env"

settings = Settings()